import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=new URL('./',import.meta.url);
const d=JSON.parse(await fs.readFile(new URL('review_data.json',root),'utf8'));
const evidence=JSON.parse(await fs.readFile(new URL('source_evidence.json',root),'utf8'));
const wb=Workbook.create(),s=wb.worksheets.add('Quarter');s.showGridLines=false;
const key=(t,a,b)=>`${t}|${a||''}|${b}`;
const unique=[...new Map(evidence.financial.map(x=>[key(x.tag,x.start,x.end),x])).values()];
const refs=new Map(unique.map((x,i)=>[key(x.tag,x.start,x.end),`B${100+i}`]));
const ref=(tag,start,end)=>{const r=refs.get(key(tag,start,end));if(!r)throw Error(key(tag,start,end));return r;};
const money='#,##0.00;(#,##0.00);0.00',pct='0.00%;(0.00%);0.00%';
const checks=[];
s.getRange('A2').values=[['Amazon（AMZN）信用分析']];
s.getRange('A2').format.font={size:15,bold:true};
const text=(row,t,height=34)=>{s.getRange(`A${row}:E${row}`).merge();s.getRange(`A${row}`).values=[[t]];s.getRange(`A${row}:E${row}`).format={wrapText:true,rowHeight:height};};
text(3,'USD 百萬元｜合併範圍｜截止日 2026-10-25｜master 分支',24);
text(4,'依要求保留 FY2024、Q1 2025、FY2025、Q2 2026。損益分別為 3 個月與 6 個月，禁止直接計算兩欄成長率。',34);
text(5,'待驗收草稿：速動資產及總債務／融資租賃調節未完成；dbt 執行失敗；既有 marts 未視為本次驗收通過。',34);
text(6,'來源：本次 SEC → BigQuery／GCS；數值按新入庫 fact IDs 讀回核對。MD&A 已完成 API 分析並另行審閱。',34);
const header=(row,values)=>{s.getRange(`A${row}:E${row}`).values=[values];s.getRange(`A${row}:E${row}`).format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:36,horizontalAlignment:'center'};};
text(8,'YTD (Quarterly) Income',24);
header(9,['科目','Q1 2025 YTD (3 months)','% sales','Q2 2026 YTD (6 months)','% sales']);
const tags={revenue:'RevenueFromContractWithCustomerExcludingAssessedTax',cost:'CostOfGoodsAndServicesSold',operating_income:'OperatingIncomeLoss',interest:'InterestExpenseNonoperating',tax:'IncomeTaxExpenseBenefit',net_income:'NetIncomeLoss',da:'DepreciationDepletionAndAmortization'};
function expr(metric,y,end){const start=`${y}-01-01`;const r=k=>ref(tags[k],start,end);if(metric==='gross_profit')return `${r('revenue')}-${r('cost')}`;if(metric==='operating_expense')return `${r('revenue')}-${r('cost')}-${r('operating_income')}`;if(metric==='pretax')return `${r('net_income')}+${r('tax')}`;return r(metric);}
d.income_rows.forEach(([label,k],i)=>{const row=10+i;s.getRange(`A${row}`).values=[[label]];for(const [pi,c,pc] of [[1,'B','C'],[3,'D','E']]){const p=d.periods[pi];s.getRange(`${c}${row}`).formulas=[[`=${expr(k,p.year,p.end)}`]];s.getRange(`${pc}${row}`).formulas=[[`=${c}${row}/${ref(tags.revenue,`${p.year}-01-01`,p.end)}`]];s.getRange(`${c}${row}`).setNumberFormat(money);s.getRange(`${pc}${row}`).setNumberFormat(pct);checks.push({cell:`${c}${row}`,value:Number(p.values[k])});}});
let row=20;
for(const n of d.income_notes)text(row++,n,50);
text(26,'Ratios YTD',24);
header(27,['科目',...d.periods.map(x=>x.end)]);
for(let i=0;i<4;i++){
 const p=d.periods[i],c=String.fromCharCode(66+i),r=t=>ref(t,null,p.end);
 s.getRange(`${c}28`).formulas=[[`=${r('AssetsCurrent')}/${r('LiabilitiesCurrent')}`]];
 s.getRange(`${c}29`).values=[['待核實 Quick Assets']];
 s.getRange(`${c}30`).formulas=[[`=(${r('Assets')}-${r('StockholdersEquity')})/${r('StockholdersEquity')}`]];
 for(const [rr,k] of [[28,'current_ratio'],[30,'debt_ratio']]){s.getRange(`${c}${rr}`).setNumberFormat(pct);checks.push({cell:`${c}${rr}`,value:Number(p.values[k])});}
}
s.getRange('A28:A30').values=[['Current ratio'],['Quick ratio'],['Debt ratio (liabilities / equity)']];
d.ratio_notes.forEach((n,i)=>text(32+i,n,46));
text(35,'Leverage Analysis YTD',24);header(36,['科目',...d.periods.map(x=>x.end)]);
s.getRange('A37:A40').values=[['Total debt'],['LTM Standard EBITDA'],['EBITDA basis'],['Total leverage']];
const eb=(y,end)=>['net_income','interest','tax','da'].map(k=>expr(k,y,end)).join('+');
for(let i=0;i<4;i++){
 const p=d.periods[i],c=String.fromCharCode(66+i);
 s.getRange(`${c}37`).values=[['待核實借款／融資租賃']];
 const e=p.end.endsWith('12-31')?eb(p.year,p.end):`(${eb(p.year-1,`${p.year-1}-12-31`)})+(${eb(p.year,p.end)})-(${eb(p.year-1,`${p.year-1}${p.end.slice(4)}`)})`;
 s.getRange(`${c}38`).formulas=[[`=${e}`]];s.getRange(`${c}38`).setNumberFormat(money);
 s.getRange(`${c}39`).values=[['Net Income + Interest + Taxes + D&A']];s.getRange(`${c}39`).format.wrapText=true;
 s.getRange(`${c}40`).values=[['無法計算：總債務待核實']];
 checks.push({cell:`${c}38`,value:Number(p.values.ltm_ebitda)});
}
s.getRange('A39:E39').format.rowHeight=42;
d.leverage_notes.forEach((n,i)=>text(42+i,n,54));
text(46,'MD&A reference: '+d.source,30);
text(48,'財務值保留在下方來源區；全部使用本次 BigQuery 讀回紀錄。完整 fact IDs 及計算橋接見同目錄 source_evidence.json。',32);
header(99,['XBRL tag','USD million','Start','End','Source / fact IDs']);
unique.forEach((x,i)=>{const row=100+i;s.getRange(`A${row}:E${row}`).values=[[x.tag,Number(x.value),x.start||'instant',x.end,x.source_urls.join('; ')+' | '+x.fact_ids.join('; ')]];s.getRange(`B${row}`).setNumberFormat(money);s.getRange(`B${row}`).format.font.color='#0000FF';});
s.getRange(`A2:E${100+unique.length}`).format.font.name='Arial';s.getRange(`A3:E${100+unique.length}`).format.font.size=10;
s.getRange('A:A').format.columnWidth=49;s.getRange('B:E').format.columnWidth=27;
s.getRange('B10:E40').format.horizontalAlignment='right';
wb.recalculate();
for(const x of checks){const v=s.getRange(x.cell).values[0][0];if(typeof v!=='number'||Math.abs(v-x.value)>1e-9*Math.max(1,Math.abs(x.value)))throw Error(`Mismatch ${x.cell}`);}
// Verify a source edit recalculates the requested six-month output, then restore.
const input=ref(tags.revenue,'2026-01-01','2026-06-30'),original=s.getRange(input).values[0][0],before=s.getRange('D10').values[0][0];
s.getRange(input).values=[[original+1]];wb.recalculate();if(s.getRange('D10').values[0][0]!==before+1)throw Error('Recalculation failed');s.getRange(input).values=[[original]];wb.recalculate();
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:1500});
const inspect=await wb.inspect({kind:'table',range:'Quarter!A9:E12',include:'values,formulas',tableMaxRows:4,tableMaxCols:5,maxChars:1800});
await fs.writeFile(new URL('excel_validation.json',root),JSON.stringify({checkedNumericOutputs:checks.length,sourceEditRecalculated:true,nativeExcelTested:false,errors:errors.ndjson,inspection:inspect.ndjson},null,2));
for(const [name,range] of [['income','A2:E24'],['ratios_leverage','A26:E48']]){const b=await wb.render({sheetName:'Quarter',range,scale:1.5,format:'png'});await fs.writeFile(new URL(name+'.png',root),new Uint8Array(await b.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(wb)).save(fileURLToPath(new URL('AMZN_credit_review.xlsx',root)));
console.log(`Exported; ${checks.length} numeric outputs verified, source-edit recalculation checked.`);
