"""Verify declared architecture entry symbols without executing source files."""
import ast
import re
from functools import lru_cache
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
P='education/service/src/qingqi/'
R='education/runtime/src/'
W='education/web/src/'
BINDINGS={
 'tutoring':[(P+'agent.py','Agent.run'),(P+'conversation.py','prepare')],
 'path':[(P+'learning_branches.py','branch_plan'),(P+'storage.py','Store.select_learning_route')],
 'practice':[(P+'storage.py','Store.practice_action'),(P+'storage.py','Store.prepare_model_hint'),(P+'storage.py','Store._commit_model_hint'),(P+'web_store.py','WebStore.start_practice')],
 'dashboard':[(P+'learning.py','learning_projection'),(P+'learning_map.py','project_map')],
 'loop':[(P+'agent.py','Agent.run'),(P+'storage.py','Store.begin'),(P+'storage.py','Store.prepare_call'),(P+'storage.py','Store.commit'),(P+'storage.py','Store.stop_turn'),(P+'turn_control.py','CancellationScope.check')],
 'tools':[(P+'tools.py','Registry.authorize'),(P+'tools.py','Registry.call'),(P+'student_task_tools.py','StudentTaskTools.execute'),(R+'index.ts','createToolRegistry'),(R+'index.ts','createToolExecutor')],
 'memory':[(P+'storage.py','Store.current_problem'),(P+'storage.py','Store.retrieve'),(R+'memory.ts','selectScopedMemory')],
 'permissions':[(P+'product.py','Handler.principal'),(P+'product.py','Handler.host_ok'),(P+'web_store.py','WebStore.admit_teaching'),(P+'tools.py','Registry.authorize'),(R+'index.ts','PermissionService')],
 'routing':[(P+'student_tasks.py','inspect_request'),(P+'layered_routing.py','LayeredRouter.route'),(P+'tutoring_scope.py','ScopedTutorController.next'),(P+'request_controls.py','strip_denied'),(P+'presentation.py','resolve'),(P+'teaching_policy.py','choose'),(P+'teaching_plan.py','build')],
 'skills':[(P+'skills.py','Skills.load'),(R+'index.ts','createNodeSkillAdapter')],
 'models':[(P+'providers.py','JSONModel.generate'),(P+'providers.py','JSONModel.generate_text'),(P+'model_stream.py','read'),(P+'workers.py','make_workers'),(R+'index.ts','createExploreSubagentPort')],
 'visuals':[(P+'function_solver.py','analyze_function'),(P+'function_reasoning.py','render'),(P+'nonnegative_reasoning.py','render'),(P+'nonnegative_teaching.py','identify'),(P+'identity_animation.py','render'),(P+'visual_followup.py','plan'),(P+'visual_model_contract.py','select'),(P+'visual_teaching.py','validate_binding'),(W+'problem-animation.tsx','ProblemAnimation'),(W+'use-teaching-animation.ts','useTeachingAnimation'),(W+'opposite-animation.tsx','OppositeAnimation')],
 'persistence':[(P+'storage.py','Store.begin'),(P+'storage.py','Store.commit'),(P+'web_store.py','WebStore.detail')],
 'management':[(P+'management.py','update'),(P+'storage.py','Store.clear_history'),(P+'architecture_panorama.py','panorama'),(W+'architecture-svg.tsx','ArchitectureSvg')],
 'web':[(W+'use-workspace.ts','useEducationWorkspace'),(W+'workspace.tsx','EducationWorkspace')],
 'data':[(P+'catalogue.py','Catalogue.item'),(P+'catalogue.py','Catalogue.grade'),(P+'graph.py','Graph.search')],
}

BINDINGS['models'] += [(P+'model_settings.py','ModelSettings.resolve'),(P+'model_settings.py','ModelSettings.select'),(P+'secret_store.py','SecretStore.seal'),(P+'model_protocol.py','normalize_anthropic')]
BINDINGS['management'] += [(W+'architecture-board.tsx','ArchitectureCanvas')]
BINDINGS['web'] += [(W+'visual-annotation.tsx','VisualAnnotation'),(W+'visual-annotation.tsx','snapshotVisual')]
BINDINGS['permissions'] += [(P+'storage.py','Store.visual_source')]
BINDINGS['visuals'] += [(P+'geometry_solver.py','prepare_geometry'),(P+'geometry_animation.py','label_coordinates')]
BINDINGS['visuals'] += [(P+'teaching_visual_pair.py','prepare'),(P+'teaching_visual_pair.py','static_lesson'),(W+'static-reasoning-diagram.tsx','StaticReasoningDiagram')]
BINDINGS['routing'] += [(P+'request_controls.py','answer_directives')]
BINDINGS['memory'] += [(P+'math_display.py','model_history')]
BINDINGS['visuals'] += [(P+'math_display.py','compact_response'),(W+'number-line.tsx','NumberLine')]

BINDINGS['models'] += [('packages/ui/src/settings/model-provider-section/SectionLayout.tsx','ModelProviderSectionLayout'),('packages/ui/src/settings/model-provider-section/ProviderCardSections.tsx','ProviderCardHeader'),('packages/ui/src/settings/model-provider-section/ProviderCardSections.tsx','ProviderConnectionSection'),('packages/ui/src/settings/model-provider-section/ProviderCardSections.tsx','ProviderApiKeySection'),('packages/ui/src/settings/model-provider-section/ProviderFormControls.tsx','ModelRowInput'),('packages/ui/src/settings/model-provider-section/ProviderModelMetadataDialog.tsx','ProviderModelMetadataDialog')]

@lru_cache(maxsize=64)
def symbols(file,mtime):
    source=(REPO/file).read_text(encoding='utf-8-sig')
    if file.endswith('.py'):
        tree=ast.parse(source);names=set()
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):names.add(node.name)
            if isinstance(node,ast.ClassDef):
                names.update(node.name+'.'+n.name for n in node.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)))
        return names
    # TypeScript引用由根类型检查保证可解析；此处核对定义或实际调用，不能仅以文件存在冒充实现。
    return set(re.findall(r'\b(?:function|class)\s+(\w+)|\b(?:new\s+)?(\w+)\s*\(',source))

def verified_bindings(module):
    bindings=[]
    for file,symbol in BINDINGS[module]:
        path=REPO/file
        if not path.is_file():raise ValueError('architecture source missing: '+file)
        found=symbols(file,path.stat().st_mtime_ns)
        verified=symbol in found if file.endswith('.py') else any(symbol in pair for pair in found)
        if not verified:raise ValueError('architecture implementation symbol missing: '+file+':'+symbol)
        bindings.append({'file':file,'symbol':symbol,'verified':True})
    return bindings
