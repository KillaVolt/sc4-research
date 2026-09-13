# Coverage and limits

The aggregate results below describe one local GOG 1.1.641.0 installation and its copied plugin set. The proprietary working archive is not part of this repository.

## Native analysis

| Target/pass | Functions attempted | Pseudocode produced | Instruction bytes checked |
|---|---:|---:|---:|
| Windows game, conservative pass | 23,601 | 23,597 | 6,509,711 |
| Windows game, deeper discovery | 35,629 | 35,624 | 6,509,693 |
| Bundled `dbghelp.dll` | 3,222 | 3,222 | 387,736 |
| Installed SC4Fix | 552 | 552 | 68,498 |
| Installed Extra Cheats | 1,758 | 1,758 | 195,539 |
| Mac Rev A Intel reference | 67,188 | 67,188 | 8,281,854 |

The Windows passes overlap. Their counts are analysis boundaries, not a count of original Maxis functions. Instruction-byte checks establish that exports refer to the analyzed binaries; they do not prove correct function boundaries, types, expressions, or behavior.

Two Windows failures have improved experimental outputs. Three original failures remain at `0x006ed6e0`, `0x00775cc0`, and `0x0077c660`.

The debug-bearing Mac slices exposed 564,265 Intel and 69,550 PowerPC symbol/debug records. Grouping produced 1,735 class or outer-qualifier guides and 94,951 method/address records. Mac addresses and ABI details are not Windows mappings. No source-line records or original source-file contents were recovered from those paths.

## Resources

- 232,301 base-game DBPF entries extracted.
- 51,338 copied-plugin DBPF entries extracted.
- 3,254,351,675 decompressed resource bytes checked.
- Zero outstanding raw-extraction integrity failures after targeted rechecks.
- 2,049 shipped-city resources retain higher-level parser errors and their raw bytes.

Decoded representations are convenience views. A PNG, WAV, JSON file, or C-like decompiler output is not automatically a byte-identical build input.

## Missing pieces

This repository does not provide original native comments or local variable names, a matching Windows PDB, a full PowerPC decompilation, a reconstructed build system, a complete behavioral test suite, or a demonstrated replacement executable.

The embedded Windows PDB identity is:

```text
GUID 46e5cc8b-14c3-4e10-826f-ca9752664c89
age  7
key  46E5CC8B14C34E10826FCA9752664C897
```

The historical path in the binary is `c:\SimCity4\SC4000Projects\Ep1\out\ReleaseSRT\SimCity 4.pdb`. A Microsoft public-symbol-server lookup for the exact identity returned no file; that does not prove a copy does not exist elsewhere.

