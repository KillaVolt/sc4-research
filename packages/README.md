# Research packages

These archives hold the large derived outputs. Split archive parts use 1,900 MiB volumes so each file remains below GitHub's per-file limit.

- [`sc4-windows-analysis.7z.001`](sc4-windows-analysis.7z.001): 36,995 files, 174,359,595 bytes unpacked, 18,260,085 bytes compressed. Contains the deepest Windows 1.1.641 pseudocode, assembly, references, coverage tables, two analysis repairs, and Windows symbol research. The redundant conservative pass, PE memory copies, original executable, and giant full-program text listing are excluded.
- [`sc4-mac-symbol-analysis.7z.001`](sc4-mac-symbol-analysis.7z.001): 70,684 files, 571,407,476 bytes unpacked, 36,517,416 bytes compressed. Contains named Intel reference pseudocode and extracted Mac symbol/class guides. The public patch binary, raw memory copies, earlier unnamed pass, and giant full-program listing are excluded.
- [`sc4-base-scripts.7z.001`](sc4-base-scripts.7z.001): 165 files, 49,437,432 bytes unpacked, 1,066,820 bytes compressed. Contains plaintext Lua and effects definitions extracted from the base game. Installed-mod scripts are excluded.

None of the archives contains a playable game copy. Graphics, sound, video, raw resources, imported program memory, Ghidra databases, and installed-mod payloads are excluded.

Use 7-Zip to open the first `.001` file when an archive has multiple parts. Verify `SHA256SUMS.txt` before extracting.
