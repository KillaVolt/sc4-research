# Findings worth reviewing

These are the most concrete results from the current pass. “Verified” describes the stated check only; it does not turn decompiler output into original source code. Whether any finding is new to every part of the SC4 community has not been established.

## False function at `0x00808080`

An automated Ghidra pass identified `0x00808080` as a function. The only incoming reference found was the instruction at `0x007b0d8c`, which stores `0x00808080` as a scalar with `MOV`; it is not a call or jump. The alleged entry also lands inside another x86 instruction.

The aligned prologue at `0x00806fa0` begins with:

```text
81 ec 18 02 00 00 53 55 56 57
```

It follows a return and `INT3` padding. Clearing the affected analysis range and disassembling from `0x00806fa0` recovered these body ranges:

```text
[00806fa0, 00807124]
[00807130, 008074c9]
[008074d0, 008085b1]
```

The result contains 1,838 instructions spanning 5,633 instruction bytes. Every exported instruction byte was checked against the target executable. Ghidra still reports high-level type and unreachable-block warnings, so the generated C-like output requires further work.

Reproduce it with [`RepairColorReference.java`](../ghidra/RepairColorReference.java).

## Lua-interface signatures at `0x005fc020`

The broad analysis could not decompile the function at `0x005fc020`. Its instructions access a pointer stored four bytes before a Lua state and request interface ID `0xea10c4a2`, consistent with the public `cISCLua` interface and `SCLuaUtil` implementation.

The subsequent virtual calls align with `QueryInterface`, `GetTop`, `Type`, `GetGlobal`, `IsNumber`, `ToNumber`, `Pop`, `ToString`, `PushNumber`, `PushNil`, and `Release`. Applying explicit Windows `__thiscall` prototypes at those call sites allows Ghidra to emit pseudocode.

The output still contains an incompletely modeled floating-point conversion helper. Treat it as an improved analysis result, not compilable source.

Reproduce it with [`InspectAndRepairLua.java`](../ghidra/InspectAndRepairLua.java).

## SC4 HIT bytecode

One shipped HIT 1.8 resource was decoded into 193 instructions and 22 entry points, with all branch and entry targets checked as instruction boundaries. Reassembling the header, instructions, entry table, and trailer reproduced all 869 input bytes.

Opcode layouts were checked against the SC4 Mac implementation of `cHitTrackPlayer::DoCommand`. Several layouts differ from assumptions that can be made from related Maxis games. The mnemonic names are reading aids; no replacement audio runtime has been behaviorally tested.

Use [`disassemble_hit.py`](../scripts/disassemble_hit.py) with resource TGI `2026960b-ca4d19e3-ea768228` from your own copy.

## Cross-build symbol leads

Shared string references between the Windows 1.1.641 analysis and the public Mac Rev A reference produced:

- 358 candidate Windows/Mac function pairs.
- 317 distinct Windows functions represented.
- 178 pairs supported by multiple strings that were unique to one function in each build.

These are investigation leads. Port-specific wrappers, inlining, duplicated diagnostics, and build differences can all produce false matches. No Windows symbol was renamed automatically.

## Resource checks

The private working archive extracted and hash-checked 283,639 DBPF resources. The pass also found and handled:

- 1,668 version-1 terrain-edge arrays sharing a type ID with version-2 square terrain maps. Every array round-tripped and matched the corresponding full map edge.
- 1,084 ATC and 2,253 AVP animation records with byte-identical structural round trips.
- 43 UDrive It audio banks containing 904 decodable streams.
- 26 PNG resources with valid images followed by additional bytes; both the clean image and exact trailing bytes were preserved.

Most underlying formats were already documented by community researchers. The useful part here is the exhaustive validation against this target set, not a claim that the formats were newly discovered.

