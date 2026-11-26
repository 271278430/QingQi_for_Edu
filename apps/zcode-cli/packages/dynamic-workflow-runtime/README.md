# @zcode/dynamic-workflow-runtime

沙箱 harness（dynamic workflow 执行引擎的 phase 1.4）。把一份 workflow 脚本在受控子进程里跑起来，
用 NDJSON 把子进程的 `__host.*` 调用桥接到 `@zcode/dynamic-workflow` 的纯引擎核心。

规范：`@zcode/dynamic-workflow/docs/execution-engine.md`（"The sandbox" 与 "The shape of a run:
three boundaries" 里点名本包）。

## 依赖边界

**仅**依赖 `@zcode/dynamic-workflow`（workspace）与 node 内建。**绝不** import `@zcode/core` /
`@zcode/contracts` / `@zcode/bootstrap` / `@zcode/adapters`——本包是 phase 1 "整条 sandbox↔engine
管线 app-free 可跑"的证明。

## 用法

```ts
import { runWorkflowScript } from "@zcode/dynamic-workflow-runtime";

const settlement = await runWorkflowScript({
  scriptText, // 或 lowered: <async 函数体>
  caps: { maxConcurrency: 16 },
  askSpecs, // site id ∈ 合成 schemas 记录即 typed
  validate, // @zcode/dynamic-workflow 的 validate（适配到 ValidateFn）
  makeDriver: (sink) => driver, // driver 自带 journal + emit；sink 是引擎的向上回报面
  signal, // 可选：AbortSignal
  timeoutMs, // 可选：墙钟超时
});
// settlement: { status: "completed", artifact } | { status: "failed", error } | { status: "cancelled" }
```

## 架构

```
┌─ parent (harness) ──────────────┐  NDJSON  ┌─ child (vm.createContext) ──────┐
│ runWorkflowScript               │  stdio   │ 只含 ES intrinsics + __host       │
│  - lower(scriptText)            │◀────────▶│  createActor 同步返回 local 句柄  │
│  - WorkflowEngine(driver,...)   │          │  ask/worldRead → 请求父进程       │
│  - 桥接 __host.* ↔ engine       │          │  args 冻结全局（spawn 时过界一次）  │
│  - spawn/kill/timeout/abort     │          │  Date.now/Math.random 运行期禁令  │
└─────────────────────────────────┘          └──────────────────────────────────┘
```

## NDJSON 线协议

见 `src/protocol.ts`（唯一真源）。child→parent：`create-actor`（即发即忘）/ `request`（ask、
world-read）/ `event`（log）/ `complete`；parent→child：`response`。

## 构建顺序

测试与 typecheck 通过 `@zcode/dynamic-workflow` 的**已构建 dist** 解析依赖，故 `pretest` /
`pretypecheck` 会先 `pnpm --filter @zcode/dynamic-workflow build`。全新检出直接 `pnpm test` 即可，
不会踩到 stale-dist。

## 失败裁决与取舍

- run 的裁决归引擎所有。终结失败（脚本抛错 / 子进程崩溃 / 超时 / 协议损坏）都调
  `engine.fail(error)`——结算 `failed`、driver 侧取消在飞 ask、journal 记 `dwf_run.status =
"failed"` + `failure_json`，journal 与调用方看到的结果一致。abort 信号是唯一的"真取消"，
  调 `engine.cancel()`（结算 `cancelled`，可 resume）。harness 侧的 first-wins finalize 只管
  子进程清理（清 timer、关 stdin、kill child），不自造结算。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow-runtime 基础工程中的 dynamic workflow runtime 模块文件。

### 子目录

| 目录                      | 存放内容                                                            |
| ------------------------- | ------------------------------------------------------------------- |
| [src/](src/README.md)     | @zcode/dynamic-workflow-runtime 基础工程中的 src 实现源码。         |
| [tests/](tests/README.md) | @zcode/dynamic-workflow-runtime 基础工程中的 tests 验收与回归场景。 |

### 文件

| 文件                           | 简要说明                                                   |
| ------------------------------ | ---------------------------------------------------------- |
| [package.json](package.json)   | @zcode/dynamic-workflow-runtime 的包信息、依赖和开发命令。 |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                           |
| [tsconfig.json](tsconfig.json) | 本模块的 TypeScript 编译、类型检查或构建范围。             |

<!-- qingqi-directory-index:end -->
