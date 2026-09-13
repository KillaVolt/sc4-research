"""Find reviewable Windows/Mac function-name candidates from shared string references."""
from pathlib import Path
import collections,csv,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/symbols/cross-build'

def rows(path):
    with path.open(encoding='utf-8',newline='') as f:yield from csv.DictReader(f,delimiter='\t')

def references(program):
    by_string=collections.defaultdict(set)
    for r in rows(ROOT/'artifacts/code'/program/'string-references.tsv'):
        if len(r['value'])>=12:by_string[r['value']].add(r['function'])
    return by_string

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    windows=references('SimCity4-deep')
    mac_program='Mac-RevA-x86-named' if (ROOT/'artifacts/code/Mac-RevA-x86-named/export-summary.txt').exists() else 'Mac-RevA-x86'
    mac=references(mac_program);names=collections.defaultdict(set)
    for r in rows(ROOT/'artifacts/symbols/mac/x86/functions.tsv'):names[r['address']].add(r['demangled'])
    pairs=collections.defaultdict(list)
    for value in windows.keys()&mac.keys():
        # ponytail: bounded string-based candidates only; structural binary matching is a separate investigation.
        if len(windows[value])>4 or len(mac[value])>4:continue
        for w in windows[value]:
            for m in mac[value]:pairs[w,m].append(dict(value=value,windowsUsers=len(windows[value]),macUsers=len(mac[value])))
    candidates=[]
    for (w,m),evidence in pairs.items():
        unique=sum(e['windowsUsers']==e['macUsers']==1 for e in evidence)
        if len(evidence)<2 and not(unique and len(evidence[0]['value'])>=28):continue
        candidates.append(dict(windowsAddress=w,macAddress=m,macNames=sorted(names.get(m,[])),anchors=sorted(evidence,key=lambda x:x['value']),
                               uniqueAnchors=unique,confidence='multiple-unique-string-anchors' if unique>=2 else 'string-reference-candidate'))
    candidates.sort(key=lambda r:(-r['uniqueAnchors'],-len(r['anchors']),r['windowsAddress'],r['macAddress']))
    (OUT/'string-candidates.json').write_text(json.dumps(candidates,indent=2),encoding='utf-8')
    lines=['# Windows and Mac function comparison candidates','','Shared strings provide leads, not proof of equivalent functions. Port-specific wrappers, inlining, and common diagnostics can produce misleading matches. No Windows names or addresses were automatically replaced. Review the full JSON for competing candidates and exact string users.','', '| Windows address | Mac address | Mac symbol names | Shared / unique anchors |','|---|---|---|---|']
    for r in candidates:
        names_text='; '.join(r['macNames']).replace('|','\\|')
        lines.append(f"| [{r['windowsAddress']}](../../code/SimCity4-deep/functions/{r['windowsAddress']}.c) | [{r['macAddress']}](../../code/{mac_program}/functions/{r['macAddress']}.c) | {names_text} | {len(r['anchors'])} / {r['uniqueAnchors']} |")
    # Failed functions have diagnostic files instead of .c output; use their actual index paths.
    for program in ('SimCity4-deep',mac_program):
        for f in rows(ROOT/'artifacts/code'/program/'functions.tsv'):
            if f['status']!='decompiled':lines=[line.replace(f'{program}/functions/{f["address"]}.c',f'{program}/{f["file"]}') for line in lines]
    (OUT/'STRING-CANDIDATES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    summary=dict(candidatePairs=len(candidates),windowsFunctions=len({r['windowsAddress'] for r in candidates}),
                 multipleUniqueAnchorPairs=sum(r['uniqueAnchors']>=2 for r in candidates),macProgram=mac_program)
    assert all(r['anchors'] for r in candidates)
    (ROOT/'manifests/cross-build-string-candidates.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)
if __name__=='__main__':run()
