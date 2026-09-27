"""Read-only workbook audit; normalize explicitly sourced official additions."""
import json, csv, hashlib, argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import Counter
import openpyxl

ROOT=Path(__file__).resolve().parents[1]
DEFAULT=Path(r'C:\Data_Unbackupped\FRASEB01\Downloads\Lotto-Draw-Dataset.xlsx')
def save(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,default=str),encoding='utf-8')
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--workbook',type=Path,default=DEFAULT)
    path=parser.parse_args().workbook
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    wb=openpyxl.load_workbook(path,read_only=True,data_only=True)
    ws=wb['Lotto Draws']; rows=list(ws.values); header=next(i for i,r in enumerate(rows) if r[0]=='Draw No.')
    original=[]; errors=[]; blank_rows=[]; missing=[]
    for line,r in enumerate(rows[header+1:],header+2):
        if all(v is None for v in r): blank_rows.append(line); continue
        for col,v in enumerate(r[:10],1):
            if v is None: missing.append({'row':line,'column':col})
        if not isinstance(r[0],int): errors.append(f'Invalid draw ID row {line}'); continue
        if not isinstance(r[1],datetime): errors.append(f'Malformed date row {line}'); continue
        nums=list(r[2:8]); bonus=r[8]
        if len(nums)!=6 or any(not isinstance(x,int) or not 1<=x<=38 for x in nums): errors.append(f'Invalid main numbers row {line}')
        if len(set(nums))!=6: errors.append(f'Duplicate main numbers row {line}')
        if not isinstance(bonus,int) or not 1<=bonus<=38: errors.append(f'Invalid bonus row {line}')
        if bonus in nums: errors.append(f'Bonus repeats main number row {line}')
        original.append(dict(draw_id=r[0],date=r[1].date().isoformat(),numbers=sorted(nums),bonus=bonus,source=r[9],origin='workbook',sheet='Lotto Draws',row=line))
    ids=[r['draw_id'] for r in original]; dates=[r['date'] for r in original]
    dup_ids=[k for k,v in Counter(ids).items() if v>1]
    duplicate_records=[k for k,v in Counter((r['date'],tuple(r['numbers']),r['bonus']) for r in original).items() if v>1]
    absent=sorted(set(range(min(ids),max(ids)+1))-set(ids))
    official=[]
    for f in sorted((ROOT/'data').glob('official-20*.json')):
        payload=json.loads(f.read_text(encoding='utf-8-sig'))
        if not isinstance(payload,list): raise ValueError(f'Official API error in {f.name}')
        for day in payload:
            for period,r in day.items():
                if not r or not isinstance(r,dict) or not r.get('drawNumber'): continue
                nums=sorted(map(int,r['winNumber'].split())); bonus=int(r['bonusBall'])
                assert len(nums)==6 and len(set(nums))==6 and all(1<=n<=38 for n in nums) and 1<=bonus<=38 and bonus not in nums
                official.append(dict(draw_id=int(r['drawNumber']),date=r['drawDate'],numbers=nums,bonus=bonus,source='https://supremeventures.com/past-results/',api_source='https://test-results.supremeventures.com/public/game/5/',raw_file=str(f.relative_to(ROOT)),origin='official_archive'))
    merged={r['draw_id']:r for r in original}; added=[]; corroborated=[]; conflicts=[]
    for r in official:
        old=merged.get(r['draw_id'])
        if old:
            if any(old[k]!=r[k] for k in ['date','numbers','bonus']): conflicts.append({'workbook':old,'official':r})
            else: corroborated.append(r['draw_id'])
        else: merged[r['draw_id']]=r; added.append(r)
    data=sorted(merged.values(),key=lambda r:r['draw_id'])
    for a,b in zip(data,data[1:]):
        if a['date']>=b['date']: errors.append(f'Date not increasing: {a["draw_id"]}, {b["draw_id"]}')
    date_offsets=[]
    expected=datetime.fromisoformat(data[0]['date'])
    for r in data:
        if datetime.fromisoformat(r['date']).weekday() not in [2,5]: date_offsets.append(r['draw_id'])
    report=dict(workbook=str(path),sha256=digest,sheet='Lotto Draws',data_range=f'A{header+2}:J{len(rows)}',original_draws=len(original),first_draw=min(ids),last_draw=max(ids),first_date=min(dates),last_date=max(dates),order='descending' if ids==sorted(ids,reverse=True) else 'unsorted',dates_descending=dates==sorted(dates,reverse=True),missing_draw_ids=absent,duplicate_ids=dup_ids,duplicate_records=duplicate_records,missing_cells=missing,invalid_rows=errors,unexpected_weekday_ids=date_offsets,blank_data_rows=blank_rows,official_additions=added,official_corroborated_ids=sorted(set(corroborated)),source_conflicts=conflicts,analysis_draws=len(data),analysis_first=data[0]['date'],analysis_last=data[-1]['date'],remaining_missing_ids=sorted(set(range(data[0]['draw_id'],data[-1]['draw_id']+1))-set(merged)),retrieved_utc=datetime.now(timezone.utc).isoformat(),source_limitations='Original source column refers to a prior workbook/screenshots, not independently verified primary records. Official archive host is named test-results but is the live feed referenced by Supreme Ventures official public results page. Original rows preserved; overlaps compared.')
    save('results/audit.json',report); save('data/original_draws.json',original); save('data/external_draws.json',added); save('data/draws.json',data)
    wb.close(); assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
    print(json.dumps({k:v for k,v in report.items() if k not in ['official_additions','source_limitations']},indent=2,default=str))
    if errors or missing or dup_ids or duplicate_records or conflicts or report['remaining_missing_ids']: raise ValueError('Resolve audit issues before analysis')
if __name__=='__main__': main()
