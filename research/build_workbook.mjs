import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root = path.resolve(import.meta.dirname, '..');
const out = path.join(root, 'outputs', 'deviceiq-inventory-2026-11-24');
const inventory = JSON.parse(await fs.readFile(path.join(out, 'deviceiq_inventory.json'), 'utf8'));
const t = inventory.tables;
const names = [
  'START HERE', 'RESEARCH SCOPE', 'MASTER DEVICE INVENTORY', 'SMARTPHONES', 'TABLETS', 'LAPTOPS',
  'DEVICE CONFIGURATIONS', 'BRAND MASTERLIST', 'MANUFACTURER MASTERLIST',
  'PHILIPPINE RELEASE RECORDS', 'SOURCE REFERENCES', 'VERIFICATION QUEUE', 'EXCLUDED RECORDS',
  'RAW RESEARCH DATA', 'ANNUAL SUMMARY', 'BRAND YEAR SUMMARY', 'DATA QUALITY REPORT'
];
const wb = Workbook.create();
const sh = Object.fromEntries(names.map(name => [name, wb.worksheets.add(name)]));
const navy = '#123354', blue = '#235A91', pale = '#E9F0F7', ink = '#172B42', muted = '#566A7F';
const excelDate = value => value ? Math.round((Date.parse(value.slice(0, 10) + 'T00:00:00Z') - Date.UTC(1899, 11, 30)) / 86400000) : '';
const v = value => value === null || value === undefined ? '' : value;
const map = (rows, id) => new Map(rows.map(row => [row[id], row]));
const brands = map(t.brands, 'brand_id'), manufacturers = map(t.manufacturers, 'manufacturer_id');
const models = map(t.device_models, 'device_id'), sources = map(t.data_sources, 'source_id');
const releases = map(t.philippines_market_releases, 'device_id');
const configurations = new Map();
for (const row of t.device_configurations) {
  if (!configurations.has(row.device_id)) configurations.set(row.device_id, []);
  configurations.get(row.device_id).push(row);
}
const col = n => { let s=''; for (n++; n; n=Math.floor((n-1)/26)) s=String.fromCharCode(65+(n-1)%26)+s; return s; };
function sheetTable(name, headers, rows, tableName, options={}) {
  const sheet = sh[name];
  sheet.showGridLines = false;
  sheet.tabColor = options.tabColor || blue;
  const matrix = [headers, ...rows.map(row => row.map(v))];
  const end = col(headers.length-1);
  sheet.getRange(`A1:${end}${matrix.length}`).values = matrix;
  sheet.getRange(`A1:${end}1`).format = { fill: navy, font: { name: 'Aptos', size: 10, bold: true, color: '#FFFFFF' }, rowHeight: 34, wrapText: true, verticalAlignment: 'center' };
  if (rows.length) {
    const body = sheet.getRange(`A2:${end}${matrix.length}`);
    body.format.font = { name: 'Aptos', size: 10, color: ink };
    body.format.rowHeight = options.rowHeight || 24;
    body.format.verticalAlignment = 'center';
  }
  const table = sheet.tables.add(`A1:${end}${Math.max(2,matrix.length)}`, true, tableName);
  table.style = 'TableStyleMedium2';
  table.showFilterButton = true;
  sheet.freezePanes.freezeRows(1);
  for (let i=0;i<headers.length;i++) sheet.getRange(`${col(i)}:${col(i)}`).format.columnWidth = Math.min(55, Math.max(15, headers[i].length+4));
  for (const [column,width] of Object.entries(options.widths || {})) sheet.getRange(`${column}:${column}`).format.columnWidth = width;
  for (const column of options.dateColumns || []) if (rows.length) sheet.getRange(`${column}2:${column}${matrix.length}`).setNumberFormat('yyyy-mm-dd');
  return sheet;
}
function textSheet(name, title, rows) {
  const s=sh[name]; s.showGridLines=false; s.tabColor=blue;
  s.getRange('A1:F1').values=[[title,'','','','','']];
  s.getRange('A1:F1').format={fill:navy,font:{name:'Aptos Display',size:18,bold:true,color:'#FFFFFF'},rowHeight:42};
  s.getRange(`A3:B${rows.length+2}`).values=rows;
  s.getRange(`A3:A${rows.length+2}`).format.font={name:'Aptos',size:10,bold:true,color:blue};
  s.getRange(`B3:B${rows.length+2}`).format.font={name:'Aptos',size:10,color:ink};
  s.getRange(`A3:B${rows.length+2}`).format.rowHeight=34;
  s.getRange(`A3:B${rows.length+2}`).format.wrapText=true;
  s.getRange('A:A').format.columnWidth=30; s.getRange('B:B').format.columnWidth=105;
  s.freezePanes.freezeRows(1); return s;
}

