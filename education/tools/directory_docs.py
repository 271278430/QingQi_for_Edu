"""Generate and verify directory READMEs from the versioned source file set."""
import argparse
from collections import defaultdict
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import quote, unquote

ROOT=Path(__file__).resolve().parents[2]
START='<!-- qingqi-directory-index:start -->'
END='<!-- qingqi-directory-index:end -->'
BASIS='清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。'
COMMON={
 'turn_control.py':'Store停止命令、临时取消作用域及本轮HTTP连接中断。',
 'turn_stop_fixture.py':'观察真实连接断开的本地模型与独立产品夹具。',
 'turn_stop_acceptance.py':'停止、输入归属、提交竞争、帮助曝光和双协议HTTP验收。',
 'turn_stop_browser.mjs':'桌面和手机停止、刷新恢复、双提交与草稿保留的浏览器验收。',
 'runtime_bounds_acceptance.py':'RPC绝对截止时间、重复回调和有界清理验收。',
 'composer-actions.tsx':'生成期间的发送和停止按钮。',
 'turn-status.tsx':'运行、停止、失败与明确重新回答的消息操作。',
 'codex-agent-capabilities-v1.md':'Codex源码对照、通用能力修正、状态边界和验收范围。',
 'codex-turn-control-v1.md':'轮次停止、权限准入、终态竞争与工具预算规格。',
 'student_tasks.py':'当前输入的任务识别、资料引用、查询 Controller 与任务产物校验。',
 'student_task_tools.py':'推荐练习、学习路线预览和学情读取的同学生工具端口。',
 'student-task-contract.ts':'题卡、学习摘要和学生任务结果的公共类型。',
 'student-task-results.tsx':'对话中的题卡、学情和路线展示，以及旧错误回复的明确重执行入口。',
 'README.md':'本目录用途、子目录与逐文件说明。',
 'AGENTS.md':'本目录的开发规范、模块边界与验证要求。',
 'CONTRACT.md':'模块职责、公共接口、依赖方向和状态约定。',
 'LICENSE':'代码许可原文。','LICENSE.md':'代码许可原文。',
 'NOTICE':'来源与版权声明。','NOTICE.md':'来源与版权声明。',
 'THIRD-PARTY-NOTICES.md':'第三方依赖和资源的版权与许可声明。',
 'UPSTREAM_README.md':'ZCode 或第三方资料的原始目录说明，保留原文和版权。',
 'pnpm-lock.yaml':'pnpm 锁定的依赖版本和完整性信息。',
 'package-lock.json':'ZCode 基础工程保留的 npm 依赖锁文件。',
 'pnpm-workspace.yaml':'工作区包、平台依赖与构建许可配置。',
 '.gitignore':'不进入 Git 的依赖、缓存、凭据和运行产物规则。',
 '.gitattributes':'文件换行、二进制资产与 Git 属性规则。',
 '.npmrc':'pnpm/npm 安装源与工作区链接方式。',
 'tsconfig.base.json':'工作区 TypeScript 公共编译配置。',
 'architecture-policy.yaml':'模块所有者、层级、依赖方向与架构检查策略。',
}
DOMAIN={
 'current_task':'本轮任务优先、多图查询、推荐与同题续聊',
 'architecture':'系统关系图、真实循环和模块职责',
 'acceptance':'Agent 请求、权限、工具和提交边界',
 'product_deployment':'已部署入口、四页面和管理界面',
 'learning_tutor':'练习与同题辅导的连续性',
 'tutoring_evolution':'教学方式、追问与步骤演示',
 'model_acceptance':'模型调用与结果边界',
 'course_model':'课程专项模型',
 'system_review':'路由、核验与错误场景',
 'read_teach_response':'教学响应读取',
 'save_full_diagram':'完整 SVG 导出',
 'contextual_teaching':'上下文教学方式与单个可视化输出',
 'composer_models':'对话选模、推理档位与发送快照',
 'conversation_function':'同题函数辅导','conversation_problem':'同题上下文与多问续聊',
 'grounded_hint':'原题提示与学生进度归因','history_tutor':'历史题选择与连续辅导',
 'scoped_stream':'小问范围与流式输出','codex_stream':'增量文字、错误终态与恢复',
 'model_settings':'模型连接、加密凭据与角色配置','model_stream_budget':'模型流式与生成预算',
 'zcode_model':'ZCode 供应商与嵌套型号','source_reuse':'ZCode UI 与浏览器基础',
 'runtime_reuse':'ZCode 工具、MCP、Skills、记忆和子任务',
 'runtime_build':'Node 运行层构建与原子发布','provider_protocol':'模型协议适配',
 'adaptive_learning':'动态学情、学习路径与多样化三题','learning_evidence':'独立作答、保持与复习依据',
 'student_data':'教材、题库、画像与学情页面','four_feature':'四项学生功能',
 'product_usability':'学生操作、原题绑定与错误状态','interaction_inventory':'页面全部操作入口',
 'solid_web':'页面布局、设置生命周期与手机导航','multimodal':'多图上传、识读与消息附件',
 'vision_schema':'视觉模型协议与错误响应','vision_protocol':'视觉模型协议',
 'problem_reasoning':'函数与几何的解题步骤图示','geometry':'几何条件、构造与核验',
 'identity_animation':'恒等式动画与答案许可','story_context':'情景故事与原题条件',
 'combined_presentation':'图示、动画与故事的组合请求','visual_discussion':'图上标注与返图讨论',
 'visual_tasks':'可视化任务与原题参数','visual_teaching':'教学图示与精确坐标',
 'history_clear':'历史清理、版本和幂等回执','system_management':'系统设置与管理权限',
 'route_quality':'任务路由与教学策略','precise_math':'分数、根式和精确数值展示',
 'concept_definition':'概念解释与引导','demo':'自编数据与无密钥演示',
 'browser_recovery':'超时、错误与浏览器恢复','launcher':'启动和停止入口',
}

