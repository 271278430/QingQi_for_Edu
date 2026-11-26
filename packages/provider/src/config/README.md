# config

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/provider 基础工程中的 config 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                           |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [ids.ts](ids.ts)                                   | 实现或公开接口：ProviderId、ProviderTemplateId、ModelId。                                          |
| [index.ts](index.ts)                               | index 的实现文件。                                                                                 |
| [manual-model-config.ts](manual-model-config.ts)   | 手动模式只冻结产品明确开放的叶子；新增系统字段默认不属于个人手动配置。                             |
| [model-config.ts](model-config.ts)                 | 实现或公开接口：EnumOptionSpec、LimitOptionSpec、EnumOptionSpecConfigInput、EnumOptionSpecConfig。 |
| [provider-config.ts](provider-config.ts)           | 实现或公开接口：ProviderApiType、ProviderGroup、ZhipuAccountMode、ApiKeyAccessConfigInput。        |
| [provider-data-schema.ts](provider-data-schema.ts) | 加速卡访问类别；与 zcodeProviderAccountAccessSchema.mode 同值，改动需同步两处。                    |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                   |
| [rule-data-schema.ts](rule-data-schema.ts)         | 不能通过最后一次覆盖掩盖矛盾模式；身份用元组编码，避免模型 ID 自带分隔符碰撞。                     |
| [schema-validation.ts](schema-validation.ts)       | 翻译已有问题协议，不维护另一份字段或内容校验清单。                                                 |
| [schema.ts](schema.ts)                             | Account 运行时事实仍只有成员及权益；不是磁盘配置规则的第二种格式。                                 |

<!-- qingqi-directory-index:end -->