textSheet('START HERE','DEVICEIQ  |  PHILIPPINE DEVICE INVENTORY',[
 ['Purpose','Research working file for model-level Philippine smartphone, tablet, and laptop evidence. This snapshot is provisional; it is not an exhaustive census.'],
 ['Snapshot cutoff','2026-11-24. Source material includes preliminary brand/year examples and the existing DeviceIQ catalog.'],
 ['Historical record','Retain 2021-01-01 through 2026-11-24 for audit and boundary analysis.'],
 ['Selected five-year window','2021-11-24 through 2026-11-24 by default. Change the two blue date cells on RESEARCH SCOPE to inspect another window.'],
 ['Geography','Philippines. Official local launch or manufacturer/authorized Philippine availability evidence is required for verified status.'],
 ['Categories','Smartphone, tablet, laptop. One master row represents one base model; hardware versions belong on DEVICE CONFIGURATIONS.'],
 ['Status: pending','Preliminary examples are research leads. A brand/year example is not proof that a specific model was released locally.'],
 ['Status: verified launch','A dated official Philippine launch was found. A launch date is not necessarily a first retail sale date.'],
 ['Status: authorized availability','Official Philippine product/store or local newsroom evidence establishes local presence. Original launch date may remain unknown.'],
 ['Color key','Navy = table header; blue = editable scope input; amber = pending evidence; green = verified; gray = outside selected window.'],
 ['How to add a model','Record a unique brand and exact base model, link the manufacturer, add a Philippine release record and source evidence, then enter SKU-specific specifications in configurations.'],
 ['Source hierarchy','Official manufacturer Philippine pages and local announcements first; authorized local retailers next; local technology reporting for discovery and corroboration.'],
 ['Manufacturer / brand / model / configuration','Manufacturer is the corporate maker, brand is the consumer label, model is the base marketed device, configuration is a distinct hardware or storage variant.'],
 ['Research limitations','Many original local dates and laptop/year lists are missing. See VERIFICATION QUEUE and DATA QUALITY REPORT. The live website catalog is separate.'],
]);
const scope=textSheet('RESEARCH SCOPE','RESEARCH SCOPE  |  CONFIGURABLE WINDOW',[
 ['Geographic market','Philippines'],
 ['Historical start','2021-01-01'],
 ['Research cutoff','2026-11-24'],
 ['Selected start','2021-11-24'],
 ['Selected end','2026-11-24'],
 ['Inclusion','A distinct base model with official Philippine launch or authorized local availability within the selected window.'],
 ['Exclusion','Foreign-only releases, accessories, duplicates, unsupported year claims, and models demonstrably outside the selected window.'],
 ['Date precedence','Exact local first sale > dated local launch > dated official local availability. Keep their meanings distinct.'],
 ['Year-only evidence','If only local year is known, selected-window eligibility is conservative at boundary years.'],
 ['Source review','Save source URL, publisher, publication date, evidence excerpt, and the specific claim supported.'],
 ['Specifications','Record only source-backed model or configuration fields. Empty cells mean unknown, not zero.'],
 ['Prior approved website panel','Earlier site scope: 2021-01-01 through planned 2026-11-30. This research snapshot does not change the live site.'],
 ['Completeness','The supplied notes are example lists, not a complete model census. Laptop discovery remains open.'],
]);
scope.getRange('B4:B7').values=[[excelDate('2021-01-01')],[excelDate('2026-11-24')],[excelDate('2021-11-24')],[excelDate('2026-11-24')]];
scope.getRange('B4:B7').setNumberFormat('yyyy-mm-dd');
scope.getRange('B6:B7').format={fill:'#DBEAFE',font:{name:'Aptos',bold:true,color:'#154C85'},borders:{preset:'outside',style:'thin',color:'#6FA4D7'}};
scope.getRange('B6:B7').dataValidation={rule:{type:'date',operator:'between',formula1:excelDate('2021-01-01'),formula2:excelDate('2026-11-24')}};

