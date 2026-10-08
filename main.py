"""장비 속성을 semantic ID로 식별하고 단위 변환, 중복 의미, 값 범위, 장비 연결 참조 오류를 검사합니다."""
import argparse, json, math, html
from pathlib import Path

def finite(value, name, minimum=None):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(name + ': finite number required')
    if minimum is not None and value < minimum:
        raise ValueError(name + ': below minimum')
    return value

def report(result, title):
    payload=html.escape(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    return '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>body{font:16px/1.6 system-ui;max-width:1000px;margin:32px auto;padding:20px;background:#101b2b;color:#ecf4ff}pre{padding:24px;background:#192b40;border-radius:12px;white-space:pre-wrap;overflow-wrap:anywhere}h1{color:#80e4c5}</style><h1>'+html.escape(title)+'</h1><p>오프라인 샘플 계산 결과 · 실물 장비 연결 없음</p><pre>'+payload+'</pre></html>'

def cli(run,title):
    parser=argparse.ArgumentParser(description=title)
    parser.add_argument('--input',default=str(Path(__file__).with_name('sample-input.json')))
    parser.add_argument('--html',help='optional standalone HTML result path')
    args=parser.parse_args()
    try:
        data=json.loads(Path(args.input).read_text(encoding='utf-8'))
        result=run(data)
        if args.html: Path(args.html).write_text(report(result,title),encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    except (ValueError,KeyError,TypeError) as exc:
        parser.exit(2, 'input error: '+str(exc)+'\n')

UNITS={'temperature':{'Cel':(1,0),'K':(1,-273.15)},'speed':{'m/s':(1,0),'mm/s':(0.001,0)},'current':{'A':(1,0),'mA':(0.001,0)}}
CANON={'temperature':'Cel','speed':'m/s','current':'A'}

def run(data):
    contracts=data['contracts']; assets=data['assets'];errors=[];normalized=[]
    ids=[a['id'] for a in assets]
    if any(not isinstance(x,str) or not x for x in ids):raise ValueError('asset IDs required')
    if len(set(ids))!=len(ids):raise ValueError('duplicate asset ID')
    for semantic,c in contracts.items():
        if c['kind'] not in UNITS:raise ValueError('unsupported contract kind')
        if finite(c['min'],'min')>finite(c['max'],'max'):raise ValueError('contract bounds inverted')
    for a in assets:
        seen=set()
        for p in a['properties']:
            semantic=p['semantic_id'];base={'asset_id':a['id'],'semantic_id':semantic}
            if semantic in seen:errors.append({**base,'reason':'duplicate_semantic_id'});continue
            seen.add(semantic);c=contracts.get(semantic)
            if not c:errors.append({**base,'reason':'unknown_semantic_id'});continue
            kind=c['kind'];unit=p['unit'];transform=UNITS[kind].get(unit)
            if not transform:errors.append({**base,'reason':'incompatible_unit','unit':unit});continue
            try:value=finite(p['value'],'property value')*transform[0]+transform[1]
            except ValueError:errors.append({**base,'reason':'nonfinite_value'});continue
            if not c['min']<=value<=c['max']:errors.append({**base,'reason':'value_out_of_range'});continue
            normalized.append({**base,'value':round(value,6),'unit':CANON[kind]})
        for semantic,c in contracts.items():
            if c.get('required',False) and semantic not in seen:errors.append({'asset_id':a['id'],'semantic_id':semantic,'reason':'required_property_missing'})
        for target in a.get('connected_to',[]):
            if target not in ids:errors.append({'asset_id':a['id'],'target':target,'reason':'dangling_connection'})
    return {'valid':not errors,'normalized_properties':normalized,'errors':errors,'format':'local_semantic_contract_not_aas_certification'}

if __name__ == "__main__": cli(run,'장비 의미 모델 계약 검사기')
