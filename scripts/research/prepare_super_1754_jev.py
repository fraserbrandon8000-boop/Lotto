from pathlib import Path
R=Path(__file__).resolve().parents[2]
src=(R/'scripts/research/super_jev.mjs').read_text(encoding='utf-8-sig')
src=src.replace('../../results/super_lotto/','../../results/super_lotto/draw1754/')
src="import {verifiedFetch} from './super_1754_transport.mjs';\n"+src
src=src.replace("logLevel:'off',timeout:60000","logLevel:'off',timeout:60000,retry:{maxRetries:0},fetch:verifiedFetch")
old="  await writeFile(new URL('../../results/super_lotto/draw1754/jev_response.json',import.meta.url),JSON.stringify(response,null,2));"
assert old in src;src=src.replace(old,'')
src=src.replace('  const response=await client.systemOne(request);','  const response=await client.systemOne(request);\n'+old.replace('JSON.stringify(response,null,2));',"JSON.stringify(response,null,2),{flag:'wx'});"))
(R/'scripts/research/super_1754_jev.mjs').write_text(src,encoding='utf-8')
print('Identical V1 question framework; isolated paths, one-attempt transport and first-response preservation added.')
