# 教育工作台

产品介绍、截图、教学动画与克隆运行步骤见[仓库README](../README.md)。

本目录是学生产品的主体：个性化辅导、学习路径、学情看板和每次三题的个性化练习。设置管理包含模型连接与单张系统关系图，图中直接展示Agent Loop的决策、调用、观察与返回。

```sh
pnpm education:build
pnpm education:demo
```

演示无需密钥，使用独立合成学生与45道自编数值题。已有真实模型与资料的本机入口继续使用 `education:start` 或 `education:flash`；配置、学生状态、题库和模型权重不随源码上传。

- [运行与数据导入](docs/operations.md)
- [模块职责与系统关系](docs/architecture.md)
- [源码复用边界](docs/reuse.md)
- [维护所有者](docs/ownership.md)
- [当前56组验收与独立真实API检查](docs/verification.md)

`service/src/qingqi`拥有教学与状态；`runtime/src`适配ZCode运行能力；`client/src`提供HTTP/SSE合同；`web/src`只管理交互与草稿；`tools/review_manifest.json`是当前回归入口。历史审查文档保留当时实现，当前行为以`specs/education`和上述维护说明为准。
