# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/documents-plugin 基础工程中的 scripts 工程脚本。

### 子目录

| 目录                              | 存放内容                                              |
| --------------------------------- | ----------------------------------------------------- |
| [templates/](templates/README.md) | @zcode/documents-plugin 基础工程中的 templates 模板。 |

### 文件

| 文件                                               | 简要说明                                                                         |
| -------------------------------------------------- | -------------------------------------------------------------------------------- |
| [\_\_init\_\_.py](__init__.py)                     | **init** 的实现文件。                                                            |
| [add_toc_placeholders.py](add_toc_placeholders.py) | Add placeholder entries to Table of Contents in a DOCX file.                     |
| [document.py](document.py)                         | Library for working with Word documents: comments, tracked changes, and editing. |
| [fix_footer_fields.py](fix_footer_fields.py)       | Fix footer PAGE field instructions in a DOCX file for WPS/Word compatibility.    |
| [postcheck.py](postcheck.py)                       | postcheck.py — Document business rule self-check script                          |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                 |
| [utilities.py](utilities.py)                       | Utilities for editing OOXML documents.                                           |

<!-- qingqi-directory-index:end -->
