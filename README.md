# wot-box 独立战绩插件

本项目用于维护一个 World of Tanks 客户端战斗效率显示插件。当前代码会编译为单个 `.wotmod`，用于在战斗 UI 中显示玩家效率和胜率徽章，并集成 `DispersionReticle` 的落弹环功能。

## 目录结构

- `src/res/scripts/client/gui/mods/`：Python 2.7 插件源码
- `src/atlas/res/gui/flash/atlases/`：胜率徽章需要的 atlas 图集资源
- `src/res/gui/flash/DispersionReticleFlash.swf`：落弹环运行所需的 Flash 资源
- `src/meta.xml`：最终 `.wotmod` 的包元数据
- `.build/`：本地编译中间产物
- `tools/`：编译、打包脚本
- `tools/buildlib/`：构建脚本的配置、文件工具、第三方同步、编译与打包模块
- `release/`：最终生成的 `.wotmod`

## 当前状态

- 独立输出插件：`release/battle_efficiency_standalone.wotmod`
- 当前包标识：`battle.efficiency.standalone`
- 当前包版本：`2.1.0`
- 目标 Python 版本：`2.7`
- 打包格式：ZIP 容器，扩展名为 `.wotmod`

## 功能逻辑

- Python 逻辑会在战斗加载时获取玩家数据，并把效率、胜率等文本拼接进玩家显示名称。
- 两侧玩家面板和玩家头顶名称复用游戏里的玩家名格式化结果，因此显示文本来自同一套 hook 逻辑。
- 战斗 UI 徽章通过 `badge_XX` 这类 atlas 条目名渲染，实际图标资源来自 `src/atlas/res/gui/flash/atlases/battleAtlas.*`。
- 构建阶段会同步公开的 `Pruszko/DispersionReticle` MIT 源码，并将其 focused dispersion reticle 逻辑一并打入最终 `.wotmod`。
- `DispersionReticleFlash.swf` 已固定纳入 `src/res/gui/flash/`，不再依赖 `original/` 目录参与构建。
- 车辆标记和小地图相关图标不再由本插件覆盖，保持游戏默认显示效果。

## 打包方式

构建脚本会完成以下工作：

1. 使用 Python 2.7 编译 `src/res/scripts/client/gui/mods/*.py`。
2. 首次构建时自动拉取 `Pruszko/DispersionReticle` 的 `v3.1.3` 公开源码到 `.build/vendor/DispersionReticle/`。
3. 将公开源码映射到 `.build/integrated_src/`，并复制 `src/res/gui/flash/DispersionReticleFlash.swf`。
4. 将 `src/atlas/` 中的徽章 atlas 资源与集成后的脚本、图片、翻译资源一起写入最终 `.wotmod`。
5. 写入 `src/meta.xml` 作为包元数据，并校验 atlas 资源、徽章条目、脚本数量和包元数据。

测试时只加载 `release/battle_efficiency_standalone.wotmod` 这一个文件。

## 典型流程

1. 根据需要修改 `src/res/scripts/client/gui/mods/*.py` 或 `src/meta.xml`。
2. 首次构建需要本机可用 `git` 以拉取公开源码。
3. 优先双击根目录 `build_release.cmd`，它会强制使用 Python 2.7 编译，并输出 `release/battle_efficiency_standalone.wotmod`。
4. 如果需要命令行执行，请直接运行 `D:\02.registered programs\Python27\python.exe tools\build_release.py`，不要使用裸 `python`，因为当前系统里的 `python` 可能不是可用的 Python 2.7。

## 说明

`.build/`、`build/` 和 `release/` 都是本地生成目录，不参与提交。提交源码时应包含 `src/`、`tools/`、`build_release.cmd`、`README.md` 和相关配置文件。
