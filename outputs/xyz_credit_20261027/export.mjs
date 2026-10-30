import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=new URL('./',import.meta.url),d=JSON.parse(await fs.readFile(new URL('review_data.json',root),'utf8'));
const wb=Workbook.create(),s=wb.worksheets.add('Quarter');s.showGridLines=false;
const refs=new Map(d.inputs.map((x,i)=>[x.id,`B${100+i}`]));
const R=(name,start,end)=>{const id=`${name}|${start??'None'}|${end}`,x=refs.get(id);if(!x)throw Error(id);return x;};
const fmt='#,##0.00;(#,##0.00);0.00',pct='0.00%;(0.00%);0.00%',checks=[];
function text(row,t,height=34){s.getRange(`A${row}:E${row}`).merge();s.getRange(`A${row}`).values=[[t]];s.getRange(`A${row}:E${row}`).format={wrapText:true,rowHeight:height};}
function head(row,values){s.getRange(`A${row}:E${row}`).values=[values];s.getRange(`A${row}:E${row}`).format={fill:'#243746',font:{bold:true,color:'#FFFFFF'},horizontalAlignment:'center',wrapText:true,rowHeight:30};}
function set(cell,expression,inputs,expected,format=fmt){const guard=inputs.map(x=>`ISNUMBER(${x})`).join(',');s.getRange(cell).formulas=[[`=IF(AND(${guard}),${expression},"缺少資料")`]];s.getRange(cell).setNumberFormat(format);if(expected!==undefined)checks.push({cell,expected:Number(expected)});}
const tags={revenue:'Revenues',cost:'CostOfRevenue',gross_profit:'GrossProfit',operating_income:'OperatingIncomeLoss',pretax:'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',tax:'IncomeTaxExpenseBenefit'};
function ex(k,p){const r=k=>R(tags[k],p.start,p.end);if(k==='operating_expense')return {expr:`${r('gross_profit')}-${r('operating_income')}`,inputs:[r('gross_profit'),r('operating_income')]};if(k==='net_income')return {expr:`${r('pretax')}-${r('tax')}`,inputs:[r('pretax'),r('tax')]};return {expr:r(k),inputs:[r(k)]};}
text(2,'Block（Square 母公司；XYZ）信用分析',26);s.getRange('A2').format.font={size:15,bold:true};
text(3,'USD 百萬元｜合併範圍（含非控制權益）｜截止日：2026-10-27｜master',24);
text(4,'FY2024、2025 Q2、FY2025、2026 Q2；兩期損益均採六個月 YTD。',24);
text(5,'待驗收：總額利息、速動資產及 Standard LTM EBITDA 尚未完成。客戶資金受限制，不視為公司可自由償債現金。',36);
text(6,'本次讀回核對 BigQuery 新入庫資料及補查證據；MD&A 模型已回傳 13 主題並對照原文整理。dbt 與舊查詢未完整完成。',36);
text(8,'YTD (Quarterly) Income',24);head(9,['Metric／科目','H1 2025','% revenue','H1 2026','% revenue']);
d.income_rows.forEach(([label,k],i)=>{const row=10+i;s.getRange(`A${row}`).values=[[label]];for(const [index,c,pc] of [[1,'B','C'],[3,'D','E']]){const p=d.periods[index];if(k==='gross_interest'){s.getRange(`${c}${row}`).values=[['待核實總額']];s.getRange(`${pc}${row}`).values=[['無法計算']];continue;}const x=ex(k,p);set(`${c}${row}`,x.expr,x.inputs,p.values[k]);const rev=R('Revenues',p.start,p.end);s.getRange(`${pc}${row}`).formulas=[[`=IF(AND(ISNUMBER(${c}${row}),ISNUMBER(${rev})),IF(${rev}=0,"無法計算",${c}${row}/${rev}),"缺少資料")`]];s.getRange(`${pc}${row}`).setNumberFormat(pct);checks.push({cell:`${pc}${row}`,expected:Number(p.values[k])/Number(p.values.revenue)});}});
text(20,'合併淨利 = 稅前損益 − 帶符號稅費，與歸屬普通股股東淨利分開；淨利息揭露於下方分析，不替代總額費用。',32);
d.income_notes.forEach((n,i)=>text(22+i,n,54));
text(28,'Ratios YTD',24);head(29,['Metric／科目',...d.periods.map(p=>p.end)]);
s.getRange('A30:A32').values=[['Current ratio／流動比率'],['Quick ratio／速動比率'],['Debt ratio／總負債÷合併權益']];
for(let i=0;i<4;i++){const p=d.periods[i],c=String.fromCharCode(66+i);for(const [row,num,den,k] of [[30,R('AssetsCurrent',null,p.end),R('LiabilitiesCurrent',null,p.end),'current_ratio'],[32,R('Liabilities',null,p.end),R('consolidated_equity',null,p.end),'debt_ratio']]){set(`${c}${row}`,`IF(${den}=0,"無法計算",${num}/${den})`,[num,den],p.values[k],pct);}s.getRange(`${c}31`).values=[['待核實 Quick Assets']];}
d.ratio_notes.forEach((n,i)=>text(34+i,n,50));
text(37,'Leverage Analysis YTD',24);head(38,['Metric／科目',...d.periods.map(p=>p.end)]);
s.getRange('A39:A42').values=[['Total debt／票據＋warehouse 本金'],['LTM Standard EBITDA'],['EBITDA basis'],['Total leverage／總槓桿倍數']];
for(let i=0;i<4;i++){const p=d.periods[i],c=String.fromCharCode(66+i),a=R('notes_principal',null,p.end),b=R('warehouse_principal',null,p.end);set(`${c}39`,`${a}+${b}`,[a,b],p.values.total_debt);s.getRange(`${c}40`).values=[['待核實總額利息']];s.getRange(`${c}41`).values=[['NI + Interest + Taxes + D&A']];s.getRange(`${c}42`).values=[['無法計算']];}
s.getRange('B41:E41').format={wrapText:true,rowHeight:36};
d.leverage_notes.forEach((n,i)=>text(44+i,n,52));
text(48,'來源：'+d.source,34);text(49,'下方來源區含原始標籤、日期、BigQuery fact IDs 或附註定位。完整核對與剩餘項目保留於 validation.json。',32);
head(99,['原始標籤／補查科目','USD million','Start','End','來源網址及 fact ID／定位']);
d.inputs.forEach((x,i)=>{const row=100+i;s.getRange(`A${row}:E${row}`).values=[[x.label,Number(x.value),x.start||'instant',x.end,x.source+' | '+x.locator]];s.getRange(`B${row}`).setNumberFormat(fmt);s.getRange(`B${row}`).format.font.color='#0000FF';});
s.getRange(`A2:E${100+d.inputs.length}`).format.font.name='Arial';s.getRange(`A3:E${100+d.inputs.length}`).format.font.size=10;
s.getRange('A:A').format.columnWidth=54;s.getRange('B:E').format.columnWidth=26;s.getRange('B10:E42').format.horizontalAlignment='right';
wb.recalculate();
for(const x of checks){const v=s.getRange(x.cell).values[0][0];if(typeof v!=='number'||Math.abs(v-x.expected)>1e-9*Math.max(1,Math.abs(x.expected)))throw Error(`Mismatch ${x.cell}`);}
const target=R('Revenues','2026-01-01','2026-06-30'),original=s.getRange(target).values[0][0];
s.getRange(target).values=[[original+1]];wb.recalculate();if(s.getRange('D10').values[0][0]!==original+1)throw Error('Source edit did not recalculate');
s.getRange(target).values=[[null]];wb.recalculate();if(s.getRange('D10').values[0][0]!=='缺少資料')throw Error('Missing source became zero');
s.getRange(target).values=[[0]];wb.recalculate();if(s.getRange('D10').values[0][0]!==0||s.getRange('E10').values[0][0]!=='無法計算')throw Error('Zero handling failed');
s.getRange(target).values=[[original]];wb.recalculate();
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:1200});
const inspect=await wb.inspect({kind:'table',range:'Quarter!A9:E12',include:'values,formulas',tableMaxRows:4,tableMaxCols:5,maxChars:1600});
await fs.writeFile(new URL('excel_validation.json',root),JSON.stringify({numericOutputsChecked:checks.length,sourceEditRecalculated:true,blankNotZero:true,zeroDenominatorHandled:true,nativeExcelTested:false,formulaErrors:errors.ndjson,inspection:inspect.ndjson},null,2));
for(const [name,range] of [['income','A2:E26'],['ratios_leverage','A28:E49']]){const b=await wb.render({sheetName:'Quarter',range,scale:1.5,format:'png'});await fs.writeFile(new URL(name+'.png',root),new Uint8Array(await b.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(wb)).save(fileURLToPath(new URL('XYZ_Square_credit_review.xlsx',root)));
console.log('Exported workbook;',checks.length,'numeric outputs verified; blank, zero and recalculation checks passed.');
