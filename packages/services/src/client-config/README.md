# client-config

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 client config 实现源码。

### 文件

| 文件                                             | 简要说明                                                             |
| ------------------------------------------------ | -------------------------------------------------------------------- |
| [clientConfig.ts](clientConfig.ts)               | 窗口级公开配置读取。业务模块只消费自己的字段，不拥有第二份请求缓存。 |
| [clientConfigService.ts](clientConfigService.ts) | 只返回已裁剪的配置；不同请求身份不共用快照或在飞请求。               |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                     |

<!-- qingqi-directory-index:end -->
