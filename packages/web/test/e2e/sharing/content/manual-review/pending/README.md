# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 pending 测试场景。

### 文件

| 文件                                             | 简要说明                                                                         |
| ------------------------------------------------ | -------------------------------------------------------------------------------- |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                 |
| [share-content.mjs](share-content.mjs)           | SHARE-WF02：fixture 只拦截网络，不访问真实账号、分享或模型。                     |
| [share-input-images.mjs](share-input-images.mjs) | SHARE-IMG01：本地网络 fixture，验证匿名分享页的输入图片及加载失败回退。          |
| [share-manage.mjs](share-manage.mjs)             | SHARE-MG01：先启动 pnpm dev:web-share:mock，再运行本文件；仅使用开发态 fixture。 |
| [share-not-found.mjs](share-not-found.mjs)       | SHARE-NF01：先启动 pnpm dev:web-share:mock，再运行本文件；仅使用开发态 fixture。 |

<!-- qingqi-directory-index:end -->
