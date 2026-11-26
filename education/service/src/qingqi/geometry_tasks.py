"""Recognize explicit geometry constructions; never infer absent conditions."""
import re
from fractions import Fraction

def clean(text):
    text=text.replace('：',':').replace('∶',':').replace('⟂','⊥').replace('垂直于','⊥').replace('（','(').replace('）',')')
    text=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',text)
    text=text.replace('\\perp','⊥').replace('\\angle','∠').replace('\\triangle','△').replace('\\circ','°').replace('\\neq','≠')
    text=re.sub(r'\\(?:mathrm|operatorname|overline|text|rm)\{([A-Za-z]+)\}',r'\1',text)
    text=re.sub(r'角([A-Z])',r'∠\1',text)
    return re.sub(r'[\s${}*`]','',text)

def identify(source):
    text=clean(source)
    triangle=re.search(r'(?:△|三角形)([A-Z]{3})',text)
    right=re.search(r'∠([A-Z])=90',text)
    if not triangle or not right or right[1] not in triangle[1]:return None
    c=right[1];ends=[v for v in triangle[1] if v!=c]
    if len(set(ends))!=2:return None
    arms=[ends[0]+c,c+ends[0]];other=[ends[1]+c,c+ends[1]]
    if any(left+'≠'+right in text or right+'≠'+left in text for left in arms for right in other):return None
    if not any(left+'='+right in text or right+'='+left in text for left in arms for right in other):return None
    on=re.findall(r'([A-Z])(?:是|为)?(?:在)?([A-Z]{2})(?:边|上)',text)
    d=next((p for p,edge in on if set(edge)==set(ends) and p not in triangle[1]),None)
    moving=next(((p,edge) for p,edge in on if c in edge and p not in triangle[1] and p!=d),None)
    if not d or not moving:return None
    e,edge=moving;a=next(p for p in edge if p!=c);b=next(p for p in ends if p!=a)
    intersection=re.search(r'([A-Z]{2})与射线([A-Z]{2})(?:相)?交(?:于)?(?:点)?([A-Z])',text)
    if not intersection or intersection[2]!=b+c:return None
    f=intersection[3]
    if set(intersection[1])!={d,f} or not any(l+'⊥'+r in text for l in (d+f,f+d) for r in (d+e,e+d)) and not any(l+'⊥'+r in text for r in (d+f,f+d) for l in (d+e,e+d)):return None
    labels=dict(zip(('a','b','c','d','e','f'),(a,b,c,d,e,f)))
    if len(set(labels.values()))!=6:return None
    ratio_key=a+d+':'+d+b+'='
    symbol=re.search(re.escape(ratio_key)+r'([a-z])',text)
    fixed=re.search(re.escape(ratio_key)+r'(\d+(?:\.\d+)?)[/:](\d+(?:\.\d+)?)',text)
    if fixed and (Fraction(fixed[1])<=0 or Fraction(fixed[2])<=0):return {'clarify':'分点比应为正数，当前条件会使几何构造退化，请检查题干中的比例。'}
    ratio=str(Fraction(fixed[1])/Fraction(fixed[2])) if fixed and Fraction(fixed[2]) else '1'
    scale=re.search(r'(?:'+re.escape(a+c+'='+b+c)+r'|'+re.escape(b+c+'='+a+c)+r')=(\d+(?:\.\d+)?)',text)
    if scale and Fraction(scale[1])<=0:return {'clarify':'三角形边长应大于零，请检查识别的边长。'}
    x=re.search(re.escape(a+e)+r'=([a-z])',text);y=re.search(re.escape(b+f)+r'=([a-z])',text)
    midpoint=bool(re.search(re.escape(d)+r'(?:是|为)(?:边)?'+re.escape(a+b)+r'(?:边)?的?中点',text))
    parts=(['midpoint'] if midpoint else [])+(['ratio'] if symbol else [])+(['function'] if fixed and scale and x and y else [])
    if not parts:parts=['ratio']
    return {'arguments':{'construction':'right_isosceles_perpendicular','labels':labels,'scale':scale[1] if scale else 'a','ratio':ratio,'parameter':symbol[1] if symbol else 'r','x_variable':x[1] if x else 'x','y_variable':y[1] if y else 'y','parts':parts}}