const masterHeaders=['Device ID','Category','Manufacturer','Brand','Product Line','Exact Model','Model Number','Global Release Date','Philippine Release Date','Philippine Release Year','RAM Range (GB)','Storage Range (GB)','Processor','Verification Status','Inclusion Snapshot','Primary Source URL','Notes','Selected Scope Status','Quality Flag','Local Evidence Observed Date','Claimed Release Year'];
const masterRows=t.device_models.map(m=>{
  const b=brands.get(m.brand_id), r=releases.get(m.device_id)||{}, configs=configurations.get(m.device_id)||[];
  const range=key=>[...new Set(configs.map(c=>c[key]).filter(x=>x!==null&&x!==undefined))].sort((a,b)=>a-b).join(', ');
  return [m.device_id,m.category_id,manufacturers.get(m.manufacturer_id)?.manufacturer_name||'',b?.brand_name||'',m.product_line||'',m.model_name,m.model_number||'',excelDate(m.global_release_date),excelDate(r.philippine_release_date),r.philippine_release_year||'',range('ram_gb'),range('internal_storage_gb'),configs.map(c=>c.processor).find(Boolean)||'',r.verification_status||m.device_status,r.inclusion_status||'Pending',sources.get(r.primary_source_id)?.source_url||'',r.reviewer_notes||m.description||'','','',excelDate(r.availability_observed_at),r.claimed_release_year||''];
});
const master=sheetTable('MASTER DEVICE INVENTORY',masterHeaders,masterRows,'MasterInventory',{dateColumns:['H','I','T'],widths:{A:28,C:28,D:18,F:32,P:54,Q:48}});
const lastMaster=masterRows.length+1;
// The selected-scope formula never upgrades a preliminary claim to a verified device.
for(let i=2;i<=lastMaster;i++){
  master.getRange(`R${i}`).formulas=[[`=IF(N${i}="PENDING_VERIFICATION","Pending",IF(I${i}<>"",IF(AND(I${i}>='RESEARCH SCOPE'!$B$6,I${i}<='RESEARCH SCOPE'!$B$7),"Included","Excluded"),IF(J${i}="","Pending date",IF(OR(J${i}<YEAR('RESEARCH SCOPE'!$B$6),J${i}>YEAR('RESEARCH SCOPE'!$B$7)),"Excluded",IF(AND(J${i}>YEAR('RESEARCH SCOPE'!$B$6),J${i}<YEAR('RESEARCH SCOPE'!$B$7)),"Included",IF(AND(J${i}=YEAR('RESEARCH SCOPE'!$B$6),MONTH('RESEARCH SCOPE'!$B$6)=1,DAY('RESEARCH SCOPE'!$B$6)=1),"Included",IF(AND(T${i}<>"",T${i}<'RESEARCH SCOPE'!$B$6),"Excluded",IF(AND(J${i}=YEAR('RESEARCH SCOPE'!$B$7),T${i}<>"",T${i}<='RESEARCH SCOPE'!$B$7),"Included","Pending date"))))))))`]];
  master.getRange(`S${i}`).formulas=[[`=IF(COUNTIFS($B$2:$B$${lastMaster},B${i},$D$2:$D$${lastMaster},D${i},$F$2:$F$${lastMaster},F${i})>1,"Duplicate base model",IF(D${i}="","Missing brand",IF(C${i}="","Missing manufacturer",IF(P${i}="","Missing model source",IF(N${i}="PENDING_VERIFICATION","Unverified model",IF(I${i}="","Missing exact local date",IF(AND(K${i}="",L${i}="",M${i}=""),"Missing specifications",IF(R${i}="Excluded","Outside window","Ready for review"))))))))`]];
}
master.getRange(`B2:B${lastMaster}`).dataValidation={rule:{type:'list',values:['smartphones','tablets','laptops']}};
master.getRange(`N2:N${lastMaster}`).dataValidation={rule:{type:'list',values:['PENDING_VERIFICATION','VERIFIED_OFFICIAL_LAUNCH','VERIFIED_AUTHORIZED_AVAILABILITY']}};
master.getRange(`N2:N${lastMaster}`).conditionalFormats.add('containsText',{text:'VERIFIED',format:{fill:'#DDF3E8',font:{color:'#126B44'}}});
master.getRange(`N2:N${lastMaster}`).conditionalFormats.add('containsText',{text:'PENDING',format:{fill:'#FFF1CF',font:{color:'#8A5A00'}}});

