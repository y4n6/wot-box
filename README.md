# wot-xvm 重建工程

本目录用于从 `s0urce.box.combat.eff.wotmod` 重建可维护源码，并重新编译为可测试产物。

## 目录结构

- `src/`：重建后的 Python 2.7 源码根目录
- `build/`：解包、反编译和中间产物
- `original/`：存放原始 `.wotmod` 输入文件
- `tools/`：反编译、编译、打包脚本
- `release/`：最终生成的 `.wotmod`

## 当前状态

- 原始插件：`original/s0urce.box.combat.eff.wotmod`
- 目标 Python 版本：`2.7`
- 打包格式：ZIP 容器，扩展名为 `.wotmod`

## 典型流程

1. 运行 `tools/decompile_wotmod.py` 解包并重建源码。
2. 根据需要修改 `src/res/scripts/client/gui/mods/*.py`。
3. 优先双击根目录 `build_release.cmd`，它会强制使用 Python 2.7 编译并输出到 `release/`。
4. 如果需要命令行执行，请直接运行 `D:\02.registered programs\Python27\python.exe tools\build_release.py`，不要使用裸 `python`，因为当前系统里的 `python` 可能不是可用的 Python 2.7。

## 说明

由于原始文件仅包含 `.pyc` 字节码，重建源码可能与作者原始工程在注释、局部变量名和排版上不同，但目标是保持行为等价并可维护。
