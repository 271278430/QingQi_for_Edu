# storage

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 storage 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                                              |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                                      |
| [StorageCategoryDetail.tsx](StorageCategoryDetail.tsx)           | 实现或公开接口：StorageCategoryDetail。                                                               |
| [StorageCategoryList.tsx](StorageCategoryList.tsx)               | 实现或公开接口：StorageCategoryList。                                                                 |
| [storageCategoryPresentation.ts](storageCategoryPresentation.ts) | 把多个根的同类别占用合并，按 bytes 降序（同为 0 时保持目录顺序）。                                    |
| [StorageCleanConfirmDialog.tsx](StorageCleanConfirmDialog.tsx)   | 实现或公开接口：StorageCleanConfirmTarget、StorageCleanConfirmDialog。                                |
| [StorageDiskCard.tsx](StorageDiskCard.tsx)                       | 实现或公开接口：StorageDiskCard。                                                                     |
| [StorageSection.tsx](StorageSection.tsx)                         | \* 资源管理器「存储」tab。                                                                            |
| [useStorageUsage.ts](useStorageUsage.ts)                         | \* useStorageUsage —— 资源管理器「存储」tab 的数据源，输入是 preload 暴露的 StorageManagementBridge。 |

<!-- qingqi-directory-index:end -->
