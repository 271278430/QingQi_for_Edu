# setting

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 setting 实现源码。

### 文件

| 文件                                                                     | 简要说明                                                                        |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| [legacyAccountConnectionSettings.ts](legacyAccountConnectionSettings.ts) | 仅迁移器解释旧键；组织信息由 Host 的只读 OAuth 查询注入。退役旧版后删除。       |
| [normalizeSettingsPatch.ts](normalizeSettingsPatch.ts)                   | locale 现在只表示已解析后的实际语言，localePreference 才表示用户偏好。          |
| [observableSettingService.ts](observableSettingService.ts)               | \* 为 Host 内的设置服务增加提交后通知，不扩大 Setting RPC 契约。                |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                |
| [setting.ts](setting.ts)                                                 | Host 私有装配端口：只读取本机已提交目录，禁止递归读取设置或网络。               |
| [settingService.ts](settingService.ts)                                   | NODE_ENV 来自用户 shell 时会误导服务层 debug 开关；统一使用 ZCODE_RUNTIME_ENV。 |
| [settingsWriteQueue.ts](settingsWriteQueue.ts)                           | 设置写入队列持有真实持久化顺序，Provider 层不 await 也无法释放这里的 pending。  |

<!-- qingqi-directory-index:end -->
