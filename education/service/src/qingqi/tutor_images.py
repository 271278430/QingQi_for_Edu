"""Bounded image decoding; no paths or remote URLs from students."""
import base64
import io
import re
from .contracts import ContractError, TEXT, obj

VISION_SCHEMA = obj({'text': {**TEXT, 'maxLength': 1400}, 'unclear': {'type': 'boolean'}, 'note': {**TEXT, 'maxLength': 300}})


def optional_choices_recognition(result):
    """Missing choices do not prevent an already complete, bounded numeric task."""
    import re
    from .function_solver import identify
    note=result.get('note','');text=result.get('text','')
    # 真实截图的数值目标完整，OCR曾只因选项未截入而阻断。只能恢复这一明确范围，不能猜模糊的系数。
    if result.get('unclear') and re.search(r'选项|冒号',note) and not re.search(r'看不清|模糊|不清晰|无法辨认|不确定|可能|遮挡|系数.*(?:缺|残)|条件.*(?:缺|残)',note) and re.search(r'最大值.*最小值.*(?:和|之和)',text) and identify(text):
        return {**result,'unclear':False,'note':'转写包含完整函数、正零点条件、区间与数值所求；截图缺少选项不影响该目标，不补造选项。'}
    return result

def legacy_recognition_failure(state,images):
    # 同一规则用于恢复准入和历史投影，避免旧失败在页面上继续显示为可重发输入错误。
    error=state.get('error','')
    return bool(images and not state.get('vision') and state.get('error_type')=='ContractError' and
                error.startswith('$: unknown') and 'input' in error and 'required_output_schema' in error)

def recognition_result(value):
    # 已有真实识别字段时可以忽略提供方夹带的已知包装；仅回显输入时仍拒绝，不能冒充识图。
    if isinstance(value,dict) and {'text','unclear','note'}<=set(value) and set(value)<={'text','unclear','note','unclear_reason','input','required_output_schema'}:
        value={k:v for k,v in value.items() if k not in {'input','required_output_schema'}}
    # 真实 GLM 会附加 unclear_reason；只归一这个说明别名，仍拒绝其余未知字段。
    if isinstance(value, dict) and set(value) <= {'text', 'unclear', 'note', 'unclear_reason'}:
        value = {**value, 'note': value.get('note', value.get('unclear_reason', ''))}
        value.pop('unclear_reason', None)
    return value

def describes_image(question):
    # “描述图片，不解题”属于描述；不能仅看见“解题/答案”就忽略邻近否定。
    positive_teaching=any(not re.search(r'(?:不要|不用|不需要|无需|别|不)(?:先|再|直接|给|给我|求|提供|最终|完整|正确|任何|的|\s){0,5}$',question[max(0,m.start()-14):m.start()]) for m in re.finditer(r'解题|解方程|提示|答案|作答|苏格拉底',question))
    return bool(re.search(r'图片|照片|截图|这张图|图中|图表|这张表|表中|表格', question) and re.search(r'表达|内容|描述|什么意思|总结|分析|介绍|说明|比较|解读|含义', question) and not positive_teaching)

def refers_to_image(question):
    # “图里这道题”也是明确的同会话图片引用，不应要求学生再贴一次题目。
    return bool(re.search(r'图片|照片|截图|这张图|图中|图里|图上的题|图表|这张表|表中|表格|这行|这一列|第[一二三四五六七八九十0-9]+[行列]', question) and not re.search(r'新问题|新题|取消|结束当前', question))

def normalize(data_url):
    from PIL import Image, ImageOps, UnidentifiedImageError
    match = re.fullmatch(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)', data_url)
    if not match:
        raise ContractError('请选择 PNG、JPEG 或 WebP 图片。')
    try:
        raw = base64.b64decode(match[2], validate=True)
        if not raw or len(raw) > 8 * 1024 * 1024:
            raise ContractError('单张图片不能超过 8 MB。')
        with Image.open(io.BytesIO(raw)) as image:
            if image.format not in {'PNG', 'JPEG', 'WEBP'} or image.width * image.height > 16_000_000 or getattr(image, 'n_frames', 1) != 1:
                raise ContractError('图片格式、尺寸或动画不支持，请上传静态题目图片。')
            image.load()
            image = ImageOps.exif_transpose(image).convert('RGB')
            image.thumbnail((1600, 1600))
            output = io.BytesIO()
            image.save(output, 'JPEG', quality=90)
            return output.getvalue(), image.width, image.height
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as error:
        if isinstance(error, ContractError):
            raise
        raise ContractError('图片无法读取，请换一张清晰的题目图片。') from None

def data_uri(raw):
    return 'data:image/jpeg;base64,' + base64.b64encode(raw).decode('ascii')
