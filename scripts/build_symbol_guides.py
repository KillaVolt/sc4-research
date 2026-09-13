"""Create navigable class/method guides from symbol evidence, without inventing class layouts."""
from pathlib import Path
import collections,csv,json,re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/symbols/mac'

def rows(path):
    with path.open(encoding='utf-8',newline='') as f:yield from csv.DictReader(f,delimiter='\t')

def class_name(signature):
    match=re.match(r'(?:(?:non-virtual|virtual) thunk to )?([A-Za-z_]\w*)::',signature)
    return match[1] if match else None

assert class_name('cSC4TrafficSimulator::GetData(int)')=='cSC4TrafficSimulator'
assert class_name('lua_gettop(lua_State*)') is None

def run():
    classes=collections.defaultdict(list);counts={};paths=set()
    native=ROOT/'artifacts/code/Mac-RevA-x86-named'
    available={r['address']:r['file'] for r in rows(native/'functions.tsv')} if (native/'export-summary.txt').exists() else {}
    for architecture in ('x86','ppc'):
        unique={}
        for r in rows(OUT/architecture/'functions.tsv'):
            key=(r['address'],r['demangled'])
            if key not in unique or r['source_file']:unique[key]=r
        counts[architecture]=len(unique)
        for r in unique.values():
            name=class_name(r['demangled'])
            if name:classes[name].append(dict(architecture=architecture,**r))
        for r in rows(OUT/architecture/'symbols.tsv'):
            if r['type'] in ('64','84','66') and r['name']:paths.add((architecture,r['type'],r['name']))
    pages=OUT/'classes';pages.mkdir(exist_ok=True)
    index=['# Named classes in the Mac reference builds','','These names and signatures come from symbols, not original class declarations. Return types are often absent from C++ mangling. The first class/namespace qualifier groups entries; nested classes appear on their outer group page. Mac addresses, layouts, and calling conventions are not Windows mappings. No line-number records were present.','', '| Class or outer qualifier | Method/address records |','|---|---|']
    for name,methods in sorted(classes.items()):
        index.append(f'| [{name}](classes/{name}.md) | {len(methods)} |')
        lines=[f'# {name}','','Mac reference-build symbol evidence. An Intel address links to its decompiled function where available. Source references are debug-path clues, not recovered source files.','', '| Architecture | Address | Method signature | Source reference |','|---|---|---|---|']
        for r in sorted(methods,key=lambda x:(x['architecture'],x['address'],x['demangled'])):
            address=f"`{r['address']}`"
            if r['architecture']=='x86' and r['address'] in available:address=f"[{address}](../../../code/Mac-RevA-x86-named/{available[r['address']]})"
            signature=r['demangled'].replace('|','\\|').replace('`','\\`');source=r['source_file'].replace('|','\\|')
            lines.append(f"| {r['architecture']} | {address} | `{signature}` | {source} |")
        (pages/f'{name}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/'CLASS-INDEX.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    (OUT/'source-paths.json').write_text(json.dumps([dict(architecture=a,recordType=t,path=p) for a,t,p in sorted(paths)],indent=2))
    summary=dict(classes=len(classes),methodAddressRecords=sum(map(len,classes.values())),uniqueFunctionAddressNames=counts,
                 sourcePathRecords=len(paths),intelDecompiledFunctionsAvailable=len(available))
    (ROOT/'manifests/mac-symbol-navigation.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)
if __name__=='__main__':run()
