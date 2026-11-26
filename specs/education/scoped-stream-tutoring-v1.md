# 分问多意图教学与流式回复

2026-11-23。学生请求“直接给第二问答案，然后开始第三问教学”时，整句共享答案许可导致第三问也被直接解答。默认教学未显式声明其他方式时统一苏格拉底式；学情、难度改变提示深度与长度，不擅自切换答案模式。

## 任务与所有者

Store拥有同学生、同会话、同原题的当前小问与各问已公开答案。原题由现有OCR/题库绑定读取。scope planner读取题干小问和操作句，生成按输入顺序的units(part, intent, teaching)。单句可包含“第2问参考解答”和“第3问苏格拉底引导”，许可只属于对应unit。未知小问澄清，不猜编号；未指定时承接当前小问，首次从第一可用小问开始。题干中的编号和“求”字不是教学方式指令。

每段正文及图示标明第几问；mixed回复以最后一个unit的互动方式结束，继续学习时绑定最后一问。每问使用原Agent工具授权/模型网关/验证，不能因别问给过答案而扩张许可。数学教师仍可先简短解释卡点，再提出一个有价值的推理问题。

## 流式链路

```mermaid
sequenceDiagram
 participant UI as Web草稿投影
 participant HTTP as 已鉴权POST /api/teach (SSE)
 participant Loop as 唯一Agent Loop
 participant Model as 原模型网关
 participant Store as Store事务
 UI->>HTTP: 同一session/request_id + Accept event-stream
 HTTP->>Loop: admission / 原题 / 按小问路由
 Loop-->>UI: scope与阶段（带序号）
 Loop->>Model: 原调用账本 + stream:true
 Model-->>Loop: 提供方真实文本增量 / 工具选择
 Loop-->>UI: 当前unit临时文字增量
 Loop->>Loop: 原有教学与工具校验
 Loop-->>UI: 必要时替换当前draft（修复/压缩不拼接旧文）
 Loop->>Store: 一次提交已接受回复与记忆
 Store-->>UI: done：规范回复与会话投影
```

仅Web采用流式，普通JSON API保留兼容；OCR、内部工具参数与模型推理不发给学生。模型工具调用增量必须完整重组再授权。SSE以UTF-8逐帧解析，错误事件仍映射原错误类型；断流不静默重发模型调用，用同request_id恢复已接受结果。draft由当前UI generation拥有，换会话/清历史后旧结果失效；done才成为持久事实。确定性教师按已生成且核验的小问内容发出段落，不用计时器假造模型打字。

刷新时先恢复同身份的最近会话与原题，再允许发送；仅bootstrap完成不能解除发送锁。浏览器已暴露在会话Detail尚未恢复时发“继续”会创建新会话的时序问题，initializing由同一workspace hook拥有并受generation限制。

## 验收

先维护隔离HTTP与浏览器：截图复现（2解答/3引导）、默认提示、多问标号、不跨问扩权、自然续问承接第3问、未知问号、两问明确答案、否定作用域、原题内指令不变模式；真实SSE增量早于提供方结束，Unicode/公式/分片、工具参数不泄露、错误/断流/重放、图片与草稿保留、generation防旧流、最后事务/无成绩写入。根typecheck、Lint/Hooks、架构、构建与两个正式入口验收。