const detailHeaders=['Device ID','Brand','Exact Model','Philippine Year','Verification','Selected Scope','Local Date','Processor','RAM GB','Storage GB','Display in','Resolution','Battery mAh','Battery Wh','Rear Camera MP','Front Camera MP','Operating System','Price PHP','Primary Source URL','Research Notes'];
for(const [name,cat] of [['SMARTPHONES','smartphones'],['TABLETS','tablets'],['LAPTOPS','laptops']]){
  const rows=t.device_models.filter(m=>m.category_id===cat).map(m=>{
    const b=brands.get(m.brand_id),r=releases.get(m.device_id)||{},c=(configurations.get(m.device_id)||[])[0]||{};
    return [m.device_id,b?.brand_name||'',m.model_name,r.philippine_release_year||'',r.verification_status||'PENDING_VERIFICATION',r.inclusion_status||'Pending',excelDate(r.philippine_release_date),c.processor||'',v(c.ram_gb),v(c.internal_storage_gb),v(c.display_inches),c.display_resolution||'',v(c.battery_mah),v(c.battery_wh),v(c.rear_camera_mp),v(c.front_camera_mp),c.operating_system||'',v(c.price_php),sources.get(r.primary_source_id)?.source_url||'',r.reviewer_notes||''];
  });
  sheetTable(name,detailHeaders,rows,name+'Models',{dateColumns:['G'],widths:{C:30,S:55,T:48}});
}
sheetTable('DEVICE CONFIGURATIONS',['Configuration ID','Device ID','Brand','Exact Model','Configuration','SKU','Model Code','Processor','Chipset','CPU','GPU','RAM GB','Storage GB','Display in','Resolution','Display Type','Refresh Hz','Battery mAh','Battery Wh','Charging W','Rear Camera MP','Front Camera MP','Operating System','Connectivity','Weight g','Price PHP','Price Condition','Price Observed','Source URL','Notes'],t.device_configurations.map(c=>{
  const m=models.get(c.device_id);return [c.configuration_id,c.device_id,brands.get(m.brand_id)?.brand_name||'',m.model_name,c.configuration_name,c.sku,c.model_code,c.processor,c.chipset,c.cpu,c.gpu,c.ram_gb,c.internal_storage_gb,c.display_inches,c.display_resolution,c.display_type,c.refresh_hz,c.battery_mah,c.battery_wh,c.charging_w,c.rear_camera_mp,c.front_camera_mp,c.operating_system,c.connectivity,c.weight_g,c.price_php,c.price_condition,excelDate(c.price_observed_at),sources.get(c.price_source_id)?.source_url||'',c.notes];
}),'DeviceConfigurations',{dateColumns:['AB'],widths:{D:30,AC:50,AD:48}});

const brandHeaders=['Brand ID','Brand','Canonical Brand','Manufacturer','Parent Company','Alternative Names','Official Website','Brand Status',...Array.from({length:6},(_,i)=>String(2021+i))];
const brandRows=t.brands.map(b=>[b.brand_id,b.brand_name,b.canonical_brand_name,manufacturers.get(b.manufacturer_id)?.manufacturer_name||'',manufacturers.get(manufacturers.get(b.manufacturer_id)?.parent_company_id)?.manufacturer_name||'',b.alternative_names,b.official_website,b.brand_status,...Array(6).fill('')]);
const brandSheet=sheetTable('BRAND MASTERLIST',brandHeaders,brandRows,'BrandMasterlist',{widths:{B:20,D:27,G:45}});
for(let i=2;i<=brandRows.length+1;i++)for(let j=0;j<6;j++)brandSheet.getRange(`${col(8+j)}${i}`).formulas=[[`=IF(COUNTIFS('MASTER DEVICE INVENTORY'!$D$2:$D$${lastMaster},B${i},'MASTER DEVICE INVENTORY'!$J$2:$J$${lastMaster},${2021+j},'MASTER DEVICE INVENTORY'!$R$2:$R$${lastMaster},"Included")>0,1,0)`]];