def inventory():
    names=subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT).decode('utf-8').split('\0')
    files=defaultdict(set);children=defaultdict(set)
    for name in names:
        if not name or not (ROOT/name).is_file():continue
        p=PurePosixPath(name);files[str(p.parent)].add(p.name)
        for parent in p.parents:
            files.setdefault(str(parent),set())
            if str(parent)!='.':children[str(parent.parent)].add(parent.name)
    # 目录说明本身也是版本化文件；生成前后使用相同文件集。
    for directory in list(files):
        existing=next((n for n in files[directory] if n.lower()=='readme.md'),None)
        files[directory].add(existing or 'README.md')
    return files,children

def read_text(path):
    with path.open('rb') as stream:data=stream.read(1000000)
    return data.decode('utf-8',errors='replace')

def clean(text):
    # 模块注释中的 Markdown 语法示例不是目录链接，索引保留其文字含义。
    text=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',text)
    text=re.sub(r'\s+',' ',text).strip().replace('|','\\|')
    text=text.replace('复用','采用')
    return text[:160]

def link_label(name):
    for character in ['\\','_','*','[',']','`']:
        name=name.replace(character,'\\'+character)
    return name

def package_info(directory,cache):
    for parent in [ROOT/directory,*(ROOT/directory).parents]:
        if not parent.is_relative_to(ROOT):break
        key=str(parent)
        if key not in cache:
            p=parent/'package.json'
            try:cache[key]=json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else None
            except (ValueError,UnicodeError):cache[key]=None
        if cache[key]:return cache[key]
    return None

def scope(directory,descriptions,cache):
    if directory in descriptions['folders']:return descriptions['folders'][directory]
    parts=PurePosixPath(directory).parts
    roles={'src':'实现源码','tests':'验收与回归场景','test':'测试场景','fixtures':'测试夹具与样例',
           'assets':'静态资源','resources':'运行资源','docs':'设计与维护文档','scripts':'工程脚本',
           'hooks':'生命周期与操作入口','templates':'模板','references':'参考资料','skills':'技能指导和资源',
           'licenses':'第三方许可','icons':'图标','fonts':'字体资源','migrations':'数据库迁移',
           'components':'界面组件','store':'界面状态','adapters':'外部能力与平台适配',
           'contracts':'公共契约','schemas':'运行时数据结构','locales':'语言资源'}
    role=next((roles[p] for p in reversed(parts) if p in roles),'模块文件')
    package=package_info(directory,cache)
    location=PurePosixPath(directory).name.replace('-',' ')
    if directory.startswith('third-party/') or 'vendor' in parts or 'design-resources' in parts:
        return f'第三方资料中的 {location} {role}，保留原始来源、版权和资源内容。'
    if directory.startswith(('apps/','packages/')):
        name=package.get('name','ZCode') if package else 'ZCode'
        return f'{name} 基础工程中的 {location} {role}。'
    return f'{location} {role}，属于 {parts[0] if parts else "项目"} 目录。'

