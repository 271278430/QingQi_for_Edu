# adapters

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 adapters 外部能力与平台适配。

### 文件

| 文件                                             | 简要说明                                                                                                         |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| [fsCleaner.ts](fsCleaner.ts)                     | \* 清理执行器：枚举候选（递归 / 非递归两种范围）与有界并发删除。                                                 |
| [fsWalker.ts](fsWalker.ts)                       | \* 数据根遍历器：异步、有界并发、可取消、不跟随符号链接。                                                        |
| [inProcessScanRunner.ts](inProcessScanRunner.ts) | \* 进程内扫描 runner：walker + domain 累加器 + 卷探测。                                                          |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                                                 |
| [rootsResolver.ts](rootsResolver.ts)             | \* 数据根解析：R1 = 家目录下的 .zcode（永远存在），R2 = 自定义数据存储路径下的 .zcode（仅当设置了且 ≠ 家目录）。 |
| [volumeProbe.ts](volumeProbe.ts)                 | \* 卷探测：用 stat().dev 识别物理卷，向上遍历找到挂载点，再 statfs 取容量。                                      |

<!-- qingqi-directory-index:end -->
