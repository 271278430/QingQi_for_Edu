# WebdriverIO 文档镜像说明

`docs/` 是 WebdriverIO 9.x 上游文档的裁剪镜像，与项目当前 9.27.0 主版本一致，但不是完整离线站点：构建生成的 command/API 页面和其他 package 文档未复制，`/docs/...` 路由可能只能在上游网站打开。

项目当前仍使用已被上游弃用的 `wdio-electron-service`；文档中的安装示例只反映镜像来源，升级时应评估迁移到 `@wdio/electron-service`。实际测试配置以 `packages/desktop` 的依赖和配置为准。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

webdriverio 设计与维护文档，属于 docs 目录。

### 子目录

| 目录                    | 存放内容                              |
| ----------------------- | ------------------------------------- |
| [docs/](docs/README.md) | docs 设计与维护文档，属于 docs 目录。 |

### 文件

| 文件                   | 简要说明                         |
| ---------------------- | -------------------------------- |
| [README.md](README.md) | 本目录用途、子目录与逐文件说明。 |

<!-- qingqi-directory-index:end -->
