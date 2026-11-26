# rules

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

zcode-cli 基础工程中的 rules 技能指导和资源。

### 文件

| 文件                                                                               | 简要说明                                                                                      |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [\_sections.md](_sections.md)                                                      | Sections：说明文档。                                                                          |
| [\_template.md](_template.md)                                                      | Rule Title Here：说明文档。                                                                   |
| [advanced-effect-event-deps.md](advanced-effect-event-deps.md)                     | Do Not Put Effect Events in Dependency Arrays：说明文档。                                     |
| [advanced-event-handler-refs.md](advanced-event-handler-refs.md)                   | Store Event Handlers in Refs：说明文档。                                                      |
| [advanced-init-once.md](advanced-init-once.md)                                     | Initialize App Once, Not Per Mount：说明文档。                                                |
| [advanced-use-latest.md](advanced-use-latest.md)                                   | useEffectEvent for Stable Callback Refs：说明文档。                                           |
| [async-api-routes.md](async-api-routes.md)                                         | Prevent Waterfall Chains in API Routes：说明文档。                                            |
| [async-cheap-condition-before-await.md](async-cheap-condition-before-await.md)     | Check Cheap Conditions Before Async Flags：说明文档。                                         |
| [async-defer-await.md](async-defer-await.md)                                       | Defer Await Until Needed：说明文档。                                                          |
| [async-dependencies.md](async-dependencies.md)                                     | Dependency-Based Parallelization：说明文档。                                                  |
| [async-parallel.md](async-parallel.md)                                             | Promise.all() for Independent Operations：说明文档。                                          |
| [async-suspense-boundaries.md](async-suspense-boundaries.md)                       | Strategic Suspense Boundaries：说明文档。                                                     |
| [bundle-analyzable-paths.md](bundle-analyzable-paths.md)                           | Prefer Statically Analyzable Paths：说明文档。                                                |
| [bundle-barrel-imports.md](bundle-barrel-imports.md)                               | Avoid Barrel File Imports：说明文档。                                                         |
| [bundle-conditional.md](bundle-conditional.md)                                     | Conditional Module Loading：说明文档。                                                        |
| [bundle-defer-third-party.md](bundle-defer-third-party.md)                         | Defer Non-Critical Third-Party Libraries：说明文档。                                          |
| [bundle-dynamic-imports.md](bundle-dynamic-imports.md)                             | Dynamic Imports for Heavy Components：说明文档。                                              |
| [bundle-preload.md](bundle-preload.md)                                             | Preload Based on User Intent：说明文档。                                                      |
| [client-event-listeners.md](client-event-listeners.md)                             | Deduplicate Global Event Listeners：说明文档。                                                |
| [client-localstorage-schema.md](client-localstorage-schema.md)                     | Version and Minimize localStorage Data：说明文档。                                            |
| [client-passive-event-listeners.md](client-passive-event-listeners.md)             | Use Passive Event Listeners for Scrolling Performance：说明文档。                             |
| [client-swr-dedup.md](client-swr-dedup.md)                                         | Use SWR for Automatic Deduplication：说明文档。                                               |
| [js-batch-dom-css.md](js-batch-dom-css.md)                                         | Avoid Layout Thrashing：说明文档。                                                            |
| [js-cache-function-results.md](js-cache-function-results.md)                       | Cache Repeated Function Calls：说明文档。                                                     |
| [js-cache-property-access.md](js-cache-property-access.md)                         | Cache Property Access in Loops：说明文档。                                                    |
| [js-cache-storage.md](js-cache-storage.md)                                         | Cache Storage API Calls：说明文档。                                                           |
| [js-combine-iterations.md](js-combine-iterations.md)                               | Combine Multiple Array Iterations：说明文档。                                                 |
| [js-early-exit.md](js-early-exit.md)                                               | Early Return from Functions：说明文档。                                                       |
| [js-flatmap-filter.md](js-flatmap-filter.md)                                       | Use flatMap to Map and Filter in One Pass：说明文档。                                         |
| [js-hoist-regexp.md](js-hoist-regexp.md)                                           | Hoist RegExp Creation：说明文档。                                                             |
| [js-index-maps.md](js-index-maps.md)                                               | Build Index Maps for Repeated Lookups：说明文档。                                             |
| [js-length-check-first.md](js-length-check-first.md)                               | Early Length Check for Array Comparisons：说明文档。                                          |
| [js-min-max-loop.md](js-min-max-loop.md)                                           | Use Loop for Min/Max Instead of Sort：说明文档。                                              |
| [js-request-idle-callback.md](js-request-idle-callback.md)                         | Defer Non-Critical Work with requestIdleCallback：说明文档。                                  |
| [js-set-map-lookups.md](js-set-map-lookups.md)                                     | Use Set/Map for O(1) Lookups：说明文档。                                                      |
| [js-tosorted-immutable.md](js-tosorted-immutable.md)                               | Use toSorted() Instead of sort() for Immutability：说明文档。                                 |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                              |
| [rendering-activity.md](rendering-activity.md)                                     | Use Activity Component for Show/Hide：说明文档。                                              |
| [rendering-animate-svg-wrapper.md](rendering-animate-svg-wrapper.md)               | Animate SVG Wrapper Instead of SVG Element：说明文档。                                        |
| [rendering-conditional-render.md](rendering-conditional-render.md)                 | Use Explicit Conditional Rendering：说明文档。                                                |
| [rendering-content-visibility.md](rendering-content-visibility.md)                 | CSS content-visibility for Long Lists：说明文档。                                             |
| [rendering-hoist-jsx.md](rendering-hoist-jsx.md)                                   | Hoist Static JSX Elements：说明文档。                                                         |
| [rendering-hydration-no-flicker.md](rendering-hydration-no-flicker.md)             | Prevent Hydration Mismatch Without Flickering：说明文档。                                     |
| [rendering-hydration-suppress-warning.md](rendering-hydration-suppress-warning.md) | Suppress Expected Hydration Mismatches：说明文档。                                            |
| [rendering-resource-hints.md](rendering-resource-hints.md)                         | Use React DOM Resource Hints：说明文档。                                                      |
| [rendering-script-defer-async.md](rendering-script-defer-async.md)                 | Use defer or async on Script Tags：说明文档。                                                 |
| [rendering-svg-precision.md](rendering-svg-precision.md)                           | Optimize SVG Precision：说明文档。                                                            |
| [rendering-usetransition-loading.md](rendering-usetransition-loading.md)           | Use useTransition Over Manual Loading States：说明文档。                                      |
| [rerender-defer-reads.md](rerender-defer-reads.md)                                 | Defer State Reads to Usage Point：说明文档。                                                  |
| [rerender-dependencies.md](rerender-dependencies.md)                               | Narrow Effect Dependencies：说明文档。                                                        |
| [rerender-derived-state-no-effect.md](rerender-derived-state-no-effect.md)         | Calculate Derived State During Rendering：说明文档。                                          |
| [rerender-derived-state.md](rerender-derived-state.md)                             | Subscribe to Derived State：说明文档。                                                        |
| [rerender-functional-setstate.md](rerender-functional-setstate.md)                 | Use Functional setState Updates：说明文档。                                                   |
| [rerender-lazy-state-init.md](rerender-lazy-state-init.md)                         | Use Lazy State Initialization：说明文档。                                                     |
| [rerender-memo-with-default-value.md](rerender-memo-with-default-value.md)         | Extract Default Non-primitive Parameter Value from Memoized Component to Constant：说明文档。 |
| [rerender-memo.md](rerender-memo.md)                                               | Extract to Memoized Components：说明文档。                                                    |
| [rerender-move-effect-to-event.md](rerender-move-effect-to-event.md)               | Put Interaction Logic in Event Handlers：说明文档。                                           |
| [rerender-no-inline-components.md](rerender-no-inline-components.md)               | Don't Define Components Inside Components：说明文档。                                         |
| [rerender-simple-expression-in-memo.md](rerender-simple-expression-in-memo.md)     | Do not wrap a simple expression with a primitive result type in useMemo：说明文档。           |
| [rerender-split-combined-hooks.md](rerender-split-combined-hooks.md)               | Split Combined Hook Computations：说明文档。                                                  |
| [rerender-transitions.md](rerender-transitions.md)                                 | Use Transitions for Non-Urgent Updates：说明文档。                                            |
| [rerender-use-deferred-value.md](rerender-use-deferred-value.md)                   | Use useDeferredValue for Expensive Derived Renders：说明文档。                                |
| [rerender-use-ref-transient-values.md](rerender-use-ref-transient-values.md)       | Use useRef for Transient Values：说明文档。                                                   |
| [server-after-nonblocking.md](server-after-nonblocking.md)                         | Use after() for Non-Blocking Operations：说明文档。                                           |
| [server-auth-actions.md](server-auth-actions.md)                                   | Authenticate Server Actions Like API Routes：说明文档。                                       |
| [server-cache-lru.md](server-cache-lru.md)                                         | Cross-Request LRU Caching：说明文档。                                                         |
| [server-cache-react.md](server-cache-react.md)                                     | Per-Request Deduplication with React.cache()：说明文档。                                      |
| [server-dedup-props.md](server-dedup-props.md)                                     | Avoid Duplicate Serialization in RSC Props：说明文档。                                        |
| [server-hoist-static-io.md](server-hoist-static-io.md)                             | Hoist Static I/O to Module Level：说明文档。                                                  |
| [server-no-shared-module-state.md](server-no-shared-module-state.md)               | Avoid Shared Module State for Request Data：说明文档。                                        |
| [server-parallel-fetching.md](server-parallel-fetching.md)                         | Parallel Data Fetching with Component Composition：说明文档。                                 |
| [server-parallel-nested-fetching.md](server-parallel-nested-fetching.md)           | Parallel Nested Data Fetching：说明文档。                                                     |
| [server-serialization.md](server-serialization.md)                                 | Minimize Serialization at RSC Boundaries：说明文档。                                          |

<!-- qingqi-directory-index:end -->
