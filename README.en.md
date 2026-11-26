# QingQi for Edu

QingQi is a student-facing education Agent project built on [ZCode](https://github.com/zai-org/ZCode). It connects mathematics tutoring, learning paths, a learning dashboard, and personalized sets of three exercises.

See the [Chinese README](README.md) for product screenshots, the teaching animation, architecture, model configuration, and the complete directory index.

## Run the public demo

Requires Node.js 24, pnpm 10 and Python 3.12 or later.

```sh
pnpm install --ignore-scripts
python -m pip install -r education/service/requirements.txt
pnpm education:build
pnpm education:demo
```

Open http://127.0.0.1:18774/. The demo uses authored questions and a synthetic student profile. Private student records, model weights and credentials are not distributed.

## Repository layout

| Directory           | Contents                                                       |
| ------------------- | -------------------------------------------------------------- |
| education/service   | Python teaching service, verification and student state        |
| education/runtime   | Node runtime based on ZCode's foundation modules               |
| education/client    | HTTP and SSE contracts                                         |
| education/web       | Student pages, visuals and settings                            |
| education/tools     | Startup, import, maintenance and documentation tools           |
| education/tests     | Acceptance scenarios, browser checks, fixtures and live probes |
| education/docs      | Architecture, operation guides, screenshots and animation      |
| apps and packages   | ZCode foundation sources and workspace packages                |
| scripts and .github | Engineering checks, builds and CI                              |
| docs and specs      | Foundation documentation and product specifications            |
| third-party         | Third-party sources, inventories and licenses                  |

Each versioned directory has a README describing its purpose, immediate subdirectories and files. Start at [education/README.md](education/README.md). Source attribution and module boundaries are recorded in [education/source.json](education/source.json) and [the ZCode foundation guide](education/docs/zcode-foundation.md).

The project is distributed under [Apache-2.0](LICENSE), with original source headers and third-party notices retained.
