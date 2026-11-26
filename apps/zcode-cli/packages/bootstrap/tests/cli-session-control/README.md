# cli-session-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 cli session control 验收与回归场景。

### 文件

| 文件                                       | 简要说明                                                        |
| ------------------------------------------ | --------------------------------------------------------------- |
| [observation.test.ts](observation.test.ts) | observation.test 的实现文件。                                   |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                |
| [runtime-fixture.ts](runtime-fixture.ts)   | 当前调用者可为 yolo；新根必须使用自己的配置，不能继承此模式。   |
| [runtime.test.ts](runtime.test.ts)         | 没有读范围的调用者只看到本进程托管的根。                        |
| [vitest.config.ts](vitest.config.ts)       | 独立验证本 adapter；不加载根应用 setup，也不依赖 CLI 聚合构建。 |

<!-- qingqi-directory-index:end -->