def describe(name,descriptions):
    if name in descriptions['files']:return descriptions['files'][name]
    p=PurePosixPath(name);base=p.name
    if base.lower()=='readme.md':return COMMON['README.md']
    if base in COMMON:return COMMON[base]
    if base.startswith(('LICENSE','NOTICE','COPYING')):return '原始许可或版权声明。'
    if base=='package.json':
        value=json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
        return f'{value.get("name","模块")} 的包信息、依赖和开发命令。'
    if base.startswith('tsconfig'):return '本模块的 TypeScript 编译、类型检查或构建范围。'
    if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.ico','.svg','.gif','.woff','.woff2','.ttf','.mp3','.mp4','.pdf'}:
        role={'.svg':'矢量图形','.gif':'动画图像','.pdf':'PDF 文档','.mp4':'视频','.mp3':'音频','.woff':'字体','.woff2':'字体','.ttf':'字体'}.get(p.suffix.lower(),'图像')
        return f'{role}资源：{p.stem}。'
    if name.startswith('education/tests/'):
        domain=next((v for k,v in sorted(DOMAIN.items(),key=lambda kv:-len(kv[0])) if k in base),p.stem.replace('_',' ').replace('-',' '))
        kind='真实服务探针' if 'live' in base else '可控服务或样例数据' if any(k in base for k in ('fixture','server','cases')) else '浏览器交互验收' if 'browser' in base else '验收与检查'
        return f'{kind}：{domain}。'
    if p.suffix.lower() in {'.md','.mdx'}:
        text=read_text(ROOT/name);title=re.search(r'^#{1,3}\s+(.+)',text,re.M)
        return clean(title[1])+'：说明文档。' if title else f'{p.stem} 说明资料。'
    if p.suffix.lower() in {'.json','.jsonc','.yaml','.yml','.toml','.xml','.properties','.gradle'}:return f'{p.stem} 的数据或配置定义。'
    if p.suffix.lower() in {'.py','.ts','.tsx','.js','.mjs','.cjs','.sh','.ps1','.swift','.kt','.java','.rs','.cpp','.h','.css'}:
        text=read_text(ROOT/name)
        if p.suffix=='.py':
            doc=re.match(r'^\s*(?:#[^\n]*\n\s*)*[ruRU]?(?:"""|\x27\x27\x27)([\s\S]*?)(?:"""|\x27\x27\x27)',text)
            if doc:return clean(doc[1].strip().splitlines()[0])
            symbols=re.findall(r'^(?:async\s+)?(?:def|class)\s+(\w+)',text,re.M)
        else:
            comments=re.findall(r'^\s*(?://|/\*\*?|\*)\s*([^\n]+)',text[:4000],re.M)
            useful=next((c for c in comments if len(c)>14 and not re.search(r'copyright|license|SPDX|modified by|eslint|https?://|^@|^---|^===',c,re.I) and not c.startswith(('import','export'))),None)
            if useful:return clean(useful.rstrip('*/ '))
            symbols=re.findall(r'export\s+(?:default\s+)?(?:async\s+)?(?:function|class|interface|type|const|enum)\s+(\w+)',text)
        if symbols:return '实现或公开接口：'+ '、'.join(dict.fromkeys(symbols[:4]))+'。'
        role={'.css':'布局与样式','.tsx':'React 组件','.sh':'Shell 脚本','.ps1':'PowerShell 脚本','.swift':'原生 Swift 实现','.kt':'Android 实现'}.get(p.suffix,'实现文件')
        return f'{p.stem} 的{role}。'
    return f'{p.stem} 模块的资源或工程文件。'

def section(directory,files,children,descriptions,cache):
    lines=[START,'## 目录与文件','',BASIS,'',scope(directory,descriptions,cache),'']
    if children[directory]:
        lines+=['### 子目录','','| 目录 | 存放内容 |','| --- | --- |']
        for child in sorted(children[directory],key=str.casefold):
            path=str(PurePosixPath(directory)/child)
            lines.append(f'| [{link_label(child)}/]({quote(child+"/README.md",safe="/._-")}) | {clean(scope(path,descriptions,cache))} |')
        lines.append('')
    lines+=['### 文件','','| 文件 | 简要说明 |','| --- | --- |']
    for name in sorted(files[directory],key=str.casefold):
        path=str(PurePosixPath(directory)/name)
        lines.append(f'| [{link_label(name)}]({quote(name,safe="._-")}) | {clean(describe(path,descriptions))} |')
    lines+=['',END]
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description='维护版本化目录的 README 索引，不读取运行数据。')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    descriptions=json.loads((ROOT/'education/docs/directory-descriptions.json').read_text(encoding='utf-8-sig'))
    files,children=inventory();cache={};errors=[];updated=0
    for directory in sorted(files):
        name=next(n for n in files[directory] if n.lower()=='readme.md');p=ROOT/directory/name
        expected=section(directory,files,children,descriptions,cache)
        current=p.read_text(encoding='utf-8-sig') if p.exists() else ''
        if args.check:
            match=re.search(re.escape(START)+r'([\s\S]*?)'+re.escape(END),current)
            if not match:errors.append({'directory':directory,'reason':'missing_index'});continue
            targets=set(re.findall(r'\]\(([^)]+)\)',match[1]))
            wanted=set(re.findall(r'\]\(([^)]+)\)',expected))
            if targets!=wanted:errors.append({'directory':directory,'reason':'stale_or_incomplete_file_list'})
            if BASIS not in match[1]:errors.append({'directory':directory,'reason':'missing_project_origin'})
            for target in targets:
                if '://' not in target and not (p.parent/unquote(target)).exists():errors.append({'directory':directory,'reason':'broken_link','target':target})
            continue
        before=re.sub(re.escape(START)+r'[\s\S]*?'+re.escape(END),'',current).rstrip()
        if not before:before='# '+('仓库' if directory=='.' else PurePosixPath(directory).name)
        value=before+'\n\n'+expected+'\n'
        if current!=value:p.write_text(value,encoding='utf-8',newline='\n');updated+=1
    report={'directories':len(files),'direct_file_entries':sum(map(len,files.values())),'updated':updated,'errors':errors,'check':args.check}
    print(json.dumps(report,ensure_ascii=False))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