const manufacturerHeaders=['Manufacturer ID','Manufacturer','Corporate Parent','Country','Official Website','Associated Brands',...Array.from({length:6},(_,i)=>String(2021+i))];
const manufacturerRows=t.manufacturers.map(m=>[m.manufacturer_id,m.manufacturer_name,manufacturers.get(m.parent_company_id)?.manufacturer_name||'',m.country_of_origin,m.official_website,t.brands.filter(b=>b.manufacturer_id===m.manufacturer_id).map(b=>b.brand_name).join(', '),...Array(6).fill('')]);
const manufacturerSheet=sheetTable('MANUFACTURER MASTERLIST',manufacturerHeaders,manufacturerRows,'ManufacturerMasterlist',{widths:{B:30,F:55}});
for(let i=2;i<=manufacturerRows.length+1;i++)for(let j=0;j<6;j++)manufacturerSheet.getRange(`${col(6+j)}${i}`).formulas=[[`=IF(COUNTIFS('MASTER DEVICE INVENTORY'!$C$2:$C$${lastMaster},B${i},'MASTER DEVICE INVENTORY'!$J$2:$J$${lastMaster},${2021+j},'MASTER DEVICE INVENTORY'!$R$2:$R$${lastMaster},"Included")>0,1,0)`]];

sheetTable('PHILIPPINE RELEASE RECORDS',['Device ID','Brand','Exact Model','Category','Local Launch Date','Precision','Local Release Year','Availability Date','Observed Date','Availability Status','Launch Status','Authorized Distributor','Evidence','Inclusion Snapshot','Verification','Primary Source URL','Notes'],t.philippines_market_releases.map(r=>{
  const m=models.get(r.device_id);return [r.device_id,brands.get(m.brand_id)?.brand_name||'',m.model_name,m.category_id,excelDate(r.philippine_release_date),r.release_date_precision,r.philippine_release_year,excelDate(r.availability_date),excelDate(r.availability_observed_at),r.availability_status,r.official_launch_status,r.authorized_distributor,r.market_availability_evidence,r.inclusion_status,r.verification_status,sources.get(r.primary_source_id)?.source_url||'',r.reviewer_notes];
}),'PhilippineReleases',{dateColumns:['E','H','I'],widths:{C:30,M:65,P:60,Q:50}});

const evidenceRows=t.device_source_evidence.map(e=>{
 const s=sources.get(e.source_id), m=models.get(e.device_id);return [e.source_id,e.device_id,brands.get(m.brand_id)?.brand_name||'',m.model_name,s.source_title,s.publisher,s.source_url,s.source_type,excelDate(s.publication_date),excelDate(s.access_date),e.supported_claim,e.verification_result,s.source_reliability,e.reviewer_notes||e.evidence_excerpt||''];
});
const sourceSheet=sheetTable('SOURCE REFERENCES',['Source ID','Device ID','Brand','Model','Source Title','Publisher','Source URL','Source Type','Published','Accessed','Supported Claim','Verification Result','Reliability','Reviewer Notes'],evidenceRows,'SourceReferences',{dateColumns:['I','J'],widths:{D:30,E:42,G:65,K:50,N:55}});
for(let i=2;i<=evidenceRows.length+1;i++)if(evidenceRows[i-2][6]){
  const url=evidenceRows[i-2][6].replaceAll('"','""');
  sourceSheet.getRange(`G${i}`).formulas=[[`=HYPERLINK("${url}","${url}")`]];
}

