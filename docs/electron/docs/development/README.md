# Developing Electron

These guides are intended for people working on the Electron project itself.
For guides on Electron app development, see
[/docs/README.md](../README.md#guides-and-tutorials).

## Table of Contents

- [Issues](issues.md)
- [Pull Requests](pull-requests.md)
- [Documentation Styleguide](coding-style.md#documentation)
- [Source Code Directory Structure](source-code-directory-structure.md)
- [Coding Style](coding-style.md)
- [Using clang-tidy on C++ Code](clang-tidy.md)
- [Build Instructions](build-instructions-gn.md)
  - [macOS](build-instructions-macos.md)
  - [Windows](build-instructions-windows.md)
  - [Linux](build-instructions-linux.md)
- [Chromium Development](chromium-development.md)
- [V8 Development](v8-development.md)
- [Testing](testing.md)
- [Debugging](debugging.md)
- [Patches](patches.md)

## Getting Started

In order to contribute to Electron, the first thing you'll want to do is get the code.

[Electron's `build-tools`](https://github.com/electron/build-tools) automate much of the setup for compiling Electron from source with different configurations and build targets.

If you would prefer to build Electron manually, see the [build instructions](build-instructions-gn.md).

Once you've checked out and built the code, you may want to take a look around the source tree to get a better idea
of what each directory is responsible for. The [source code directory structure](source-code-directory-structure.md) gives a good overview of the purpose of each directory.

## Opening Issues on Electron

For any issue, there are generally three ways an individual can contribute:

1. By opening the issue for discussion
   - If you believe that you have found a new bug in Electron, you should report it by creating a new issue in
     the [`electron/electron` issue tracker](https://github.com/electron/electron/issues).
2. By helping to triage the issue
   - You can do this either by providing assistive details (a reproducible test case that demonstrates a bug) or by providing suggestions to address the issue.
3. By helping to resolve the issue
   - This can be done by demonstrating that the issue is not a bug or is fixed;
     but more often, by opening a pull request that changes the source in `electron/electron`
     in a concrete and reviewable manner.

See [issues](issues.md) for more information.

## Making a Pull Request to Electron

Most pull requests opened against the `electron/electron` repository include
changes to either the C/C++ code in the `shell/` folder,
the TypeScript code in the `lib/` folder, the documentation in `docs/`,
or tests in the `spec/` folder.

See [pull requests](pull-requests.md) for more information.

If you want to add a new API module to Electron, you'll want to look in [creating API](creating-api.md).

## Governance

Electron has a fully-fledged governance system that oversees activity in Electron and whose working groups are responsible for areas like APIs, releases, and upgrades to Electron's dependencies including Chromium and Node.js. Depending on how frequently and to what end you want to contribute, you may want to consider joining a working group.

Details about each group and their responsibilities can be found in the [governance repo](https://github.com/electron/governance).

## Patches in Electron

Electron is built on two major upstream projects: Chromium and Node.js. Each of these projects has several of their own dependencies, too. We try our best to use these dependencies exactly as they are but sometimes we can't achieve our goals without patching those upstream dependencies to fit our use cases.

As such, we maintain a collection of patches as part of our source tree. The process for adding or altering one of these patches to Electron's source tree via a pull request can be found in [patches](patches.md).

## Debugging

There are many different approaches to debugging issues and bugs in Electron, many of which
are platform specific.

For an overview of information related to debugging Electron itself (and not an app _built with Electron_), see [debugging](debugging.md).

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

development 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                     | 简要说明                                           |
| ------------------------------------------------------------------------ | -------------------------------------------------- |
| [api-history-migration-guide.md](api-history-migration-guide.md)         | Electron API History Migration Guide：说明文档。   |
| [build-instructions-gn.md](build-instructions-gn.md)                     | Build Instructions：说明文档。                     |
| [build-instructions-linux.md](build-instructions-linux.md)               | Build Instructions (Linux)：说明文档。             |
| [build-instructions-macos.md](build-instructions-macos.md)               | Build Instructions (macOS)：说明文档。             |
| [build-instructions-windows.md](build-instructions-windows.md)           | Build Instructions (Windows)：说明文档。           |
| [chromium-development.md](chromium-development.md)                       | Chromium Development：说明文档。                   |
| [clang-tidy.md](clang-tidy.md)                                           | Using clang-tidy on C++ Code：说明文档。           |
| [coding-style.md](coding-style.md)                                       | Coding Style：说明文档。                           |
| [creating-api.md](creating-api.md)                                       | Creating a New Electron Browser Module：说明文档。 |
| [debugging-on-macos.md](debugging-on-macos.md)                           | Debugging on macOS：说明文档。                     |
| [debugging-on-windows.md](debugging-on-windows.md)                       | Debugging on Windows：说明文档。                   |
| [debugging-with-symbol-server.md](debugging-with-symbol-server.md)       | Setting Up Symbol Server in Debugger：说明文档。   |
| [debugging-with-xcode.md](debugging-with-xcode.md)                       | Debugging with XCode：说明文档。                   |
| [debugging.md](debugging.md)                                             | Electron Debugging：说明文档。                     |
| [issues.md](issues.md)                                                   | Issues In Electron：说明文档。                     |
| [patches.md](patches.md)                                                 | Patches in Electron：说明文档。                    |
| [pull-requests.md](pull-requests.md)                                     | Pull Requests：说明文档。                          |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                   |
| [reclient.md](reclient.md)                                               | Reclient：说明文档。                               |
| [source-code-directory-structure.md](source-code-directory-structure.md) | Source Code Directory Structure：说明文档。        |
| [style-guide.md](style-guide.md)                                         | Electron Documentation Style Guide：说明文档。     |
| [testing.md](testing.md)                                                 | Testing：说明文档。                                |
| [v8-development.md](v8-development.md)                                   | V8 Development：说明文档。                         |

<!-- qingqi-directory-index:end -->
