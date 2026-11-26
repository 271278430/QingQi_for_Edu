# graphs

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 graphs 验收与回归场景。

### 子目录

| 目录                            | 存放内容                                                       |
| ------------------------------- | -------------------------------------------------------------- |
| [expected/](expected/README.md) | @zcode/dynamic-workflow 基础工程中的 expected 验收与回归场景。 |

### 文件

| 文件                                                                                                 | 简要说明                                                                                          |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [actor-agent-to-workspace.ts](actor-agent-to-workspace.ts)                                           | An agent's output becomes a file PATH (flows into a files.read argument), and the                 |
| [actor-dead-code-after-return.ts](actor-dead-code-after-return.ts)                                   | Asks that are dead code AFTER the top-level return. Analysis is flow-insensitive (no              |
| [actor-may-pick-inside-fanout.ts](actor-may-pick-inside-fanout.ts)                                   | Composes may-projection + fan-out containment + aggregation in one shape: a ternary               |
| [actor-nested-inline-fanout-family.ts](actor-nested-inline-fanout-family.ts)                         | Nested INLINE fan-outs: agent created inside the inner map (which is inside the                   |
| [actor-nonsingleton-lane-computed.ts](actor-nonsingleton-lane-computed.ts)                           | An array of agents indexed by a COMPUTED index widens the receiver actor set to                   |
| [actor-or-aggregation-and-context-dissolve.ts](actor-or-aggregation-and-context-dissolve.ts)         | Aggregation rules in one shape: seed feeds a two-actor pick (inexact, {a,b}) AND                  |
| [actor-relay-chain-connectivity.ts](actor-relay-chain-connectivity.ts)                               | An ask-produced collection routed through BOTH a fan-out and a join before reaching               |
| [agent-array-indexed-selection.ts](agent-array-indexed-selection.ts)                                 | Agents stored in an array, selected by a static vs a computed index on the ask                    |
| [alias-write.ts](alias-write.ts)                                                                     | Aliasing store (heap fix): `alias` and `box` are the SAME object, so a write through              |
| [all-catch.ts](all-catch.ts)                                                                         | .catch on a real Promise (Promise.all returns Promise<string[]>). Runtime: if any                 |
| [array-from-mapper.ts](array-from-mapper.ts)                                                         | Array.from(xs, mapper): a per-element callback per the registry (`each`, iterated = arg 0,        |
| [array-push-all.ts](array-push-all.ts)                                                               | Heap mutator (Array.push) accumulating Nodes into an array, then a NON-literal                    |
| [array-spread-shared.ts](array-spread-shared.ts)                                                     | Sole-element array spread `[...arr1]` shallow-copies: `arr2[0] === arr1[0]` (shared               |
| [async-promise-allsettled-value.ts](async-promise-allsettled-value.ts)                               | Promise.allSettled: field-sensitive access through the settled records                            |
| [async-promise-custom-thenable.ts](async-promise-custom-thenable.ts)                                 | Custom thenable: `await thenable` invokes its then() method, which forwards the                   |
| [async-promise-double-await-mutate.ts](async-promise-double-await-mutate.ts)                         | Double await of one Node: both awaits settle to the SAME object at runtime, so a                  |
| [async-promise-executor-launder.ts](async-promise-executor-launder.ts)                               | Promise executor laundering: the value passed to resolve() IS the awaited value.                  |
| [async-promise-executor-reject-param.ts](async-promise-executor-reject-param.ts)                     | Executor reject param: `new Promise((_, reject) => reject(secret))`. The generic                  |
| [async-promise-for-await-of.ts](async-promise-for-await-of.ts)                                       | for await...of over an array of Nodes: the loop variable is the awaited element.                  |
| [async-promise-join-in-ternary.ts](async-promise-join-in-ternary.ts)                                 | A join under a conditional PLACE: both arms are `Promise.all` calls, so the ternary               |
| [async-promise-nested-join-destructure.ts](async-promise-nested-join-destructure.ts)                 | Nested joins: an outer `Promise.all` whose ELEMENTS are themselves `Promise.all`                  |
| [async-promise-node-field-alias-await.ts](async-promise-node-field-alias-await.ts)                   | A Node<T> stored in an object field after creation, awaited later through a                       |
| [async-promise-race-any.ts](async-promise-race-any.ts)                                               | Promise.race / Promise.any are NOT join-listed: they must fall to the                             |
| [async-promise-reject-try-catch.ts](async-promise-reject-try-catch.ts)                               | Rejected promise awaited in a try: `await failure` THROWS the rejection reason                    |
| [async-promise-then-both-callbacks.ts](async-promise-then-both-callbacks.ts)                         | .then with BOTH callbacks plus a .finally in the chain: either callback's ask                     |
| [async-promise-then-destructured-param.ts](async-promise-then-destructured-param.ts)                 | .then callback with a DESTRUCTURED parameter over a join result: at runtime                       |
| [callback-array-from-length.ts](callback-array-from-length.ts)                                       | Callback invocation family (docs/analysis.md), the motivating                                     |
| [callback-array-from-phased.ts](callback-array-from-phased.ts)                                       | Callback invocation family: `Array.from(xs, fn)` with an inline mapper inside a phase, next       |
| [callback-dead-function-sweep.ts](callback-dead-function-sweep.ts)                                   | Callback invocation family: the sweep's remaining job. `unused` is never applied by any           |
| [callback-multi-target-dispatch.ts](callback-multi-target-dispatch.ts)                               | Callback invocation family: an indirect dispatch that may reach EITHER of two script              |
| [callback-named-map-phased.ts](callback-named-map-phased.ts)                                         | Callback invocation family: a NAMED callback to `.map` inside a phase. The value-based            |
| [callback-promise-executor.ts](callback-promise-executor.ts)                                         | Callback invocation family: a `new Promise(executor)` whose executor issues an ask. The           |
| [callback-then-in-phase.ts](callback-then-in-phase.ts)                                               | Callback invocation family: a `.then` continuation registered inside a phase. Once-deferred       |
| [callback-through-param.ts](callback-through-param.ts)                                               | Callback invocation family: a callback handed to a helper and invoked through the helper's        |
| [chained-assign.ts](chained-assign.ts)                                                               | Chained assignment `x = y = t` taints BOTH targets (nested EqualsToken). Positive                 |
| [circular-ref.ts](circular-ref.ts)                                                                   | Circular reference (divergence-crash fix): a self-referential object (`a.self = a`)               |
| [class-extends-method.ts](class-extends-method.ts)                                                   | A derived class with no constructor inherits the base constructor (implicit super                 |
| [class-field-initializer-ask.ts](class-field-initializer-ask.ts)                                     | A facade call inside a class field initializer must be evaluated (the initializer runs            |
| [class-field-method.ts](class-field-method.ts)                                                       | A class instance carries taint through a constructor-stored field returned by a                   |
| [class-getter-taint.ts](class-getter-taint.ts)                                                       | A getter returns this.field; reading the getter (modeled as a field whose value is the            |
| [class-static-block-ask.ts](class-static-block-ask.ts)                                               | A facade call inside a static block runs at class initialization. Static and instance             |
| [class-this-write-method.ts](class-this-write-method.ts)                                             | A method writes its argument into this.field; a second method reads it back. The write            |
| [classes-2-class-accessors.ts](classes-2-class-accessors.ts)                                         | Class-declared accessors with DIFFERENT names (so the raw field write cannot mask the             |
| [classes-2-class-alias-ctor-effect.ts](classes-2-class-alias-ctor-effect.ts)                         | A class aliased through a plain variable (`const Alias = Cfg`) and new'd through the              |
| [classes-2-class-expr-in-field.ts](classes-2-class-expr-in-field.ts)                                 | A class EXPRESSION stored in an object field and new'd through box.C. Runtime:                    |
| [classes-2-computed-method-name.ts](classes-2-computed-method-name.ts)                               | A method declared with a COMPUTED name (["run"]) but called through the plain static              |
| [classes-2-cross-instance-conflation.ts](classes-2-cross-instance-conflation.ts)                     | Cross-instance conflation (sound-by-design over-approximation, per spec residual 6):              |
| [classes-2-extends-mixin-call.ts](classes-2-extends-mixin-call.ts)                                   | A class extending a mixin CALL (`class D extends mix(Base) {}`). D itself resolves,               |
| [classes-2-extracted-method-bare-call.ts](classes-2-extracted-method-bare-call.ts)                   | A method extracted off an instance and called BARE (const m = r.run; m("go")). The                |
| [classes-2-new-in-fanout.ts](classes-2-new-in-fanout.ts)                                             | `new` inside a fan-out body: one Judge instance per element, all conflated into the               |
| [classes-2-param-property.ts](classes-2-param-property.ts)                                           | A constructor PARAMETER PROPERTY (`constructor(private x: string) {}`) performs an                |
| [classes-2-private-field.ts](classes-2-private-field.ts)                                             | A #private field carries taint: put() writes this.#x, take() reads it back.                       |
| [classes-2-static-method-static-field.ts](classes-2-static-method-static-field.ts)                   | A static method called via the class name asks with a static field (read through                  |
| [classes-2-super-method-arg.ts](classes-2-super-method-arg.ts)                                       | A derived method (different name from the base method) forwards its argument to                   |
| [classes-2-super-method-return.ts](classes-2-super-method-return.ts)                                 | A derived method (under a DIFFERENT name, so merged-field dispatch cannot mask it)                |
| [compound-assign-loop.ts](compound-assign-loop.ts)                                                   | Realistic idiom: accumulate a report string across a loop of asks with `+=`, then                 |
| [compound-assign.ts](compound-assign.ts)                                                             | Compound assignment: `report += a` must write a's taint back into report so the                   |
| [computed-callee.ts](computed-callee.ts)                                                             | A callee selected by a COMPUTED index (`fns[i]`) must still dispatch to the tracked               |
| [computed-index.ts](computed-index.ts)                                                               | Computed (dynamic) index access is THE widening rule: reading `items[i]` with a                   |
| [conditional-receiver-may-set.ts](conditional-receiver-may-set.ts)                                   | Conditional receiver: `(flag ? a : b).ask(...)` — the receiver resolves to a MAY                  |
| [context-sharing.ts](context-sharing.ts)                                                             | The context relation. `shared` is one actor asked at two sites -> a context edge                  |
| [control-flow-comma-alias-write.ts](control-flow-comma-alias-write.ts)                               | The comma (sequence) operator yields its RIGHT operand at runtime, so                             |
| [control-flow-comma-incrementor.ts](control-flow-comma-incrementor.ts)                               | Comma expression as the for-incrementor: the second operand's compound                            |
| [control-flow-do-while-self-loop.ts](control-flow-do-while-self-loop.ts)                             | do-while: loop-carried draft feeds the SAME ask's instructions next round.                        |
| [control-flow-for-await.ts](control-flow-for-await.ts)                                               | for await...of over an array of Nodes: elements carry both asks' labels.                          |
| [control-flow-forin-key-taint.ts](control-flow-forin-key-taint.ts)                                   | for-in over a tainted object's keys: the key strings ARE derived from the                         |
| [control-flow-forof-assign-form.ts](control-flow-forof-assign-form.ts)                               | for...of with an ASSIGNMENT-form initializer (pre-declared variable, no                           |
| [control-flow-if-no-else-skip.ts](control-flow-if-no-else-skip.ts)                                   | A skippable choice vs an exhaustive one. The first `if` has no else, so its head has a            |
| [control-flow-in-operator.ts](control-flow-in-operator.ts)                                           | `in` operator over a tainted operand: the boolean depends on the ask's keys.                      |
| [control-flow-labeled-break-nested.ts](control-flow-labeled-break-nested.ts)                         | Labeled break out of nested loops carrying taint into a post-loop read.                           |
| [control-flow-loop-condition-step.ts](control-flow-loop-condition-step.ts)                           | KNOWN APPROXIMATION (docs/analysis.md, "The control-flow graph"): the walk                        |
| [control-flow-optional-calls.ts](control-flow-optional-calls.ts)                                     | Optional calls on facade functions: `planner.ask?.()`, `planner?.ask()`,                          |
| [control-flow-optional-chain-read.ts](control-flow-optional-chain-read.ts)                           | Optional-chaining reads (d?.core.text) off a nullable ask result must flow.                       |
| [control-flow-optional-fn-call.ts](control-flow-optional-fn-call.ts)                                 | Optional call on a maybe-undefined script-local function: when defined at                         |
| [control-flow-recursive-helper.ts](control-flow-recursive-helper.ts)                                 | A recursive helper: the SCC is a `loop` region in the trace, and the re-entrant call is a         |
| [control-flow-return-in-fanout-callback.ts](control-flow-return-in-fanout-callback.ts)               | A `return` inside a fan-out callback ends THAT element's iteration: it targets the fanout         |
| [control-flow-return-in-helper.ts](control-flow-return-in-helper.ts)                                 | A `return` inside a helper targets the helper's `call` region, not the script's root: the         |
| [control-flow-shadowed-names.ts](control-flow-shadowed-names.ts)                                     | Two distinct symbols named x: the inner (tainted) one must flow out via out,                      |
| [control-flow-switch-fallthrough.ts](control-flow-switch-fallthrough.ts)                             | switch fallthrough + default: taint reaches msg through every clause shape.                       |
| [control-flow-throw-in-catch.ts](control-flow-throw-in-catch.ts)                                     | A `throw` inside a catch block does not land back in the same try: `catch` is a sibling of        |
| [control-flow-try-finally-return.ts](control-flow-try-finally-return.ts)                             | try/finally where the FINALLY return wins at runtime and carries the taint.                       |
| [curry.ts](curry.ts)                                                                                 | Positive coverage: a returned closure capturing the outer curry parameter plus its                |
| [cyclic-nodes-through-fanout-map.ts](cyclic-nodes-through-fanout-map.ts)                             | Cyclic linked-list nodes iterated by .map; the callback writes a tainted field and                |
| [default-param.ts](default-param.ts)                                                                 | Default parameter initializer referencing tainted outer state must be evaluated:                  |
| [destructure-alias.ts](destructure-alias.ts)                                                         | Destructuring aliasing (heap fix): a destructuring declaration off a live place binds             |
| [destructuring-assign.ts](destructuring-assign.ts)                                                   | Destructuring assignment expressions (not declarations) must bind their targets:                  |
| [element-field-write.ts](element-field-write.ts)                                                     | Element-field write (heap fix): a tainted field written through an element-access                 |
| [emission-graph-computed-elem-read-ask.ts](emission-graph-computed-elem-read-ask.ts)                 | A facade ask in the KEY position of an element-access READ (`o[<ask>]`). Runtime: ask#1's         |
| [emission-graph-computed-elem-write-key-taint.ts](emission-graph-computed-elem-write-key-taint.ts)   | A facade ask in the KEY position of an element-access WRITE (`o[<ask>] = v`). Runtime: ask#2's    |
| [emission-graph-computed-key-ask.ts](emission-graph-computed-key-ask.ts)                             | A facade ask in a COMPUTED PROPERTY NAME position. Runtime: ask#1's output (s) is                 |
| [emission-graph-computed-method-name-obj.ts](emission-graph-computed-method-name-obj.ts)             | A facade ask in a COMPUTED METHOD NAME of an object literal (`{ [<ask>]() {…} }`). Runtime:       |
| [emission-graph-conditional-condition-ask.ts](emission-graph-conditional-condition-ask.ts)           | A facade ask in the CONDITION position of a conditional expression. Runtime: ask#1's              |
| [emission-graph-dedupe-exact-or.ts](emission-graph-dedupe-exact-or.ts)                               | One edge, two witnesses: `a` reaches ask#2 directly (exact) AND through a                         |
| [emission-graph-empty-join-into-ask.ts](emission-graph-empty-join-into-ask.ts)                       | Promise.all([]) — a join with NO inputs — consumed by an ask. The join carries its                |
| [emission-graph-fanout-map-wrap-aggregate.ts](emission-graph-fanout-map-wrap-aggregate.ts)           | Root cause 8, integration: a two-stage fan-out where the second stage's per-item map              |
| [emission-graph-fanout-ordinal-skip.ts](emission-graph-fanout-ordinal-skip.ts)                       | Fan-out ordinal stability: the FIRST iteration candidate (.map with no facade sites               |
| [emission-graph-join-destructure-element-write.ts](emission-graph-join-destructure-element-write.ts) | Destructure a Promise.all result, then WRITE through one destructured element.                    |
| [emission-graph-join-in-object-literal.ts](emission-graph-join-in-object-literal.ts)                 | Two joins grouped in ONE object literal, their results read downstream. Regression guard          |
| [emission-graph-join-index-write-original.ts](emission-graph-join-index-write-original.ts)           | Write through a static index of a BOUND Promise.all result, read back through the                 |
| [emission-graph-join-shorthand-wrapped-element.ts](emission-graph-join-shorthand-wrapped-element.ts) | Root cause 8: an async map callback wraps its awaited ask in a SHORTHAND object literal           |
| [emission-graph-may-receiver-overlap-context.ts](emission-graph-may-receiver-overlap-context.ts)     | Context edges over MAY-set receivers: ask#2 runs on {alpha,beta}, ask#3 on                        |
| [emission-graph-port-subsumption.ts](emission-graph-port-subsumption.ts)                             | Port subsumption at one sink: element 0 of a join result AND the whole tuple both                 |
| [emission-graph-return-shorthand-object.ts](emission-graph-return-shorthand-object.ts)               | Root cause 8: a tainted value wrapped in a SHORTHAND object-literal property at the               |
| [emission-graph-same-actor-self-edge.ts](emission-graph-same-actor-self-edge.ts)                     | One actor, three asks; data flows from ask#1 into ask#2 only. Expected: actor-graph               |
| [emission-graph-untracked-join-pruned.ts](emission-graph-untracked-join-pruned.ts)                   | A Promise.all over untracked string literals whose result is DISCARDED: the join                  |
| [emission-graph-workspace-aggregation.ts](emission-graph-workspace-aggregation.ts)                   | Two distinct world-read sites feeding one ask: the actor projection must aggregate                |
| [emission-graph-worldread-return-only.ts](emission-graph-worldread-return-only.ts)                   | Agent-relevance filter: a world read flowing straight into the script result, no                  |
| [extracted-alias.ts](extracted-alias.ts)                                                             | Extracted-alias (heap fix): a sub-object pulled out of a container by an aliasing                 |
| [facade-siting-optional-chain.ts](facade-siting-optional-chain.ts)                                   | Optional-chain call forms should still SITE (the callee is a PropertyAccess with a                |
| [facade-siting-pick-receiver.ts](facade-siting-pick-receiver.ts)                                     | Boundary probe: `Pick<Agent, "ask">` is a mapped type over the FACADE interface, so its           |
| [facade-siting-spread-receiver.ts](facade-siting-spread-receiver.ts)                                 | Boundary probe: `{ ...planner }` — at runtime spreads the agent's own enumerable props            |
| [fanout-over-join.ts](fanout-over-join.ts)                                                           | Two relay stages composed: a fan-out feeds a join whose result feeds a second                     |
| [files-read.ts](files-read.ts)                                                                       | A files.read world-input source feeding one ask.                                                  |
| [flatmap-inline-two-asks.ts](flatmap-inline-two-asks.ts)                                             | flatMap with an inline callback returning an array literal of two asks per element.               |
| [functions-summaries-apply-shift.ts](functions-summaries-apply-shift.ts)                             | f.apply(null, [secret]): runtime binds x = secret, which flows into ask#2.                        |
| [functions-summaries-arguments-object.ts](functions-summaries-arguments-object.ts)                   | The `arguments` object: f(secret) binds arguments[0] = secret at runtime, which                   |
| [functions-summaries-bind-merge-alignment.ts](functions-summaries-bind-merge-alignment.ts)           | Merge-trap regression for the bind prefix (RC4, round-3 addendum). `h` is a union of a            |
| [functions-summaries-bind-partial.ts](functions-summaries-bind-partial.ts)                           | g = f.bind(null, secret); g() — at runtime g() is f(secret): secret flows into                    |
| [functions-summaries-bind-self-rebind.ts](functions-summaries-bind-self-rebind.ts)                   | Self-rebinding a function value: `h = h.bind(null, "x")` appends one element to h's bind          |
| [functions-summaries-call-shift.ts](functions-summaries-call-shift.ts)                               | f.call(null, secret): at runtime f's param x IS secret and flows into ask#2.                      |
| [functions-summaries-closure-reassigned.ts](functions-summaries-closure-reassigned.ts)               | A closure captures `topic`, which is reassigned to a tainted value AFTER the                      |
| [functions-summaries-curry-call.ts](functions-summaries-curry-call.ts)                               | Curry + .call: g = make(topic) returns an arrow capturing make's param a; then                    |
| [functions-summaries-default-param-earlier.ts](functions-summaries-default-param-earlier.ts)         | Default parameter referencing an EARLIER parameter: f(secret) leaves b to default                 |
| [functions-summaries-fn-through-param.ts](functions-summaries-fn-through-param.ts)                   | A script-local function passed as an argument to another script-local function and                |
| [functions-summaries-iife.ts](functions-summaries-iife.ts)                                           | IIFE: an inline arrow invoked immediately with a tainted actual. The parenthesized                |
| [functions-summaries-mutual-recursion.ts](functions-summaries-mutual-recursion.ts)                   | Mutual recursion: taint enters even(), threads through odd() and back, and exits                  |
| [functions-summaries-reflect-apply.ts](functions-summaries-reflect-apply.ts)                         | Reflect.apply(f, null, [secret]): the same runtime dispatch as f.apply, but here f                |
| [functions-summaries-rest-call.ts](functions-summaries-rest-call.ts)                                 | .call on a function whose ONLY formal is a rest parameter: the rest placeholder                   |
| [functions-summaries-spread-actuals.ts](functions-summaries-spread-actuals.ts)                       | Spread actual over a tracked tuple: f(...pair) runs f("clean", secret) — b IS                     |
| [game-planner-reviewer.ts](game-planner-reviewer.ts)                                                 | Planner-Reviewer 工作流: 为 3D HTML 小游戏生成经过评审的开发计划                                  |
| [generator-forof.ts](generator-forof.ts)                                                             | Generator yields tainted values, consumed by for...of. The yielded operand must                   |
| [getter-field.ts](getter-field.ts)                                                                   | Object-literal getter: reading `.val` invokes the getter, whose return summary                    |
| [git-world-reads.ts](git-world-reads.ts)                                                             | git.\* world reads feeding one ask: four source nodes, one sink. The point of this                |
| [glob-fanout.ts](glob-fanout.ts)                                                                     | glob-fanout 的实现文件。                                                                          |
| [grep-fanout.ts](grep-fanout.ts)                                                                     | grep result fanned out over asks: the world-read site is a source node and each ask               |
| [handoff-earth-v5.ts](handoff-earth-v5.ts)                                                           | Hand-off graph acceptance sample (docs/dynamic-workflow/presentation.md「The display contract」): |
| [handoff-family-self-carry.ts](handoff-family-self-carry.ts)                                         | 交接图：fan-out 里的 ask 带 carry 自环（`Promise.all(map(async …))` 的包装对象让它按串行          |
| [handoff-family-to-family.ts](handoff-family-to-family.ts)                                           | Two literal fan-outs in one script, the second consuming the first's results. The                 |
| [handoff-literal-members.ts](handoff-literal-members.ts)                                             | Literal-length fan-out → one participant card per member (member=i/3), and a                      |
| [handoff-mayset-two-cards.ts](handoff-mayset-two-cards.ts)                                           | A dynamically selected receiver inside a phase: the may-set copies land on two cards              |
| [handoff-pushed-array-many.ts](handoff-pushed-array-many.ts)                                         | A const array literal that is later `push`ed is NOT a literal length: the analyzer must           |
| [handoff-unphased-baton.ts](handoff-unphased-baton.ts)                                               | No phase markers: every participant sits in the one implicit `unphased` phase. A                  |
| [heap-aliasing-chained-ternary-alias-write.ts](heap-aliasing-chained-ternary-alias-write.ts)         | Chained conditional alias: `d` may be `a`, and `a` may be `b` or `c`, so at runtime               |
| [heap-aliasing-cyclic-self.ts](heap-aliasing-cyclic-self.ts)                                         | Cyclic structure: `a.self = a` makes the abstract value genuinely cyclic. The                     |
| [heap-aliasing-delete-survives.ts](heap-aliasing-delete-survives.ts)                                 | `delete` is gen-only: no kill. On the non-deleting path box.f still carries                       |
| [heap-aliasing-depth-cap.ts](heap-aliasing-depth-cap.ts)                                             | Field chain 10 deep — beyond VALUE_DEPTH_CAP=8. The write lands at the leaf of                    |
| [heap-aliasing-index-assign-adopt.ts](heap-aliasing-index-assign-adopt.ts)                           | Alias established through a container-field ASSIGNMENT (not a literal element):                   |
| [heap-aliasing-late-alias-loop.ts](heap-aliasing-late-alias-loop.ts)                                 | Late alias: the aliasing assignment `wrap.box = box` sits AFTER the write in                      |
| [heap-aliasing-literal-capture-mutate.ts](heap-aliasing-literal-capture-mutate.ts)                   | An object literal captures a live place; mutation THROUGH the literal's field                     |
| [heap-aliasing-map-agent-context.ts](heap-aliasing-map-agent-context.ts)                             | Actor label through a Map: both asks run on the SAME actor at runtime (the map                    |
| [heap-aliasing-map-roundtrip.ts](heap-aliasing-map-roundtrip.ts)                                     | Map.get after Map.set of a tracked box, with the taint written AFTER the set:                     |
| [heap-aliasing-nested-ternary-alias-write.ts](heap-aliasing-nested-ternary-alias-write.ts)           | SYNTACTICALLY nested conditional place: the inner ternary is an ARM of the outer one,             |
| [heap-aliasing-param-literal-wrap.ts](heap-aliasing-param-literal-wrap.ts)                           | The callee writes through a SUB-OBJECT of its parameter; the caller's argument is                 |
| [heap-aliasing-ternary-alias-write.ts](heap-aliasing-ternary-alias-write.ts)                         | Conditional alias: `a = flag ? box1 : box2` — at runtime `a` IS one of the two                    |
| [heap-aliasing-ternary-condition-ask.ts](heap-aliasing-ternary-condition-ask.ts)                     | The CONDITION of a ternary is a real expression: the judge ask inside it reads                    |
| [heap-aliasing-two-names-push-join.ts](heap-aliasing-two-names-push-join.ts)                         | Two names for one array: the ask is pushed through `ys`, the join reads `xs`.                     |
| [heap-literal-arg-writeback.ts](heap-literal-arg-writeback.ts)                                       | The callee writes a NEW field on its parameter and hands the object back; the caller's            |
| [heap-weak-update.ts](heap-weak-update.ts)                                                           | for...of pushing ask results into an outer array (a weak heap update), the array                  |
| [helper-flow-through.ts](helper-flow-through.ts)                                                     | Context-sensitive returns: `relay` returns its argument. Called with two distinct                 |
| [helper-recursive.ts](helper-recursive.ts)                                                           | Self-recursive helper carrying a tracked value down to a base-case ask. The                       |
| [higher-order.ts](higher-order.ts)                                                                   | Higher-order dispatch: `f` is dynamically one of two functions. The call resolves                 |
| [hole-filled-no-phases.ts](hole-filled-no-phases.ts)                                                 | A filled hole without markers: the hole's own phase holds the fill's ask (`<hole id>/ask#1`),     |
| [hole-filled-two-phases.ts](hole-filled-two-phases.ts)                                               | A filled hole whose body opens with a marker: the hole's own phase claims no step, yet it         |
| [hole-in-for-of.ts](hole-in-for-of.ts)                                                               | A hole inside a for...of body. The interpreter reads for...of as an iteration candidate, and      |
| [hole-in-helper.ts](hole-in-helper.ts)                                                               | A hole in a helper called twice: one site, two issues (like any helper ask), one phase. The       |
| [hole-in-loop.ts](hole-in-loop.ts)                                                                   | A hole in a plain `for` loop (hole-in-for-of covers the for...of form): one step,                 |
| [hole-nested-filled.ts](hole-nested-filled.ts)                                                       | Both holes filled: the outer fill wrote `<outer>/…`, the inner fill wrote `<inner>/…` (one        |
| [hole-nested.ts](hole-nested.ts)                                                                     | A hole inside a fill: the inner one is open and keyed by its own name like any hole (no outer     |
| [hole-open-mid-script.ts](hole-open-mid-script.ts)                                                   | An open hole between two phases (docs/analysis.md, "Sites", Hole sites): a step of kind           |
| [hole-tail.ts](hole-tail.ts)                                                                         | The tail form `return await hole<T>(...)`: the script's end is open. The site carries `tail`,     |
| [interpolated-actor-name.ts](interpolated-actor-name.ts)                                             | Actor names the script INTERPOLATES: `agent()` gets a template literal, so the                    |
| [iterated-object-method-call.ts](iterated-object-method-call.ts)                                     | A method stored on an object that is ITERATED by a fan-out callback stays reachable:              |
| [iteration-fanout-callback-array-param.ts](iteration-fanout-callback-array-param.ts)                 | The THIRD callback parameter of map is the whole iterated array: at runtime                       |
| [iteration-fanout-destructured-element-param.ts](iteration-fanout-destructured-element-param.ts)     | map with a DESTRUCTURED element parameter ({ q }): at runtime q is element.q,                     |
| [iteration-fanout-element-mutation.ts](iteration-fanout-element-mutation.ts)                         | Element mutation through the iteration binding. At runtime the forEach callback                   |
| [iteration-fanout-empty-body-no-promote.ts](iteration-fanout-empty-body-no-promote.ts)               | EMPTY-body candidates over tracked data: neither the forEach with an empty inline                 |
| [iteration-fanout-foreach-push-join.ts](iteration-fanout-foreach-push-join.ts)                       | forEach writing un-awaited asks into an OUTER array via closure, then Promise.all                 |
| [iteration-fanout-forof-entries.ts](iteration-fanout-forof-entries.ts)                               | for...of over .entries() of a tainted array, destructured [i, v]: entries() is an                 |
| [iteration-fanout-generator-of-asks.ts](iteration-fanout-generator-of-asks.ts)                       | A generator yielding ASK NODES (not strings), consumed by for...of whose body only                |
| [iteration-fanout-join-in-object-literal.ts](iteration-fanout-join-in-object-literal.ts)             | The structural blast radius of emission-graph-join-in-object-literal, one level up: a             |
| [iteration-fanout-reduce-no-initial.ts](iteration-fanout-reduce-no-initial.ts)                       | reduce WITHOUT an initial value: at runtime the accumulator starts as parts[0]                    |
| [iteration-fanout-reduce-seed-mutation.ts](iteration-fanout-reduce-seed-mutation.ts)                 | reduce with an OBJECT accumulator mutated in place: at runtime the accumulator IS                 |
| [iteration-fanout-unknown-chain.ts](iteration-fanout-unknown-chain.ts)                               | Unknown array calls in a chain before a fan-out: .flat() on a nested tracked array                |
| [iteration-fanout-while-shift.ts](iteration-fanout-while-shift.ts)                                   | while-loop consuming a tracked array with .shift(): shift is an unknown call, so                  |
| [join-array-literal.ts](join-array-literal.ts)                                                       | Promise.all over a static array literal of asks — a join site whose argument                      |
| [join-conditional-element-write-through.ts](join-conditional-element-write-through.ts)               | A conditional PLACE as an element of a join's array literal. The join element's                   |
| [join-element-alias-write-through.ts](join-element-alias-write-through.ts)                           | Alias an element of a Promise.all result and write a NEW field through the alias, then            |
| [join-ports.ts](join-ports.ts)                                                                       | Promise.all over a static array literal: element positions become ports. One                      |
| [json-roundtrip-clone.ts](json-roundtrip-clone.ts)                                                   | JSON deep-clone round-trip. At runtime clone.f === secret, and the reader ask                     |
| [json-roundtrip-sound.ts](json-roundtrip-sound.ts)                                                   | serialize/parse round-trip must preserve taint: JSON.stringify collapses the                      |
| [linear-chain.ts](linear-chain.ts)                                                                   | A straight artifact chain: each ask consumes the previous one's result.                           |
| [map-set.ts](map-set.ts)                                                                             | Library mutator Map.set (heap fix): `m.set(k, secret)` folds secret into the map's                |
| [may-set-branch-form-parity.ts](may-set-branch-form-parity.ts)                                       | The BRANCH form of `may-set-oneshot-ternary`: `cond ? a.ask(p) : b.ask(p)` where that             |
| [may-set-fifo-against-fixed-lane.ts](may-set-fifo-against-fixed-lane.ts)                             | A may-set step that MAY share a mailbox with a fixed-lane step: `(f ? a : b).ask(…)`              |
| [may-set-loop-alternating-receiver.ts](may-set-loop-alternating-receiver.ts)                         | An alternating receiver in a loop: the script's ONLY ask site is                                  |
| [may-set-oneshot-ternary.ts](may-set-oneshot-ternary.ts)                                             | A one-shot ternary receiver at the top level: nothing guards the ask, so the source               |
| [may-set-over-cap.ts](may-set-over-cap.ts)                                                           | A may-set past the expansion cap: an array of FIVE agents indexed by a computed index             |
| [method-shorthand.ts](method-shorthand.ts)                                                           | Object-literal shorthand method: `obj.run(s)` must bind s to the method's param                   |
| [named-callback-map.ts](named-callback-map.ts)                                                       | Named callback passed to .map. A fan-out candidate like an inline arrow (candidates are           |
| [nested-fanout-reach.ts](nested-fanout-reach.ts)                                                     | Reachability across nested regions (fix #2). `deepen` asks; `viaMap` maps with a                  |
| [nested-heap-write.ts](nested-heap-write.ts)                                                         | Nested-target heap write (fix #4): an ask result assigned into a deeply nested                    |
| [nested-helper.ts](nested-helper.ts)                                                                 | Asks live inside a script-local helper function: they must still be collected,                    |
| [objassign-shared-subobject.ts](objassign-shared-subobject.ts)                                       | Object.assign shallow-copies: after the call `target.inner === src.inner` (one shared             |
| [object-assign.ts](object-assign.ts)                                                                 | Object.assign (heap fix): a free function that mutates its target in place, copying               |
| [order-control-guarded-ask.ts](order-control-guarded-ask.ts)                                         | `if (result) …` guarding a later ask: a `control` edge from the tested step into the              |
| [order-derived-guard-control.ts](order-derived-guard-control.ts)                                     | A guard that reads a value DERIVED from an ask. `const ok = t.escalate` issues nothing,           |
| [order-dynamic-promise-await.ts](order-dynamic-promise-await.ts)                                     | `await` of a dynamically-selected promise: the awaited expression is a ternary over               |
| [order-forof-sequential.ts](order-forof-sequential.ts)                                               | The motivating pair, half B: `for…of` with an inner `await`. Strictly SEQUENTIAL —                |
| [order-helper-ask-two-call-sites.ts](order-helper-ask-two-call-sites.ts)                             | A helper containing an ask, called from two sites. Phase 1 ships ONE step per site,               |
| [order-implicit-flow-guard.ts](order-implicit-flow-guard.ts)                                         | The regression guard for keeping the SYNTACTIC controller scan in phase 2's control               |
| [order-loop-carries-nothing.ts](order-loop-carries-nothing.ts)                                       | A loop that repeats but carries NO data between rounds. The self-arrow must still                 |
| [order-loop-head-await-tail-issue.ts](order-loop-head-await-tail-issue.ts)                           | The regression guard for phase 2's repetition demotion: a loop whose HEAD awaits the              |
| [order-loop-two-steps-carry.ts](order-loop-two-steps-carry.ts)                                       | A TWO-step loop whose body output feeds the next round: the `carry` edge closes a                 |
| [order-loop-unawaited-fixed-actor.ts](order-loop-unawaited-fixed-actor.ts)                           | An un-awaited ask in a loop on a FIXED actor. Nothing awaits inside the body, so the              |
| [order-loop-unawaited-fresh-actor.ts](order-loop-unawaited-fresh-actor.ts)                           | The same un-awaited loop, but the actor is created INSIDE the body: one fresh actor               |
| [order-map-concurrent.ts](order-map-concurrent.ts)                                                   | The motivating pair, half A: `Promise.all` over a `.map`. N instances COEXIST, so                 |
| [order-mixed-join-stored-promise.ts](order-mixed-join-stored-promise.ts)                             | A stored promise joined with a freshly-issued one. This is the case phase 1 got WRONG             |
| [order-promise-into-helper.ts](order-promise-into-helper.ts)                                         | A promise passed INTO a helper and awaited there. The helper is inlined at its call               |
| [order-shared-helper-residual-cycle.ts](order-shared-helper-residual-cycle.ts)                       | A shared helper issued BEFORE the loop (baseline) and INSIDE it (gate): under the                 |
| [order-stored-promise-late-await.ts](order-stored-promise-late-await.ts)                             | A promise stored in a variable and awaited much later. Phase 1 cannot resolve which               |
| [order-unawaited-one-actor.ts](order-unawaited-one-actor.ts)                                         | Two un-awaited asks on ONE actor, joined at the end: the `Promise.all` does NOT                   |
| [order-unawaited-two-actors.ts](order-unawaited-two-actors.ts)                                       | The same shape on TWO actors: genuinely concurrent. Expect NO edge between the two                |
| [param-mutation.ts](param-mutation.ts)                                                               | Parameter write-back (heap fix): objects cross call boundaries by reference. `stash`              |
| [phase-admission-carryover.ts](phase-admission-carryover.ts)                                         | The REPETITION CARVE-OUT in the phase copies' temporal admission, pinned.                         |
| [phase-empty-phase.ts](phase-empty-phase.ts)                                                         | A phase that issues no step. Its marker is still a position control passes through, so the        |
| [phase-jsonl-db.ts](phase-jsonl-db.ts)                                                               | The jsonl-db optimization loop, condensed: the motivating example for phase markers               |
| [phase-merge-fallback.ts](phase-merge-fallback.ts)                                                   | Two things at once: the same name at two call sites is ONE phase — the name is the key,           |
| [phase-provenance-fanout.ts](phase-provenance-fanout.ts)                                             | The ABSENT-DOMINATES merge rule, pinned. When several facts hold for one ordered pair             |
| [phase-scope-block.ts](phase-scope-block.ts)                                                         | Rest-of-block scope, all three of its edges at once: a marker inside an if-block does             |
| [phase-self-loop.ts](phase-self-loop.ts)                                                             | A refine-until-approved loop living entirely inside one phase. At the step level the              |
| [planner-reviewer.ts](planner-reviewer.ts)                                                           | 0-1, how confident the scan is                                                                    |
| [promise-all-map.ts](promise-all-map.ts)                                                             | Fan-out (.map bound to a variable) feeding a NON-literal Promise.all join feeding                 |
| [README.md](README.md)                                                                               | 本目录用途、子目录与逐文件说明。                                                                  |
| [reduce-accumulator.ts](reduce-accumulator.ts)                                                       | reduce chaining through the accumulator (fix #3): each iteration asks with the                    |
| [reentrant-then-composition.ts](reentrant-then-composition.ts)                                       | Positive guard (already holds): a callback passed to unknown `.then` whose body calls             |
| [replace-fn.ts](replace-fn.ts)                                                                       | .replace with a replacement FUNCTION that returns tainted text. The keystone rule                 |
| [report-progressive.ts](report-progressive.ts)                                                       | report 是站点但**在两张图里都不是节点**：它发的是进度而不是次序，没有什么能等它，                 |
| [rest-param.ts](rest-param.ts)                                                                       | Rest parameter must gather EVERY actual past its position: joinAll(a, b) binds                    |
| [review-launder-chain.ts](review-launder-chain.ts)                                                   | Realistic writer -> reviewer -> reviser workflow; the feedback is reformatted via a               |
| [setter-field.ts](setter-field.ts)                                                                   | Object-literal set accessor: assigning `box.val = secret` must record the assigned                |
| [shared-helper-callback-alias.ts](shared-helper-callback-alias.ts)                                   | The known over-approximation (docs/analysis.md "Open questions"): the callback reaches            |
| [shared-helper-callback-binding.ts](shared-helper-callback-binding.ts)                               | A rate-limit helper shared by five call sites: two fan-outs, a top-level call, and a              |
| [shared-helper-param-each.ts](shared-helper-param-each.ts)                                           | A parameter handed to a per-element library call: `xs.map(fn)` inside `each` is one               |
| [shared-helper-param-to-then.ts](shared-helper-param-to-then.ts)                                     | A parameter handed on to a library call: `.then(fn)` inside `later` is an `argument`              |
| [shared-helper-recursive-with-callback.ts](shared-helper-recursive-with-callback.ts)                 | Genuine recursion with a callback parameter: `walkTree` passes its own `visit` on to the          |
| [shared-helper-two-layers.ts](shared-helper-two-layers.ts)                                           | Two wrapper layers over one callback: `retry` hands `limited` a fresh arrow that calls            |
| [spread-shared-subobject.ts](spread-shared-subobject.ts)                                             | Object spread `{ ...o1 }` shallow-copies: `o2.inner === o1.inner` (shared reference), so          |
| [strand-async-helper-awaited.ts](strand-async-helper-awaited.ts)                                     | The control for strand-async-helper-unawaited: the same helper, awaited at its call site.         |
| [strand-async-helper-unawaited.ts](strand-async-helper-unawaited.ts)                                 | An `async` helper called but not awaited: `const p = h()` starts the helper's activation          |
| [strand-deferred-recursive.ts](strand-deferred-recursive.ts)                                         | A `.then` continuation that re-enters its own function: `refine` registers a continuation         |
| [strand-fanout-awaited-per-phase.ts](strand-fanout-awaited-per-phase.ts)                             | The control for strand-fanout-two-phases-join: the same three fan-outs, but each phase            |
| [strand-fanout-two-phases-join.ts](strand-fanout-two-phases-join.ts)                                 | The reference shape of the strands refactor. Two phases each fan out `async` work and             |
| [strand-fire-and-forget.ts](strand-fire-and-forget.ts)                                               | A fan-out nobody ever awaits: the script starts A's subagents, walks on to B, and returns         |
| [strand-overlap-chain.ts](strand-overlap-chain.ts)                                                   | Overlapping, not nested: A's work is joined before C is entered, B's only before D. The           |
| [strand-then-internal-await.ts](strand-then-internal-await.ts)                                       | A `.then` continuation that awaits inside itself, registered and only later awaited               |
| [stream-pipeline.ts](stream-pipeline.ts)                                                             | Streams (docs/dynamic-workflow/authoring.md, "Streams"): two stages written as futures, each      |
| [tagged-template.ts](tagged-template.ts)                                                             | String.raw tagged template laundering: taint must survive into the next ask.                      |
| [then-callback.ts](then-callback.ts)                                                                 | .then callback on a Node<T> result (Node<T> extends PromiseLike<T>). Runtime:                     |
| [this-field-read-in-method.ts](this-field-read-in-method.ts)                                         | Idiomatic OOP: the constructor stores an artifact in a field, a method reads this.field           |
| [throw-catch.ts](throw-catch.ts)                                                                     | throw/catch dataflow: a facade site inside a thrown expression must be evaluated,                 |
| [types-join-port-refinement.ts](types-join-port-refinement.ts)                                       | Join port refinement + actor-edge type aggregation (docs/analysis.md,                             |
| [types-producer-labels.ts](types-producer-labels.ts)                                                 | Producer-side artifact types on data edges (docs/analysis.md, "Edge                               |
| [unary-operand-facade-call.ts](unary-operand-facade-call.ts)                                         | A facade call inside a void/typeof/delete operand must still be evaluated (the operand            |
| [user-defined-ask.ts](user-defined-ask.ts)                                                           | A user object with its own `.ask` method must NOT register as an ask site:                        |
| [within-fanout.ts](within-fanout.ts)                                                                 | Static fan-out containment (`within`, item 7). Two judge idioms in one script:                    |

<!-- qingqi-directory-index:end -->