sheetTable('VERIFICATION QUEUE',['Queue ID','Device ID','Device Name','Brand','Category','Claimed Year','Missing Evidence','Verification Issue','Required Action','Priority','Current Status','Reviewer Notes'],t.research_queue.map(q=>[q.queue_id,q.device_id,q.candidate_name,q.brand_name,q.category_id,q.claimed_release_year,q.missing_evidence,q.verification_issue,q.required_action,q.priority,q.current_status,q.reviewer_notes]),'VerificationQueue',{widths:{C:36,G:47,H:47,I:58,L:45}});
sheetTable('EXCLUDED RECORDS',['Exclusion ID','Original Claim ID','Original Record','Device Name','Brand','Category','Reason','Supporting Evidence','Reviewed'],t.excluded_records.map(e=>[e.exclusion_id,e.raw_claim_id,e.original_record,e.device_name,e.brand_name,e.category_id,e.exclusion_reason,e.supporting_evidence,excelDate(e.date_reviewed)]),'ExcludedRecords',{dateColumns:['I'],widths:{C:55,D:30,G:48,H:55}});
sheetTable('RAW RESEARCH DATA',['Claim ID','Source File','Line','Original Text','Research Year','Original Brand','Original Model Text','Original Category','Original Release Claim','Original Source Reference','Processing Status','Verification Status','Duplicate Of','Reviewer Notes'],t.raw_research_claims.map(c=>[c.claim_id,c.source_file,c.source_line,c.raw_text,c.research_year,c.original_brand_name,c.original_model_text,c.original_category,c.original_release_claim,c.original_source_reference,c.processing_status,c.verification_status,c.duplicate_of,c.reviewer_notes]),'RawResearchClaims',{widths:{B:42,D:90,G:50,I:42,J:62,N:45},rowHeight:32});

const annual=sheetTable('ANNUAL SUMMARY',['Year','Smartphones Included','Tablets Included','Laptops Included','Total Included','Verified with Local Year','Pending Claims','Excluded','Manufacturers with Included Models','Brands with Included Models'],Array.from({length:6},(_,i)=>[2021+i,...Array(9).fill('')]),'AnnualSummary',{widths:{B:24,C:22,D:22,F:29,I:34,J:29}});
for(let i=2;i<=7;i++){
  for(let j=0;j<3;j++)annual.getRange(`${col(1+j)}${i}`).formulas=[[`=COUNTIFS('MASTER DEVICE INVENTORY'!$J$2:$J$${lastMaster},$A${i},'MASTER DEVICE INVENTORY'!$B$2:$B$${lastMaster},"${['smartphones','tablets','laptops'][j]}",'MASTER DEVICE INVENTORY'!$R$2:$R$${lastMaster},"Included")`]];
  annual.getRange(`E${i}`).formulas=[[`=SUM(B${i}:D${i})`]];
  annual.getRange(`F${i}`).formulas=[[`=COUNTIFS('MASTER DEVICE INVENTORY'!$J$2:$J$${lastMaster},$A${i},'MASTER DEVICE INVENTORY'!$N$2:$N$${lastMaster},"<>PENDING_VERIFICATION",'MASTER DEVICE INVENTORY'!$N$2:$N$${lastMaster},"<>")`]];
  annual.getRange(`G${i}`).formulas=[[`=COUNTIFS('MASTER DEVICE INVENTORY'!$U$2:$U$${lastMaster},$A${i},'MASTER DEVICE INVENTORY'!$N$2:$N$${lastMaster},"PENDING_VERIFICATION")`]];
  annual.getRange(`H${i}`).formulas=[[`=COUNTIFS('MASTER DEVICE INVENTORY'!$J$2:$J$${lastMaster},$A${i},'MASTER DEVICE INVENTORY'!$R$2:$R$${lastMaster},"Excluded")`]];
  annual.getRange(`I${i}`).formulas=[[`=SUM('MANUFACTURER MASTERLIST'!${col(6+i-2)}$2:${col(6+i-2)}$${manufacturerRows.length+1})`]];
  annual.getRange(`J${i}`).formulas=[[`=SUM('BRAND MASTERLIST'!${col(8+i-2)}$2:${col(8+i-2)}$${brandRows.length+1})`]];
}
sheetTable('BRAND YEAR SUMMARY',['Brand',...Array.from({length:6},(_,i)=>String(2021+i))],t.brands.map(b=>[b.brand_name,...Array(6).fill('')]),'BrandYearSummary',{widths:{A:25}});
for(let i=2;i<=brandRows.length+1;i++)for(let j=0;j<6;j++)sh['BRAND YEAR SUMMARY'].getRange(`${col(j+1)}${i}`).formulas=[[`=IF('BRAND MASTERLIST'!${col(j+8)}${i}>0,"Yes","")`]];

