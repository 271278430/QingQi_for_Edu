# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 scripts 工程脚本。

### 文件

| 文件                                         | 简要说明                                                                                                  |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [build.mjs](build.mjs)                       | Builds the plugin package in the current directory into its dist/. The package declares its               |
| [e2e.mjs](e2e.mjs)                           | \* Real bundled server + official AppBridge host + the panel in an iframe that carries the ZCode          |
| [kind-filter.mjs](kind-filter.mjs)           | \* 格式注册表（src/adapters/parsers.ts、ui/viewers/registry.ts）每种格式一行，行尾标 `// kind:<format>`； |
| [kind-filter.test.mjs](kind-filter.test.mjs) | 回归：Windows 检出的 .ts 是 CRLF，行尾残留 \r 曾让标记匹配失败，单格式插件保留了全部渲染器。              |
| [licenses.mjs](licenses.mjs)                 | \* Collect licences from the modules that actually end up in the bundles, including transitive            |
| [plugin-name.mjs](plugin-name.mjs)           | \* 读取插件根目录 .zcode-plugin/plugin.json 的 name。                                                     |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                                                          |
| [smoke.mjs](smoke.mjs)                       | Run from a built plugin package, or pass its directory. Checks follow the plugin's formats,               |

<!-- qingqi-directory-index:end -->
