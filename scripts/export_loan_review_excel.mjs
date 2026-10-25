/** Export validated report artifacts with the bundled @oai/artifact-tool runtime.
 * Usage: node export_loan_review_excel.mjs ARTIFACT_ROOT
 * Keep Quarter Q1/Q2 separate sections; source statuses are never numeric zero.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const root = path.resolve(process.argv[2]);
const wb = Workbook.create();
const states = {missing:'缺少資料',not_calculable:'無法計算／待確認',conflict:'來源衝突',not_applicable:'經確認不適用'};
const numberFormat = '#,##0.00;(#,##0.00);0.00';
function expression(f, refs) {
  const x=f.input_ids.map(id=>refs[id]);
  if(x.some(v=>!v)) throw Error('Missing formula lineage');
  const [a,b,c,d]=x;
  switch(f.formula_id) {
    case 'CF-04': return `(${a}+${b})/(${b}+${c})`;
    case 'CF-05': return `(${a}+${b}+${c})/(${b}+${d})`;
    case 'CF-09': return `(${a}-${b})/${b}`;
    case 'CF-16': case 'CASH-CHANGE-v1': case 'DER-01': case 'DER-02': case 'DER-03': case 'DER-04': case 'DER-06': return `${a}-${b}`;
    case 'DER-05': return `${a}+${b}`;
    case 'STANDARD-EBITDA-v1': return `${a}+${b}+${c}+${d}`;
    case 'CF-01': case 'CF-02': case 'CF-03': case 'CF-06': case 'CF-10': case 'CF-11': case 'CF-12': case 'COMMON-SIZE-v1': case 'LEVERAGE-v1': return `${a}/${b}`;
    default: throw Error(`Unimplemented Excel formula ${f.formula_id}`);
  }
}
const verification=[];
for(const [name, folders] of [['Quarter',['Quarter_Q1','Quarter_Q2']],['Year',['Year']]]) {
 const sheet=wb.worksheets.add(name); sheet.showGridLines=false;
 let row=2; const cases=[];
 for(const folder of folders) {
  const report=JSON.parse(await fs.readFile(path.join(root,folder,'report.json'),'utf8'));
  const acceptance=JSON.parse(await fs.readFile(path.join(root,folder,'acceptance.json'),'utf8'));
  if(!acceptance.technical_validation_passed || !acceptance.rendered_validation_passed) throw Error('Unvalidated report');
  if(Number(report.scale)!==1000000) throw Error('Expected millions');
  const md=await fs.readFile(path.join(root,folder,'report.md'),'utf8');
  const labelGroups=md.split(/\n\s*\n/).filter(g=>g.startsWith('|')).map(g=>g.split('\n').slice(2).filter(l=>l.startsWith('|')).map(l=>l.split('|')[1].trim()));
  sheet.getCell(row-1,0).values=[[`Nexstar ${folder}（百萬美元）`]];
  sheet.getCell(row-1,0).format.font={bold:true,size:14}; row++;
  sheet.getCell(row-1,0).values=[['待驗收：SEC來源、現金流期間與勾稽仍未完成。']]; row+=2;
  const outputs=[];
  for(let ti=0;ti<report.tables.length;ti++) {
   const t=report.tables[ti];
   sheet.getCell(row-1,0).values=[[t.spec.heading]]; row++;
   const headers=['科目',...t.spec.columns.map(role=>role.startsWith('pct:')?'營收占比':report.periods.find(p=>p.role===role).label)];
   sheet.getRangeByIndexes(row-1,0,1,headers.length).values=[headers];
   sheet.getRangeByIndexes(row-1,0,1,headers.length).format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:40}; row++;
   for(let ri=0;ri<t.cells.length;ri++) {
    sheet.getCell(row-1,0).values=[[labelGroups[ti][ri]]];
    t.cells[ri].forEach((fid,i)=>outputs.push({fid,row,col:i+1})); row++;
   }
   row+=2;
  }
  cases.push({folder,report,outputs});
 }
 row+=2;
 sheet.getCell(row-1,0).values=[['來源與計算明細：原值保留，核准不代表來源已核實']]; row+=2;
 const cols=['案例／科目／期間','報表值','原始值','來源金額單位','狀態','定義／限制','來源儲存格／證據'];
 sheet.getRangeByIndexes(row-1,0,1,7).values=[cols]; sheet.getRangeByIndexes(row-1,0,1,7).format={fill:'#243746',font:{bold:true,color:'#FFFFFF'}}; row++;
 for(const {folder,report,outputs} of cases) {
  const refs={};
  for(const f of Object.values(report.facts)) refs[f.id]=`B${row++}`;
  const start=row-Object.keys(refs).length;
  let r=start;
  for(const f of Object.values(report.facts)) {
   const loc=f.evidence_ids.map(id=>report.evidence[id]?.locator||id).join('; ');
   sheet.getRangeByIndexes(r-1,0,1,7).values=[[`${folder}/${f.metric}/${f.period_role}`,null,
    typeof f.original_value==='string' && f.unit!=='text'?Number(f.original_value):f.original_value,
    f.original_scale?Number(f.original_scale):null,states[f.status]||f.status,f.reason||f.definition,loc]];
   const cell=sheet.getRange(refs[f.id]);
   if(f.status==='sourced' && f.unit!=='text') {
    const divisor=f.unit==='money'?1000000:1;
    cell.formulas=[[`=IF(AND(ISNUMBER(C${r}),ISNUMBER(D${r})),C${r}*D${r}/${divisor},"缺少資料")`]];
   } else if(f.status==='calculated') {
    const checks=f.input_ids.map(id=>`ISNUMBER(${refs[id]})`).join(',');
    let expr=expression(f,refs);
    // Expected denominator zero is unavailable; all other errors remain visible.
    const denominator=f.formula_id==='CF-04'?`(${refs[f.input_ids[1]]}+${refs[f.input_ids[2]]})`:f.formula_id==='CF-05'?`(${refs[f.input_ids[1]]}+${refs[f.input_ids[3]]})`:expr.includes('/')?refs[f.input_ids[1]]:null;
    if(denominator) expr=`IF(${denominator}=0,"無法計算",${expr})`;
    cell.formulas=[[`=IF(AND(${checks}),${expr},"缺少資料")`]];
   } else cell.values=[[f.status==='sourced'?f.value:states[f.status]]];
   const fmt=f.unit==='percent'||f.unit==='percentage_points'?'0.00%;(0.00%);0.00%':f.unit==='multiple'?'0.00"x";(0.00"x");0.00"x"':numberFormat;
   cell.setNumberFormat(fmt);
   verification.push({sheet:name,ref:refs[f.id],expected:f.value,available:['sourced','calculated'].includes(f.status),unit:f.unit});
   r++;
  }
  for(const o of outputs) {
   const f=report.facts[o.fid]; const cell=sheet.getCell(o.row-1,o.col);
   cell.formulas=[[`=${refs[o.fid]}`]];
   cell.setNumberFormat(f.unit==='percent'?'0.00%;(0.00%);0.00%':f.unit==='multiple'?'0.00"x";(0.00"x");0.00"x"':numberFormat);
  }
 }
 sheet.getRange(`A2:G${row}`).format.font.name='Arial';
 sheet.getRange(`A2:G${row}`).format.font.size=10;
 sheet.getRange(`A2:A${row}`).format.columnWidth=55;
 sheet.getRange(`B2:E${row}`).format.columnWidth=25;
 sheet.getRange(`F2:G${row}`).format.columnWidth=75;
 sheet.getRange(`F2:G${row}`).format.wrapText=true;
 sheet.freezePanes.freezeRows(6);
}
wb.recalculate();
for(const v of verification) {
 const value=wb.worksheets.getItem(v.sheet).getRange(v.ref).values[0][0];
 if(v.available && v.unit!=='text' && (!Number.isFinite(value) || Math.abs(Number(value)-Number(v.expected))>1e-8*Math.max(1,Math.abs(Number(v.expected))))) throw Error('Excel/report mismatch '+v.ref);
 if(!v.available && typeof value==='number') throw Error('Unavailable became number');
}
const year=wb.worksheets.getItem('Year');
const target=verification.find(v=>v.sheet==='Year' && v.available && v.unit==='money');
const sourceRow=target.ref.slice(1);
const original=year.getRange('C'+sourceRow).values[0][0];
year.getRange('C'+sourceRow).values=[[original+1000]];
wb.recalculate();
if(Math.abs(year.getRange(target.ref).values[0][0]-Number(target.expected)-1)>1e-8) throw Error('Source edit did not recalculate');
year.getRange('C'+sourceRow).values=[[null]];
wb.recalculate();
if(year.getRange(target.ref).values[0][0] !== '缺少資料') throw Error('Blank source became zero');
year.getRange('C'+sourceRow).values=[[0]];
wb.recalculate();
if(year.getRange(target.ref).values[0][0] !== 0) throw Error('Real zero lost');
year.getRange('C'+sourceRow).values=[[original]];
wb.recalculate();
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:5},summary:'formula errors'})).ndjson);
for(const sheetName of ['Quarter','Year']) {
 const image=await wb.render({sheetName,range:'A2:G17',scale:1,format:'png'});
 await fs.writeFile(path.join(root,sheetName+'_preview.png'),new Uint8Array(await image.arrayBuffer()));
}
const file=await SpreadsheetFile.exportXlsx(wb); await file.save(path.join(root,'Nexstar_核准口徑驗證.xlsx'));
await fs.writeFile(path.join(root,'excel_validation.json'),JSON.stringify({cells_checked:verification.length,passed:true,engine:'artifact-tool; native Excel not run'},null,2));
console.log('Excel export verified',verification.length);
