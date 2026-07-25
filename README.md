# wot-xvm 重建工程

本目录用于维护已重建的 `s0urce.box.combat.eff.wotmod` 逻辑源码，并从 `s0urce.box.combat.eff.atlas.wotmod` 合并必要资源，重新编译为单个可测试产物。

## 目录结构

- `src/`：重建后的 Python 2.7 源码根目录
- `.build/`：解包、反编译和中间产物
- `original/`：存放原始 `.wotmod` 输入文件
- `tools/`：反编译、编译、打包脚本
- `release/`：最终生成的 `.wotmod`

## 当前状态

- 资源输入插件：`original/s0urce.box.combat.eff.atlas.wotmod`
- 独立输出插件：`release/battle_efficiency_standalone.wotmod`
- 当前包标识：`battle.efficiency.standalone`
- 目标 Python 版本：`2.7`
- 打包格式：ZIP 容器，扩展名为 `.wotmod`

## 两个原插件的关系

原 `s0urce.box.combat.eff.wotmod` 负责 Python 逻辑：获取玩家数据、把效率/胜率拼进玩家名，并向战斗 UI 写入 `badge_XX` 图标名。该逻辑已经重建在 `src/res/scripts/client/gui/mods/*.py` 中，构建最终插件不再需要保留原逻辑 `.wotmod`。两侧玩家面板和玩家头顶名称都复用游戏里的玩家名格式化结果，所以效率文本来自同一段 hook。

`s0urce.box.combat.eff.atlas.wotmod` 负责资源：它提供 `res/gui/flash/atlases/battleAtlas.*` 中的 `badge_10..badge_17`、`badge_20..badge_23` 图标定义，以及 `vehicleMarkerAtlas.*` 车辆标记图集。主插件写入 `isAtlasSource=True` 和 `icon='badge_XX'` 后，游戏客户端需要这些 atlas 资源才能把图标真正画出来。

新的 `battle_efficiency_standalone.wotmod` 会以原 atlas 插件为构建基底，完整保留它的目录项、条目顺序和资源元数据，再追加主插件编译后的 Python 逻辑。包根目录的 `meta.xml` 显式使用独立 ID `battle.efficiency.standalone`，最终文件名和包标识都不再沿用原插件命名。

测试时只加载 `release/battle_efficiency_standalone.wotmod` 这一个新文件，不要再同时加载原来的两个插件。构建脚本会自动删除 `release/` 中使用旧文件名生成的产物，防止资源冲突。

## 典型流程

1. 根据需要修改 `src/res/scripts/client/gui/mods/*.py` 或 `src/meta.xml`。
2. 如需检查资源插件，运行 `tools/decompile_wotmod.py atlas`，会输出 `.build/atlas_manifest.txt` 并解包到 `.build/extracted_atlas/`。
3. 优先双击根目录 `build_release.cmd`，它会强制使用 Python 2.7 编译，并输出 `release/battle_efficiency_standalone.wotmod`。
4. 如果需要命令行执行，请直接运行 `D:\02.registered programs\Python27\python.exe tools\build_release.py`，不要使用裸 `python`，因为当前系统里的 `python` 可能不是可用的 Python 2.7。

## 说明

由于原始逻辑文件仅包含 `.pyc` 字节码，重建源码可能与作者原始工程在注释、局部变量名和排版上不同，但目标是保持行为等价并可维护。`.build/`、`build/` 和 `release/` 都是本地生成目录，不参与提交。
