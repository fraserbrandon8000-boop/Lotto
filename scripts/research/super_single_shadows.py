"""Single-ticket SHADOW challengers (Super Lotto single-ticket protocol v1). Research only — never purchased.
S1 P0_standalone_top: highest standalone-scored ticket of the frozen P0 Top-12 universe (frozen constants; ties EQ then
   enumeration order) with the P0 SB order's first Super Ball.
S2 V1_pool_per_draw_seed: V1 candidate at index default_rng(2026092109 + target).integers(len(pool)) with its own SB.
Usage: super_single_shadows.py DRAWS_JSON CUTOFF CANDIDATES_JSON OUT_JSON"""
import sys,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/research'))
import super_history as S,super_p0 as P
from super_p0_apply import frozen_cred
dp,cut,cp,out=sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4];T=cut+1
Pr=json.loads((R/'results/super_lotto/p0_protocol/PROTOCOL.json').read_text());fc=Pr['frozen_constants']
records,d,sb,ids=S.load(dp);assert ids[-1]==cut
o=S.origin(d,sb,ids,len(d));cred=frozen_cred(fc);disc=P.discovery(o,cred);U=P.universe(o,disc,cred,fc['main_pool_K'])
rk=np.lexsort((np.arange(len(U['C'])),-np.round(U['EQ'],12),-np.round(U['T'],12)));s1=sorted((U['C'][rk[0]]+1).tolist())
cs=json.loads(Path(cp).read_text());i=int(np.random.default_rng(2026092109+T).integers(len(cs)));c=cs[i]
res=dict(status='SHADOW — DO NOT PURCHASE (single-ticket protocol v1 research challengers)',created_utc=datetime.now(timezone.utc).isoformat(),target=T,cutoff=cut,
  data_sha256=hashlib.sha256(Path(dp).read_bytes()).hexdigest(),candidates_sha256=hashlib.sha256(Path(cp).read_bytes()).hexdigest(),
  S1_P0_standalone_top=dict(main=s1,super_ball=disc['sborder'][0],pool=U['pool'],note='all frozen P0 credibilities are 0, so the standalone score is the equal-weight tie-break'),
  S2_V1_pool_per_draw_seed=dict(candidate=c['id'],index=i,main=c['main'],super_ball=c['super_ball'],generator=c['main_generator']))
with open(out,'x') as h:json.dump(res,h,indent=1)
print(json.dumps({k:res[k] for k in ['S1_P0_standalone_top','S2_V1_pool_per_draw_seed']},default=str))