const qualityMetrics=[
 ['All candidate and verified base models',`=COUNTA('MASTER DEVICE INVENTORY'!$A$2:$A$${lastMaster})`],
 ['Pending model verification',`=COUNTIF('MASTER DEVICE INVENTORY'!$N$2:$N$${lastMaster},"PENDING_VERIFICATION")`],
 ['Missing exact local date',`=COUNTIFS('MASTER DEVICE INVENTORY'!$N$2:$N$${lastMaster},"VERIFIED*",'MASTER DEVICE INVENTORY'!$I$2:$I$${lastMaster},"")`],
 ['Missing manufacturer',`=COUNTIF('MASTER DEVICE INVENTORY'!$C$2:$C$${lastMaster},"")`],
 ['Missing brand',`=COUNTIF('MASTER DEVICE INVENTORY'!$D$2:$D$${lastMaster},"")`],
 ['Missing model-level source',`=COUNTIF('MASTER DEVICE INVENTORY'!$P$2:$P$${lastMaster},"")`],
 ['Missing processor, RAM and storage',`=COUNTIFS('MASTER DEVICE INVENTORY'!$K$2:$K$${lastMaster},"",'MASTER DEVICE INVENTORY'!$L$2:$L$${lastMaster},"",'MASTER DEVICE INVENTORY'!$M$2:$M$${lastMaster},"")`],
 ['Outside selected period',`=COUNTIF('MASTER DEVICE INVENTORY'!$R$2:$R$${lastMaster},"Excluded")`],
 ['Duplicate exact brand/category/model',`=COUNTIF('MASTER DEVICE INVENTORY'!$S$2:$S$${lastMaster},"Duplicate base model")`],
 ['Unsupported release-year leads',`=COUNTIF('MASTER DEVICE INVENTORY'!$N$2:$N$${lastMaster},"PENDING_VERIFICATION")`],
 ['Conflicting local dates','Review required'],
 ['Incorrect categories','Review required'],
 ['Configurations misclassified as base models','Review required'],
];
const q=sheetTable('DATA QUALITY REPORT',['Check','Current Count','Interpretation'],qualityMetrics.map(([label,,],i)=>[label,'',i>=10?'Manual evidence review is needed; no deterministic check has been completed.':'Calculated from the master inventory.']),'QualityChecks',{widths:{A:48,B:23,C:86}});
qualityMetrics.forEach(([,formula],i)=>{if(typeof formula==='string' && formula.startsWith('='))q.getRange(`B${i+2}`).formulas=[[formula]];else q.getRange(`B${i+2}`).values=[[formula]];});
const statusRow=qualityMetrics.length+4;
q.getRange(`A${statusRow}:C${statusRow}`).values=[['Research status','Provisional','The supplied research examples are incomplete; see VERIFICATION QUEUE for remaining work.']];
q.getRange(`A${statusRow}:C${statusRow}`).format={fill:pale,font:{name:'Aptos',bold:true,color:ink}};

// Recalculate after all cross-sheet ranges and validation rules are in place.
wb.recalculate();
const file=path.join(out,'DeviceIQ_Philippine_Device_Inventory_2021-2026.xlsx');
const xlsx=await SpreadsheetFile.exportXlsx(wb); await xlsx.save(file);
for (const name of ['START HERE','ANNUAL SUMMARY','MASTER DEVICE INVENTORY']) {
  try {
    const preview=await wb.render({sheetName:name,range:name==='MASTER DEVICE INVENTORY'?'A1:J11':undefined,autoCrop:name==='MASTER DEVICE INVENTORY'?undefined:'all',scale:1,format:'png'});
    await fs.writeFile(path.join(out,`preview_${name.toLowerCase().replaceAll(' ','_')}.png`),new Uint8Array(await preview.arrayBuffer()));
  } catch(error) { console.warn(`Preview ${name}: ${error.message}`); }
}
console.log(JSON.stringify({file,sheets:names.length,models:masterRows.length,rawClaims:t.raw_research_claims.length,queue:t.research_queue.length}));
