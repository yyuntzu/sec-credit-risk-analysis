/** Generic canonical formal-report Excel exporter. Requires bundled @oai/artifact-tool. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(process.argv[2]);
const report=JSON.parse(await fs.readFile(path.join(root,'report.json'),'utf8'));
const acceptance=JSON.parse(await fs.readFile(path.join(root,'acceptance.json'),'utf8'));
if(!acceptance.technical_validation_passed || !acceptance.rendered_validation_passed) throw Error('Unvalidated report');
for(const name of ['report.json','report.md']) {
 const digest=createHash('sha256').update(await fs.readFile(path.join(root,name))).digest('hex');
 if(acceptance.artifact_sha256?.[name]!==digest) throw Error('Stale artifact validation receipt: '+name);
}
const wb=Workbook.create();
const review=wb.worksheets.add('Review');
const source=wb.worksheets.add('Sources');
const states={missing:'缺少資料',not_calculable:'無法計算／待確認',conflict:'來源衝突',not_applicable:'經確認不適用'};
const text=value=>typeof value==='string' && value.startsWith('=') ? "'"+value : value;
const numberFormat='#,##0.00;(#,##0.00);0.00';
const format=f=>f.unit==='percent'||f.unit==='percentage_points'?'0.00%;(0.00%);0.00%':f.unit==='multiple'?'0.00"x";(0.00"x");0.00"x"':numberFormat;
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

for(const sheet of [review,source]) sheet.showGridLines=false;
review.freezePanes.freezeRows(6);source.freezePanes.freezeRows(3);
source.getRange('A1').values=[[text(`${report.entity} · 原始數值與計算來源`)]];source.mergeCells('A1:G1');
source.getRange('A2').values=[[text(`報表單位：${report.currency} / ${report.scale}；C、D 欄保留來源原值與原始 scale`)]];source.mergeCells('A2:G2');
source.getRange('A3:G3').values=[['科目／期間','報表值','原始值','原始 scale','狀態','定義／限制','來源位置／證據']];
source.getRange('A3:G3').format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:32};
const facts=Object.values(report.facts),refs={},verification=[];
facts.forEach((f,i)=>refs[f.id]=`B${i+4}`);
for(const [i,f] of facts.entries()) {
 const row=i+4;
 const loc=f.evidence_ids.map(id=>report.evidence[id]?.locator||id).join('; ');
 const explanation=f.reason||f.definition;
 source.getRangeByIndexes(row-1,0,1,7).values=[[text(f.id),null,
  f.original_value!==null && f.unit!=='text'?Number(f.original_value):text(f.original_value),
  f.original_scale!==null?Number(f.original_scale):null,states[f.status]||f.status,text(explanation),text(loc)]];
 const cell=source.getRange(refs[f.id]);
 if(f.status==='sourced' && f.unit!=='text') {
  cell.formulas=[[`=IF(AND(ISNUMBER(C${row}),ISNUMBER(D${row})),C${row}*D${row}/${f.unit==='money'?Number(report.scale):1},"缺少資料")`]];
 } else if(f.status==='calculated') {
  const checks=f.input_ids.map(id=>`ISNUMBER(${refs[id]})`).join(',');
  let expr=expression(f,refs);
  const denominator=f.formula_id==='CF-04'?`(${refs[f.input_ids[1]]}+${refs[f.input_ids[2]]})`:f.formula_id==='CF-05'?`(${refs[f.input_ids[1]]}+${refs[f.input_ids[3]]})`:expr.includes('/')?refs[f.input_ids[1]]:null;
  if(denominator) expr=`IF(${denominator}=0,"無法計算",${expr})`;
  cell.formulas=[[`=IF(AND(${checks}),${expr},"缺少資料")`]];
 } else cell.values=[[text(f.status==='sourced'?f.value:states[f.status])]];
 cell.setNumberFormat(format(f));
 source.getRange(`C${row}:D${row}`).format.font.color='#0000FF';
 source.getRange(`F${row}:G${row}`).format.wrapText=true;
 source.getRange(`A${row}:G${row}`).format.rowHeight=Math.max(30,14*Math.ceil(Math.max(explanation.length/65,loc.length/75)));
 verification.push({fid:f.id,ref:refs[f.id],expected:f.value,available:['sourced','calculated'].includes(f.status),unit:f.unit,status:f.status});
}
let evidenceRow=facts.length+6;
source.getRangeByIndexes(evidenceRow-1,0,1,7).values=[['Evidence ID','種類','Source ID','版本','文件日期','來源位置','原始證據內容']];
source.getRangeByIndexes(evidenceRow-1,0,1,7).format={fill:'#243746',font:{bold:true,color:'#FFFFFF'}};
for(const e of Object.values(report.evidence)) {
 evidenceRow++;
 source.getRangeByIndexes(evidenceRow-1,0,1,7).values=[[e.id,e.kind,e.source_id,e.version,e.document_date,e.locator,e.content].map(text)];
 source.getRange(`A${evidenceRow}:G${evidenceRow}`).format={wrapText:true,rowHeight:Math.max(32,14*Math.ceil(Math.max(e.content.length/75,e.locator.length/65)))};
}
review.getRange('A1').values=[[text(`${report.entity} · ${report.mode} · ${report.currency} / ${report.scale}`)]];
review.mergeCells('A1:G1');review.getRange('A1').format.font={bold:true,size:14};
review.getRange('A3').values=[[acceptance.final_report_accepted?'正式驗收通過':'待驗收覆核稿：'+acceptance.acceptance_blockers.join('; ')]];
review.mergeCells('A3:G3');review.getRange('A3').format={wrapText:true,rowHeight:80,font:{color:acceptance.final_report_accepted?'#243746':'#9A3412'}};
const md=await fs.readFile(path.join(root,'report.md'),'utf8');
const labels=md.split(/\n\s*\n/).filter(g=>g.startsWith('|')).map(g=>g.split('\n').slice(2).filter(l=>l.startsWith('|')).map(l=>l.split('|')[1].trim()));
let row=5; const bindings=[],reviewRanges=[];
for(const [ti,table] of report.tables.entries()) {
 const start=row;
 review.getCell(row-1,0).values=[[text(table.spec.heading)]];review.getCell(row-1,0).format.font.bold=true;row++;
 const headers=['科目',...table.spec.columns.map(role=>role.startsWith('pct:')?'營收占比':report.periods.find(p=>p.role===role).label)];
 review.getRangeByIndexes(row-1,0,1,headers.length).values=[headers.map(text)];
 review.getRangeByIndexes(row-1,0,1,headers.length).format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:36};row++;
 for(const [ri,cells] of table.cells.entries()) {
  review.getCell(row-1,0).values=[[text(labels[ti][ri])]];
  const textRow=cells.some(fid=>report.facts[fid].unit==='text');
  review.getRangeByIndexes(row-1,0,1,cells.length+1).format.wrapText=true;
  review.getRangeByIndexes(row-1,0,1,cells.length+1).format.rowHeight=textRow?80:30;
  for(const [i,fid] of cells.entries()) {
   const cell=review.getCell(row-1,i+1);
   cell.formulas=[[`='Sources'!${refs[fid]}`]];cell.setNumberFormat(format(report.facts[fid]));
   bindings.push({fid,row,col:i+1});
  }
  row++;
 }
 reviewRanges.push([table.spec.key,`A${start}:G${row}`]);
 row+=2;
}
review.getRange(`A1:G${row}`).format.font.name='Arial';review.getRange(`A3:G${row}`).format.font.size=10;
review.getRange(`A1:A${row}`).format.columnWidth=48;review.getRange(`B1:G${row}`).format.columnWidth=24;
source.getRange(`A1:G${evidenceRow}`).format.font.name='Arial';source.getRange(`A3:G${evidenceRow}`).format.font.size=10;
for(const [col,width] of [['A',40],['B',24],['C',24],['D',16],['E',28],['F',65],['G',75]]) source.getRange(`${col}1:${col}${evidenceRow}`).format.columnWidth=width;
wb.recalculate();
function verify() {
 for(const v of verification) {
  const value=source.getRange(v.ref).values[0][0];
  if(v.available && v.unit!=='text' && (!Number.isFinite(value)||Math.abs(value-Number(v.expected))>1e-8*Math.max(1,Math.abs(Number(v.expected))))) throw Error('Excel/report mismatch '+v.fid);
  if(!v.available && typeof value==='number') throw Error('Unavailable became numeric: '+v.fid);
 }
 for(const b of bindings) if(review.getCell(b.row-1,b.col).values[0][0]!==source.getRange(refs[b.fid]).values[0][0]) throw Error('Output binding mismatch');
}
verify();
const target=verification.find(v=>v.status==='sourced' && v.unit==='money');
if(target) {
 const row=target.ref.slice(1), original=source.getRange('C'+row).values[0][0], scale=source.getRange('D'+row).values[0][0];
 source.getRange('C'+row).values=[[original+Number(report.scale)/scale]];wb.recalculate();
 if(Math.abs(source.getRange(target.ref).values[0][0]-Number(target.expected)-1)>1e-8) throw Error('Source edit did not recalculate');
 source.getRange('C'+row).values=[[null]];wb.recalculate();
 if(source.getRange(target.ref).values[0][0]!=='缺少資料') throw Error('Blank became zero');
 for(const f of facts.filter(f=>f.status==='calculated' && f.input_ids.includes(target.fid)))
  if(typeof source.getRange(refs[f.id]).values[0][0]==='number') throw Error('Missing source did not propagate');
 source.getRange('C'+row).values=[[0]];wb.recalculate();
 if(source.getRange(target.ref).values[0][0]!==0) throw Error('Real zero lost');
 source.getRange('C'+row).values=[[original]];wb.recalculate();verify();
}
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:5},summary:'formula errors'});
console.log(scan.ndjson);
for(const [sheetName,range] of [['Review','A1:G17'],['Sources','A1:E12']]) {
 const image=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(path.join(root,sheetName+'_preview.png'),new Uint8Array(await image.arrayBuffer()));
}
for(const [key,range] of reviewRanges) {
 const image=await wb.render({sheetName:'Review',range,scale:1,format:'png'});
 await fs.writeFile(path.join(root,'Review_'+key+'_preview.png'),new Uint8Array(await image.arrayBuffer()));
}
const file=await SpreadsheetFile.exportXlsx(wb);await file.save(path.join(root,'loan_review.xlsx'));
await fs.writeFile(path.join(root,'excel_validation.json'),JSON.stringify({cells_checked:verification.length,output_bindings:bindings.length,passed:true,engine:'artifact-tool; native Excel not run'},null,2));
console.log('Excel export verified',verification.length);
