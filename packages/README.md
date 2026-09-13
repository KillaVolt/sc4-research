# Research packages

These archives hold the large derived outputs. Split archive parts use 1,900 MiB volumes so each file remains below GitHub's per-file limit.

- [`sc4-windows-analysis.7z.001`](sc4-windows-analysis.7z.001): 36,995 files, 174,359,595 bytes unpacked, 18,260,085 bytes compressed. Contains the deepest Windows 1.1.641 pseudocode, assembly, references, coverage tables, two analysis repairs, and Windows symbol research. The redundant conservative pass, PE memory copies, original executable, and giant full-program text listing are excluded.
- [`sc4-mac-symbol-analysis.7z.001`](sc4-mac-symbol-analysis.7z.001): 70,684 files, 571,407,476 bytes unpacked, 36,517,416 bytes compressed. Contains named Intel reference pseudocode and extracted Mac symbol/class guides. The public patch binary, raw memory copies, earlier unnamed pass, and giant full-program listing are excluded.
- [`sc4-base-scripts.7z.001`](sc4-base-scripts.7z.001): 165 files, 49,437,432 bytes unpacked, 1,066,820 bytes compressed. Contains plaintext Lua and effects definitions extracted from the base game. Installed-mod scripts are excluded.
- [`sc4-base-dbpf.7z.001`](sc4-base-dbpf.7z.001): 22 files, 883,418,651 bytes unpacked, 651,416,966 bytes compressed. Contains the base game's DBPF `.dat` archives and locale archives. Executables, DLLs, city files, fonts, manual, Radio MP3s, and installed mods are excluded.
- [`sc4-base-graphics.7z.001`](sc4-base-graphics.7z.001): four volumes, 133,977 files, 2,862,897,387 bytes unpacked, 1,702,248,208 bytes compressed. Contains extracted FSH textures, S3D models, PNG conversions, cursors, icons, JPGs, and BMPs from the base-game resource set.
- [`sc4-base-audio.7z.001`](sc4-base-audio.7z.001): 4,183 files, 735,056,304 bytes unpacked, 384,488,039 bytes compressed. Contains XA sources, decoded WAVs, UDI banks, bank metadata, and UDI audio streams.
- [`sc4-base-video.7z.001`](sc4-base-video.7z.001): 14 files, 165,172,734 bytes unpacked, 156,545,882 bytes compressed. Contains the extracted MKV video outputs.
- [`sc4-ghidra-state.7z.001`](sc4-ghidra-state.7z.001): 57 files, 1,330,748,448 bytes unpacked, 158,402,249 bytes compressed. Contains the final deep Windows project, clean Mac reference project, and exported memory maps. The public copy uses a neutral Ghidra owner value.

The large DBPF, graphics, audio, video, and Ghidra volumes are stored through Git LFS. Installed-mod payloads remain excluded.

Use 7-Zip to open the first `.001` file when an archive has multiple parts. Verify `SHA256SUMS.txt` before extracting.
