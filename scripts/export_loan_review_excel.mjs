/** Generic canonical formal-report Excel exporter. Requires bundled @oai/artifact-tool. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(process.argv[2]);
const report=JSON.parse(await fs.readFile(path.join(root,'report.json'),'utf8'));
const candidate=process.argv[3]==='--warehouse-candidate';
if(process.argv[3] && !candidate) throw Error('Unknown Excel export mode');
const receiptHash=candidate?process.argv[4]:null;
const preview=candidate?JSON.parse(await fs.readFile(path.join(root,'preview_manifest.json'),'utf8')):null;
if(candidate && (!/^[a-f0-9]{64}$/.test(receiptHash||'') || preview.calculation_receipt_sha256!==receiptHash
 || preview.engine!=='dbt-bigquery-candidate' || preview.publication_eligible!==false || preview.precision_approved!==false
 || preview.final_report_accepted!==false)) throw Error('Unvalidated warehouse candidate');
if(candidate) for(const [name,expected] of Object.entries(preview.artifacts)) {
 if(!['report.json','report.md','dashboard.html','commentary.json','ratio_commentary_analysis.json'].includes(name)) throw Error('Unexpected candidate input artifact');
 const digest=createHash('sha256').update(await fs.readFile(path.join(root,name))).digest('hex');
 if(digest!==expected) throw Error('Stale candidate artifact: '+name);
}
const acceptance=candidate?{technical_validation_passed:true,rendered_validation_passed:true,
 final_report_accepted:false,acceptance_blockers:['影子覆核稿。倉儲數字固定保留，Sources 僅供本機試算，不回寫倉儲。精度與正式切換尚未核准。']}
 :JSON.parse(await fs.readFile(path.join(root,'acceptance.json'),'utf8'));
if(!acceptance.technical_validation_passed || !acceptance.rendered_validation_passed) throw Error('Unvalidated report');
if(!candidate) for(const name of ['report.json','report.md','commentary.json']) {
 const digest=createHash('sha256').update(await fs.readFile(path.join(root,name))).digest('hex');
 if(acceptance.artifact_sha256?.[name]!==digest) throw Error('Stale artifact validation receipt: '+name);
}
const commentary=JSON.parse(await fs.readFile(path.join(root,'commentary.json'),'utf8'));
const wb=Workbook.create();
const review=wb.worksheets.add('Review');
const source=wb.worksheets.add('Sources');
const warehouse=candidate?wb.worksheets.add('Warehouse'):null;
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

for(const sheet of [review,source,...(warehouse?[warehouse]:[])]) sheet.showGridLines=false;
review.freezePanes.freezeRows(6);source.freezePanes.freezeRows(3);
source.getRange('A1').values=[[text(`${report.entity} · ${candidate?'本機試算與原始來源':'原始數值與計算來源'}`)]];source.mergeCells('A1:G1');
source.getRange('A2').values=[[text(`報表單位：${report.currency} / ${report.scale}；C、D 欄保留來源原值與原始 scale`)]];source.mergeCells('A2:G2');
source.getRange('A3:G3').values=[['科目／期間','報表值','原始值','原始 scale','狀態','定義／限制','來源位置／證據']];
source.getRange('A3:G3').format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:32};
const facts=Object.values(report.facts),refs={},verification=[];
if(candidate) facts.sort((a,b)=>a.id.localeCompare(b.id,'en'));
const canonicalRefs={};
facts.forEach((f,i)=>refs[f.id]=`B${i+4}`);
if(warehouse) {
 warehouse.freezePanes.freezeRows(8);
 for(const [row,value] of [[1,`${report.entity} 倉儲固定結果`],[2,`Run ${preview.bindings.run_id}`],
  [3,`計算收據 ${receiptHash}`],[4,'保留原始精度字串。B 欄為 Excel 可表示的近似值。Sources 試算不改變本表。'],
  [5,`來源 ${preview.bindings.source_hash}`],[6,`公式 ${preview.bindings.formula_version} / 精度 ${preview.bindings.precision_version}`]]) {
  warehouse.mergeCells(`A${row}:F${row}`);warehouse.getRange(`A${row}`).values=[[text(value)]];
  warehouse.getRange(`A${row}:F${row}`).format={wrapText:true,rowHeight:row===3||row===5||row===6?34:26};
 }
 warehouse.getRange('A8:L8').values=[['Fact ID','倉儲值（Excel）','倉儲值（完整字串）','原始值（Fact 字串）','原始 scale（Fact 字串）','狀態','公式／版本','有序輸入 IDs','證據 IDs','單位／幣別','期間角色／起訖','Basis']];
 warehouse.getRange('A8:L8').format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:38};
 warehouse.getRange('A8:L8').format.horizontalAlignment='center';
 facts.forEach((f,i)=>{
  const row=i+9;canonicalRefs[f.id]=`B${row}`;
  const available=['sourced','calculated'].includes(f.status);
  warehouse.getRange(`A${row}:L${row}`).values=[[text(f.id),available?(f.unit==='text'?text(f.value):Number(f.value)):states[f.status],
   f.value===null?null:text(String(f.value)),f.original_value===null?null:text(String(f.original_value)),
   f.original_scale===null?null:text(String(f.original_scale)),states[f.status]||f.status,
   text([f.formula_id,f.formula_version].filter(Boolean).join(' / ')),text(JSON.stringify(f.input_ids)),text(JSON.stringify(f.evidence_ids)),
   text([f.unit,f.currency].filter(Boolean).join(' / ')),text(`${f.period_role} / ${f.start||''} / ${f.end||''}`),text(f.basis)]];
  warehouse.getRange(`B${row}`).setNumberFormat(format(f));
  warehouse.getRange(`C${row}:E${row}`).setNumberFormat('@');
  warehouse.getRange(`C${row}:F${row}`).format.horizontalAlignment='right';
 });
 warehouse.getRange(`A9:L${facts.length+8}`).format={wrapText:true,rowHeight:54,verticalAlignment:'center'};
 facts.forEach((f,i)=>warehouse.getRange(`A${i+9}:L${i+9}`).format.rowHeight=Math.max(30,14*Math.ceil(Math.max(
  f.id.length/40,String(f.value??'').length/48,JSON.stringify(f.input_ids).length/65,JSON.stringify(f.evidence_ids).length/65,f.basis.length/60))));
 warehouse.getRange(`A1:L${facts.length+8}`).format.font={name:'Arial',size:10};
 for(const [col,width] of [['A',40],['B',24],['C',48],['D',40],['E',24],['F',26],['G',50],['H',65],['I',65],['J',22],['K',54],['L',60]])
  warehouse.getRange(`${col}1:${col}${facts.length+8}`).format.columnWidth=width;
 source.getRange('L2').values=[['Excel 試算相對誤差界限（不核准倉儲精度）']];source.getRange('M2').values=[[1e-12]];
 source.getRange('L2:M2').format={wrapText:true,rowHeight:48};source.getRange('M2').setNumberFormat('0.00E+00');
 source.getRange('H3:K3').values=[['倉儲固定值','試算差額','試算相對差額','本機試算比較']];
 source.getRange('H3:K3').format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:32};
}
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
 if(warehouse) {
  source.getRange(`H${row}`).formulas=[[`='Warehouse'!${canonicalRefs[f.id]}`]];
  source.getRange(`H${row}`).setNumberFormat(format(f));source.getRange(`H${row}`).format.font.color='#008000';
  source.getRange(`I${row}`).formulas=[[`=IF(AND(ISNUMBER(B${row}),ISNUMBER(H${row})),B${row}-H${row},"不可比較")`]];
  source.getRange(`J${row}`).formulas=[[`=IF(ISNUMBER(I${row}),I${row}/MAX(1,ABS(H${row})),"不可比較")`]];
  source.getRange(`K${row}`).formulas=[[`=IF(ISNUMBER(J${row}),IF(ABS(J${row})<=$M$2,"試算誤差範圍內","超出試算誤差"),"不可比較")`]];
  source.getRange(`I${row}:J${row}`).setNumberFormat('0.00E+00');
  source.getRange(`E${row}`).format.horizontalAlignment='center';
  source.getRange(`J${row}`).conditionalFormats.addCustom(`ABS(J${row})>$M$2`,{fill:'#FEE2E2',font:{color:'#991B1B',bold:true}});
 }
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
   cell.formulas=[[warehouse?`='Warehouse'!${canonicalRefs[fid]}`:`='Sources'!${refs[fid]}`]];cell.setNumberFormat(format(report.facts[fid]));
   bindings.push({fid,row,col:i+1});
  }
  row++;
 }
 for(const entry of commentary.filter(n=>n.table===table.spec.key)) {
  const paragraphs=[entry.display.text,...entry.display.sources.map(s=>`${s.quote}\n來源：${s.source_id} · ${s.document_date} · ${s.locator}`)];
  // Split long source paragraphs so Excel's row-height limit does not clip text.
  for(const paragraph of paragraphs) for(let pos=0;pos<paragraph.length;pos+=400) {
   const line=paragraph.slice(pos,pos+400);
   review.mergeCells(`A${row}:G${row}`);review.getRange(`A${row}`).values=[[text(line)]];
   review.getRange(`A${row}:G${row}`).format={wrapText:true,rowHeight:Math.max(36,18*Math.ceil(line.length/65)),font:{color:entry.display.reviewed?'#243746':'#9A3412'}};
   row++;
  }
 }
 reviewRanges.push([table.spec.key,`A${start}:G${row}`]);
 row+=2;
}
review.getRange(`A1:G${row}`).format.font.name='Arial';review.getRange(`A3:G${row}`).format.font.size=10;
review.getRange(`A1:A${row}`).format.columnWidth=48;review.getRange(`B1:G${row}`).format.columnWidth=24;
source.getRange(`A1:G${evidenceRow}`).format.font.name='Arial';source.getRange(`A3:G${evidenceRow}`).format.font.size=10;
for(const [col,width] of [['A',40],['B',24],['C',24],['D',16],['E',28],['F',65],['G',75]]) source.getRange(`${col}1:${col}${evidenceRow}`).format.columnWidth=width;
if(warehouse) for(const col of ['H','I','J','K','L','M']) source.getRange(`${col}1:${col}${facts.length+3}`).format.columnWidth=col==='L'?44:26;
wb.recalculate();
function verify() {
 for(const v of verification) {
  const value=source.getRange(v.ref).values[0][0];
  if(v.available && v.unit!=='text' && (!Number.isFinite(value)||Math.abs(value-Number(v.expected))>1e-8*Math.max(1,Math.abs(Number(v.expected))))) throw Error('Excel/report mismatch '+v.fid);
  if(!v.available && typeof value==='number') throw Error('Unavailable became numeric: '+v.fid);
 }
 for(const b of bindings) if(review.getCell(b.row-1,b.col).values[0][0]!==
   (warehouse?warehouse.getRange(canonicalRefs[b.fid]):source.getRange(refs[b.fid])).values[0][0]) throw Error('Output binding mismatch');
}
verify();
const target=verification.find(v=>v.status==='sourced' && v.unit==='money');
if(target) {
 const row=target.ref.slice(1), original=source.getRange('C'+row).values[0][0], scale=source.getRange('D'+row).values[0][0];
 source.getRange('C'+row).values=[[original+Number(report.scale)/scale]];wb.recalculate();
 if(Math.abs(source.getRange(target.ref).values[0][0]-Number(target.expected)-1)>1e-8) throw Error('Source edit did not recalculate');
 if(warehouse && warehouse.getRange(canonicalRefs[target.fid]).values[0][0]!==Number(target.expected)) throw Error('Local trial changed canonical snapshot');
 source.getRange('C'+row).values=[[null]];wb.recalculate();
 if(source.getRange(target.ref).values[0][0]!=='缺少資料') throw Error('Blank became zero');
 for(const f of facts.filter(f=>f.status==='calculated' && f.input_ids.includes(target.fid)))
  if(typeof source.getRange(refs[f.id]).values[0][0]==='number') throw Error('Missing source did not propagate');
 source.getRange('C'+row).values=[[0]];wb.recalculate();
 if(source.getRange(target.ref).values[0][0]!==0) throw Error('Real zero lost');
 source.getRange('C'+row).values=[[original]];wb.recalculate();verify();
}
for(const sheet of [review,source,...(warehouse?[warehouse]:[])]) for(const values of sheet.getUsedRange().values) for(const value of values)
 if(typeof value==='string' && /^#(?:REF!|DIV\/0!|VALUE!|NAME\?|NUM!|N\/A|NULL!|SPILL!|CALC!)$/.test(value)) throw Error('Unexpected spreadsheet formula error: '+value);
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:5},summary:'formula errors'});
console.log(scan.ndjson);
for(const [sheetName,range] of [['Review','A1:G17'],['Sources',warehouse?'A1:G12':'A1:E12']]) {
 const image=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(path.join(root,sheetName+'_preview.png'),new Uint8Array(await image.arrayBuffer()));
}
for(const [key,range] of reviewRanges) {
 const image=await wb.render({sheetName:'Review',range,scale:1,format:'png'});
 await fs.writeFile(path.join(root,'Review_'+key+'_preview.png'),new Uint8Array(await image.arrayBuffer()));
}
const file=await SpreadsheetFile.exportXlsx(wb);await file.save(path.join(root,'loan_review.xlsx'));
if(warehouse) {
 const image=await wb.render({sheetName:'Warehouse',range:'A1:F14',scale:1,format:'png'});
 await fs.writeFile(path.join(root,'Warehouse_preview.png'),new Uint8Array(await image.arrayBuffer()));
}
const audit=warehouse?verification.map(v=>({fact_id:v.fid,canonical_value:v.expected,trial_value:source.getRange(v.ref).values[0][0],
 source_address:v.ref,
 canonical_excel_value:warehouse.getRange(canonicalRefs[v.fid]).values[0][0],canonical_address:canonicalRefs[v.fid],
 exact_address:'C'+canonicalRefs[v.fid].slice(1),original_exact_address:'D'+canonicalRefs[v.fid].slice(1),scale_exact_address:'E'+canonicalRefs[v.fid].slice(1)})):undefined;
await fs.writeFile(path.join(root,'excel_validation.json'),JSON.stringify({cells_checked:verification.length,output_bindings:bindings.length,commentary_entries:commentary.length,
 passed:true,engine:'artifact-tool; native Excel not run',...(warehouse?{calculation_receipt_sha256:receiptHash,precision_approved:false,publication_eligible:false,
 canonical_snapshot_unchanged_after_trial_edit:true,rows:audit,review_bindings:bindings.map(b=>({fact_id:b.fid,row:b.row,col:b.col,address:String.fromCharCode(65+b.col)+b.row,
 formula:`'Warehouse'!${canonicalRefs[b.fid]}`}))}:{})},null,2));
console.log('Excel export verified',verification.length);
