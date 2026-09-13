# Reproducing the native findings

## Requirements

- A lawful copy of the GOG Windows 1.1.641.0 executable.
- SHA-256 `3bc5c7fe807fe5aa24a3abb06e40f13486670bc1150612c09baf4ecedafe1a4b`.
- Ghidra 12.1.3 and a Java runtime supported by that Ghidra release.
- Python 3.10 or newer for the standalone HIT script.

Work on a copied executable. The scripts change Ghidra analysis metadata, not the executable bytes.

## Ghidra scripts

Import the copied executable as a 32-bit little-endian PE and let Ghidra complete its standard analysis. The image base should be `0x00400000`.

Run the correction scripts against the imported program with an output directory as their first script argument. For a headless project, the shape of the command is:

```text
analyzeHeadless <project-directory> <project-name> \
  -process "SimCity 4.exe" \
  -readOnly \
  -scriptPath <this-repository>/ghidra \
  -postScript RepairColorReference.java <output-directory>
```

Replace the script name with `InspectAndRepairLua.java` for the Lua-interface experiment. `-readOnly` keeps the original project analysis unchanged; the scripts write their experimental output to the directory you supply.

The color-boundary script fails explicitly if the expected prologue, scalar instruction, or false candidate differs. This prevents accidentally applying a version-specific correction to another executable.

## HIT bytecode

Extract TGI `2026960b-ca4d19e3-ea768228` from `Sound.dat` using a DBPF tool, then run:

```text
python scripts/disassemble_hit.py path/to/resource.bin --out output
```

The command writes JSON and annotated assembly. It rejects unknown opcodes, truncated operands, non-boundary entry points, non-boundary branches, and any reconstruction mismatch.

## Cross-build candidates

`compare_build_strings.py` expects the working layout documented in the script:

```text
artifacts/code/SimCity4-deep/string-references.tsv
artifacts/code/Mac-RevA-x86-named/string-references.tsv
artifacts/symbols/mac/x86/functions.tsv
```

It only emits candidates. Validate a proposed match with control flow, constants, callers, data layout, and ABI differences before applying a Windows name.

