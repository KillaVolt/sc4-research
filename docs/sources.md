# Community and public sources

This work builds on a lot of earlier SC4 research. Use the upstream projects and their licenses directly:

- [sc4-ghidra-symbols](https://github.com/0xC0000054/sc4-ghidra-symbols) — types and function-identification data derived partly from debug-bearing Mac builds.
- [gzcom-dll](https://github.com/nsgomez/gzcom-dll) — public C++ interfaces and plugin examples, including `cISCLua`.
- [SC4Fix](https://github.com/nsgomez/sc4fix) — native plugin and reverse-engineering context.
- [scdbpf](https://github.com/memo33/scdbpf) — DBPF, FSH, S3D, exemplar, and related format implementations.
- [sc4](https://github.com/sebamarynissen/sc4) — Node DBPF/QFS and resource parser.
- [NAM](https://github.com/NAMTeam/Network-Addon-Mod) and [metarules](https://github.com/memo33/metarules) — network controller and rule-generation source.
- [sc4-effects-extensions](https://github.com/caspervg/sc4-effects-extensions) and [sc4-render-services](https://github.com/caspervg/sc4-render-services) — effects, rendering interfaces, and version-specific address research.
- [PortCellar SC4 ABI notes](https://github.com/dotcom07/PortCellar/blob/main/modules/simcity-4/docs/windows-1.1.641.md) — version and platform ABI details.
- [sc4-gzids](https://github.com/0xC0000054/sc4-gzids), [sc4-dbpf-loading](https://github.com/0xC0000054/sc4-dbpf-loading), and [resource-loading-hooks](https://github.com/0xC0000054/sc4-resource-loading-hooks) — identifiers and loading interfaces.
- [FreeSO](https://github.com/riperiperi/FreeSO) — related Maxis HIT/audio format implementation. SC4 differences still require direct validation.
- [Lua 5.0](https://www.lua.org/ftp/) — upstream language/runtime source used for comparison.
- [ATC format](https://modthesims.info/wiki.php?title=ATC), [AVP format](https://modthesims.info/wiki.php?title=AVP), and [early save-format research](https://community.simtropolis.com/forums/topic/231-discovery-file-formats-the-savegame-formats-terraintrees-etc/) — historical community format documentation.
- [SC4 Maxis files](https://community.simtropolis.com/sc4-maxis-files/) — public patch archive used as the Mac reference source.

No upstream repository is vendored here. Review its current license and version before combining code.

