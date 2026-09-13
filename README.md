# SimCity 4 reverse-engineering notes

Here's a thing I put together while looking at **SimCity 4 Deluxe 1.1.641.0**. It collects a few reproducible findings, small analysis scripts, and coverage numbers. If any of it saves another developer some time, great.

The exact Windows target used for the address-specific notes is the GOG executable with SHA-256:

```text
3bc5c7fe807fe5aa24a3abb06e40f13486670bc1150612c09baf4ecedafe1a4b
```

Start with [the findings](docs/findings.md). The two Ghidra scripts reproduce the most concrete native-analysis corrections:

- [`InspectAndRepairLua.java`](ghidra/InspectAndRepairLua.java) supplies documented `cISCLua` call signatures to a function that otherwise fails to decompile.
- [`RepairColorReference.java`](ghidra/RepairColorReference.java) removes a false function created from the scalar value `0x00808080` and recovers the function beginning at `0x00806fa0`.

There is also a standalone [SC4 HIT bytecode disassembler](scripts/disassemble_hit.py), plus scripts for building Mac symbol guides and finding review candidates from strings shared by the Windows and Mac builds.

## What is included

- Address-specific research notes with verification boundaries.
- Reproduction instructions for the Ghidra corrections.
- A byte-round-tripping HIT parser/disassembler.
- Scripts for organizing symbols from a debug-bearing Mac reference build.
- Aggregate analysis and resource-coverage numbers.
- Links to the community projects and format research used as references.

## What is not included

There are no game executables, game assets, installed mods, decompiler dumps, Ghidra projects, third-party repositories, installers, or tool binaries here. Bring your own lawful game copy and download dependencies from their original projects.

This is research material, not recovered original Maxis source and not a buildable replacement game. Function boundaries, pseudocode, cross-build matches, and inferred field meanings need independent review.

See [reproduction](docs/reproducing.md), [coverage and limits](docs/coverage.md), and [sources](docs/sources.md).

