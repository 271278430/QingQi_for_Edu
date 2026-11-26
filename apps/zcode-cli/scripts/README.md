# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

zcode-cli 基础工程中的 scripts 工程脚本。

### 文件

| 文件                                                                     | 简要说明                                                                                                                        |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| [clean-dist.mjs](clean-dist.mjs)                                         | clean-dist 的实现文件。                                                                                                         |
| [count-ts-lines.mjs](count-ts-lines.mjs)                                 | 实现或公开接口：isTestSourceFile、countLines、isCountedSourceFile、collectTypeScriptFiles。                                     |
| [generate-bash-command-registry.mjs](generate-bash-command-registry.mjs) | 实现或公开接口：BashCommandRegistryOption、BashCommandRegistryNode、BASH_COMMAND_REGISTRY_VERSION、BASH_COMMAND_REGISTRY_HASH。 |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                                                |
| [shadow-replay.mjs](shadow-replay.mjs)                                   | 影子重放对账（交付 / 测试基建）。                                                                                               |

<!-- qingqi-directory-index:end -->
