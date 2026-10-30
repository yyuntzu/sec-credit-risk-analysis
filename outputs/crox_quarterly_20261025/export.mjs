import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const root=new URL('./',import.meta.url);
const report=JSON.parse(await fs.readFile(new URL('review/report.json',root),'utf8'));
const md=await fs.readFile(new URL('review/report.md',root),'utf8');
const wb=Workbook.create(),s=wb.worksheets.add('Quarter');s.showGridLines=false;
const states={missing:'缺少資料',not_calculable:'無法計算／待確認',conflict:'來源衝突',not_applicable:'經確認不適用'};
const facts=Object.values(report.facts),refs={};
const first=85;
facts.forEach((f,i)=>refs[f.id]=`B${first+i}`);
const fmt=f=>f.unit==='percent'?'0.00%;(0.00%);0.00%':f.unit==='multiple'?'0.00"x";(0.00"x");0.00"x"':'#,##0.00;(#,##0.00);0.00';
function formula(f){const x=f.input_ids.map(id=>refs[id]);if(x.some(v=>!v))throw Error('Missing input');const[a,b,c,d]=x;switch(f.formula_id){case 'CF-01':case 'CF-02':case 'CF-06':case 'CF-10':case 'CF-11':case 'CF-12':case 'COMMON-SIZE-v1':case 'LEVERAGE-v1':return `=${a}/${b}`;case 'CF-09':return `=(${a}-${b})/${b}`;case 'CF-16':case 'DER-01':case 'DER-02':case 'DER-03':case 'DER-04':return `=${a}-${b}`;case 'STANDARD-EBITDA-v1':return `=${a}+${b}+${c}+${d}`;default:throw Error(f.formula_id)}}
s.getRange('A2').values=[['Crocs（CROX）信用分析']];s.getRange('A2').format.font={size:15,bold:true};
s.getRange('A3').values=[['B. Quarterly Review — Financial Analysis']];
s.getRange('A4').values=[['USD 百萬元。Q2 損益採上半年累計。資料截止日：2026-10-25。']];
s.getRange('A5').values=[['待驗收草稿：速動資產核實及完整勾稽仍未完成。']];
s.getRange('A6').values=[['本次嚴格流程使用 SEC 本地快照；未執行 BQ／GCS 落地或 dbt。']];
const groups=md.split(/\n\s*\n/).filter(g=>g.startsWith('|')).map(g=>g.split('\n').slice(2).filter(l=>l.startsWith('|')).map(l=>l.split('|')[1].trim()));
let row=9;const checks=[];
for(let ti=0;ti<report.tables.length;ti++){
 const t=report.tables[ti];s.getCell(row-1,0).values=[[t.spec.heading]];s.getRange(`A${row}:E${row}`).format={fill:'#E6EBF0',font:{bold:true}};row++;
 s.getRange(`A${row}:E${row}`).values=[['科目',...t.spec.columns.map(role=>role.startsWith('pct:')?'營收占比':report.periods.find(p=>p.role===role).label)]];
 s.getRange(`A${row}:E${row}`).format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},horizontalAlignment:'center',rowHeight:28};row++;
 for(let ri=0;ri<t.cells.length;ri++){
  s.getCell(row-1,0).values=[[groups[ti][ri]]];
  t.cells[ri].forEach((id,j)=>{const f=report.facts[id],cell=s.getCell(row-1,j+1);if(f.unit==='text'&&f.status==='sourced'){cell.values=[[f.value]];cell.format={wrapText:true,rowHeight:58};}else if(['sourced','calculated'].includes(f.status)&&f.value!==null){cell.formulas=[[`=${refs[id]}`]];checks.push({address:String.fromCharCode(66+j)+row,value:Number(f.value)});cell.setNumberFormat(fmt(f));}else cell.values=[[states[f.status]||f.reason]];});row++;
 }
 row++;
 for(const n of t.narratives){s.getCell(row-1,0).values=[[n.status==='supported'?n.text:`${n.topic}：${n.reason}`]];s.getRange(`A${row}:E${row}`).merge();s.getRange(`A${row}:E${row}`).format={wrapText:true,rowHeight:36};row++;}
 if(ti===0){s.getRange(`A${row}:E${row}`).merge();s.getRange(`A${row}`).values=[['2025上半年含減損 USD 738.12m，2026上半年為 USD 3.30m；營業利益回升不等同本業等幅成長。來源：2026 Q2 10-Q，Goodwill and Asset impairments。']];s.getRange(`A${row}:E${row}`).format={wrapText:true,rowHeight:42};row+=2;}
 row+=2;
}
if(row>=82)throw Error('Source block overlap');
s.getRange('A82').values=[['計算輸入與逐項來源（保持原始精度）']];
s.getRange('A84:H84').values=[['Fact ID','數值／狀態','單位','起日','迄日','定義／公式','來源／限制','來源定位']];
facts.forEach((f,i)=>{const r=first+i;const ev=f.evidence_ids.map(id=>report.evidence[id]).filter(Boolean);s.getRange(`A${r}:H${r}`).values=[[f.id,['sourced','calculated'].includes(f.status)&&f.value!==null?(f.unit==='text'?f.value:Number(f.value)):(states[f.status]||f.status),f.unit,f.start||'',f.end||'',f.formula_id||f.definition,ev.map(e=>e.source_id).join('; ')||f.reason,ev.map(e=>e.locator).join('; ')]];if(f.status==='calculated')s.getRange(`B${r}`).formulas=[[formula(f)]];s.getRange(`B${r}`).setNumberFormat(fmt(f));});
s.getRange(`A2:H${first+facts.length}`).format.font.name='Arial';s.getRange(`A3:H${first+facts.length}`).format.font.size=10;
s.getRange('A:A').format.columnWidth=51;s.getRange('B:E').format.columnWidth=25;s.getRange('F:H').format.columnWidth=40;s.getRange('A4:A6').format.font.size=10; for(const r of [4,5,6]){s.getRange(`A${r}:E${r}`).merge();s.getRange(`A${r}:E${r}`).format={wrapText:true,rowHeight:28};}
s.getRange('A5:A6').format.font.color='#9C3D10';s.getRange('B10:E80').format.horizontalAlignment='right';
wb.recalculate();
for(const c of checks){const actual=s.getRange(c.address).values[0][0];if(typeof actual!=='number'||Math.abs(actual-c.value)>Math.max(1e-8,Math.abs(c.value)*1e-10))throw Error(`Mismatch ${c.address}: ${actual}`);}
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:20},maxChars:2000});
await fs.writeFile(new URL('excel_validation.json',root),JSON.stringify({checkedOutputCells:checks.length,errors:errors.ndjson}));
console.log((await wb.inspect({kind:'table',range:'Quarter!A10:E20',include:'values,formulas',tableMaxRows:3,tableMaxCols:5,maxChars:1200})).ndjson);
const preview=await wb.render({sheetName:'Quarter',range:'A2:E72',scale:1.5,format:'png'});await fs.writeFile(new URL('preview.png',root),new Uint8Array(await preview.arrayBuffer()));
await(await SpreadsheetFile.exportXlsx(wb)).save(fileURLToPath(new URL('CROX_credit_review.xlsx',root)));
console.log(`Exported workbook; ${checks.length} numeric output cells verified against strict report.`);
