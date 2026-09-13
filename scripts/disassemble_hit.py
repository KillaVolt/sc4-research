"""Strict SC4 HIT 1.8 bytecode disassembler with byte-identical reconstruction."""
from pathlib import Path
import argparse,json,struct

# B is an 8-bit register/argument; I is a 32-bit little-endian immediate.
# Layouts were checked against the SC4 Mac cHitTrackPlayer::DoCommand implementation.
OPS={2:('NoteOn','B'),3:('NoteOff','B'),4:('LoadB','BB'),5:('LoadL','BI'),6:('Set','BB'),
     7:('Call','I'),8:('Return',''),9:('Wait','B'),10:('CallEntryPoint','I'),11:('WaitSample',''),12:('End',''),13:('Jump','I'),
     0x10:('Add','BB'),0x11:('Sub','BB'),0x12:('Div','BB'),0x13:('Mul','BB'),0x14:('Compare','BB'),
     0x15:('Less','BB'),0x16:('Greater','BB'),0x17:('Not','B'),0x18:('Random','BBB'),
     0x20:('Loop',''),0x21:('SetLoop',''),0x27:('SmartChoose','B'),0x32:('PlayTrack','B'),
     0x3e:('IfEqual','I'),0x3f:('IfNotEqual','I'),0x40:('IfGreater','I'),0x41:('IfLess','I'),
     0x42:('IfGreaterOrEqual','I'),0x43:('IfLessOrEqual','I'),0x44:('SmartSetList','B'),0x46:('SequenceGroupWait','B'),
     0x47:('SequenceGroupReturn','B'),0x48:('GetSourceDataField','BBB'),0x4b:('SetLocalTarget','BB'),
     0x55:('TestRange','BBB'),0x56:('SetGlobalFromLocal','BI'),0x57:('SetLocalFromGlobal','BI'),
     0x5a:('StopTrack','B'),0x5f:('SmartIndex','BB')}

def decode(data):
    assert data[:4]==b'HIT!','HIT signature'
    major,minor=struct.unpack_from('<II',data,4)
    assert (major,minor)==(1,8),'HIT version'
    assert data[12:16]==b'TRAX','TRAX marker'
    table=data.find(b'ENTP',16)
    assert table>16 and data[-4:]==b'EENT' and (len(data)-table-8)%8==0,'entry table'
    entries=[dict(trackId=f'{track:08x}',offset=offset) for track,offset in struct.iter_unpack('<II',data[table+4:-4])]
    pc=16;instructions=[];rebuilt=bytearray(data[:16]);branches=[]
    while pc<table:
        start=pc;opcode=data[pc];pc+=1
        assert opcode in OPS,f'unknown opcode {opcode:02x} at {start:04x}'
        name,layout=OPS[opcode];length=struct.calcsize('<'+layout)
        assert pc+length<=table,'truncated operands'
        operands=struct.unpack_from('<'+layout,data,pc);pc+=length
        raw=bytes([opcode])+struct.pack('<'+layout,*operands)
        assert raw==data[start:pc]
        rebuilt.extend(raw)
        instructions.append(dict(offset=start,opcode=f'{opcode:02x}',name=name,operandLayout=layout,operands=list(operands),bytes=raw.hex()))
        if opcode in (7,13,0x3e,0x3f,0x40,0x41,0x42,0x43):branches.append(operands[0])
    starts={instruction['offset'] for instruction in instructions}
    assert all(entry['offset'] in starts for entry in entries),'entry is not an instruction boundary'
    assert all(branch in starts for branch in branches),'branch is not an instruction boundary'
    rebuilt.extend(data[table:])
    assert rebuilt==data,'byte reconstruction differs'
    return dict(format='SC4 HIT bytecode',version=[major,minor],entryPoints=entries,instructions=instructions,byteRoundTrip=True,
                note='Mnemonics aid reading; this is not original track source or a behaviorally tested replacement runtime.')

def assembly(model):
    labels={}
    for entry in model['entryPoints']:labels.setdefault(entry['offset'],[]).append(entry['trackId'])
    lines=['; SC4 HIT bytecode. Addresses are file offsets.','; Input reconstruction and instruction boundaries were checked.','']
    for instruction in model['instructions']:
        for label in labels.get(instruction['offset'],[]):lines.append(f'track_{label}:')
        operands=', '.join(f'r{value}' if kind=='B' else f'0x{value:08x}' for kind,value in zip(instruction['operandLayout'],instruction['operands']))
        lines.append(f"{instruction['offset']:04x}  {instruction['bytes']:<16}  {instruction['name']} {operands}".rstrip())
    return '\n'.join(lines)+'\n'

def self_check():
    sample=b'HIT!'+struct.pack('<II',1,8)+b'TRAX'+bytes([12])+b'ENTP'+struct.pack('<II',1,16)+b'EENT'
    model=decode(sample)
    assert model['instructions'][0]['name']=='End' and model['byteRoundTrip']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--out',type=Path,default=Path('output'))
    args=parser.parse_args();self_check()
    data=args.input.read_bytes();model=decode(data);args.out.mkdir(parents=True,exist_ok=True)
    stem=args.input.stem
    (args.out/(stem+'.hit.json')).write_text(json.dumps(model,indent=2),encoding='utf-8')
    (args.out/(stem+'.hit.asm')).write_text(assembly(model),encoding='utf-8')
    print(f"{len(model['instructions'])} instructions; {len(model['entryPoints'])} entry points; byte round trip passed")

if __name__=='__main__':main()
