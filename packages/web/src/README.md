# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 src 实现源码。

### 子目录

| 目录                                                | 存放内容                                              |
| --------------------------------------------------- | ----------------------------------------------------- |
| [auth/](auth/README.md)                             | @zcode/web 基础工程中的 auth 实现源码。               |
| [platform/](platform/README.md)                     | @zcode/web 基础工程中的 platform 实现源码。           |
| [share/](share/README.md)                           | @zcode/web 基础工程中的 share 实现源码。              |
| [share-manage/](share-manage/README.md)             | @zcode/web 基础工程中的 share manage 实现源码。       |
| [web-remote-control/](web-remote-control/README.md) | @zcode/web 基础工程中的 web remote control 实现源码。 |

### 文件

| 文件                               | 简要说明                                                             |
| ---------------------------------- | -------------------------------------------------------------------- |
| [communityUrl.ts](communityUrl.ts) | 服务端拒绝 platform=web；浏览器省略可选平台参数，避免伪装桌面系统。  |
| [env.d.ts](env.d.ts)               | core-js 不带类型声明，polyfills.ts 只做副作用导入。                  |
| [main.tsx](main.tsx)               | 远控 / 分享网页运行在用户自己的浏览器里，版本不受我们控制。          |
| [README.md](README.md)             | 本目录用途、子目录与逐文件说明。                                     |
| [styles.css](styles.css)           | 共享样式只扫描 UI 包；Web 独立入口的状态类也必须参与 Tailwind 生成。 |

<!-- qingqi-directory-index:end -->
