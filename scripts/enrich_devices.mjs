#!/usr/bin/env node
// Conservative source collection: never changes the public catalog or release status.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { pathToFileURL } from 'node:url';
import { load } from 'cheerio';

const args = process.argv.slice(2);
const getArg = (name, fallback) => {
  const index = args.indexOf(name);
  return index < 0 ? fallback : args[index + 1];
};
const inventoryPath = resolve(getArg('--inventory', 'outputs/deviceiq-inventory-2026-11-24/deviceiq_inventory.json'));
const outputPath = resolve(getArg('--output', 'research/enrichment/latest.json'));
const limit = Number(getArg('--limit', '0'));
const discoveryLimit = Number(getArg('--discover-limit', '60'));
const gsmarenaLimit = Number(getArg('--gsmarena-limit', '20'));
const ptgLimit = Number(getArg('--ptg-limit', '60'));
const timeoutMs = Number(getArg('--timeout-ms', '9000'));
const requestedDeviceId = getArg('--device-id', '');
const maxBytes = 2_000_000;
const userAgent = 'DeviceIQResearchBot/1.0 (+https://github.com/ynee6969/Device-IQ; evidence collection)';
const now = new Date().toISOString();
const sleep = ms => new Promise(done => setTimeout(done, ms));
const clean = value => String(value ?? '').replace(/\s+/g, ' ').trim();
const normalized = value => clean(value).normalize('NFKD').toLowerCase().replace(/\b5g\b/g, '5g').replace(/[^a-z0-9+]+/g, ' ').replace(/\s+/g, ' ').trim();
const boundaryMatch = (haystack, needle) => {
  const h = ` ${normalized(haystack)} `;
  const n = normalized(needle);
  return n && h.includes(` ${n} `);
};
const exactModelMention = (haystack, model) => {
  // Product names commonly write a final plus suffix as either "+" or "Plus".
  // Normalize only model-identity checks so the base model still cannot match.
  const modelName = value => normalized(value).replace(/(?<=\w)\+(?=\s|$)/g, ' plus');
  const h = modelName(haystack);
  const n = modelName(model);
  if (!boundaryMatch(h, n)) return false;
  const index = ` ${h} `.indexOf(` ${n} `);
  const after = ` ${h} `.slice(index + n.length + 2).trimStart();
  return !/^(?:ultra|pro|max|plus|fe|series|lite|mini)\b/.test(after);
};

async function fetchText(url, headers = {}, followRedirects = false) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { signal: controller.signal, redirect: followRedirects ? 'follow' : 'manual', headers: { 'user-agent': userAgent, ...headers } });
    const contentLength = Number(response.headers.get('content-length') || 0);
    if (contentLength > maxBytes) return { status: response.status, error: 'oversize', url: response.url };
    const bytes = new Uint8Array(await response.arrayBuffer());
    if (bytes.length > maxBytes) return { status: response.status, error: 'oversize', url: response.url };
    return { status: response.status, contentType: response.headers.get('content-type') || '', text: new TextDecoder().decode(bytes), url: response.url };
  } catch (error) {
    return { error: error.name === 'AbortError' ? 'timeout' : `network:${error.message}` };
  } finally {
    clearTimeout(timer);
  }
}

// RFC 9309 longest matching rule, with the crawler group preferred to wildcard.
export function robotsAllowed(body, pathname, agent = 'DeviceIQResearchBot') {
  const groups = [];
  let group = { agents: [], rules: [] };
  let hasRules = false;
  for (const raw of body.split(/\r?\n/)) {
    const line = raw.replace(/#.*$/, '').trim();
    if (!line) continue;
    const match = line.match(/^([\w-]+)\s*:\s*(.*)$/);
    if (!match) continue;
    const key = match[1].toLowerCase();
    const value = match[2].trim();
    if (key === 'user-agent') {
      if (hasRules) { groups.push(group); group = { agents: [], rules: [] }; hasRules = false; }
      group.agents.push(value.toLowerCase());
    } else if ((key === 'allow' || key === 'disallow') && group.agents.length) {
      hasRules = true;
      if (value) group.rules.push({ allow: key === 'allow', path: value });
    }
  }
  groups.push(group);
  const agentName = agent.toLowerCase();
  const matches = groups.map(g => ({ ...g, specificity: Math.max(...g.agents.filter(a => a !== '*' && agentName.includes(a)).map(a => a.length), -1) }));
  const best = Math.max(...matches.map(g => g.specificity));
  const applicable = best >= 0 ? matches.filter(g => g.specificity === best) : matches.filter(g => g.agents.includes('*'));
  const rules = applicable.flatMap(g => g.rules).filter(rule => {
    const anchored = rule.path.endsWith('$');
    const pattern = anchored ? rule.path.slice(0, -1) : rule.path;
    const expression = pattern.split('*').map(part => part.replace(/[|\\{}()[\]^$+?.]/g, '\\$&')).join('.*');
    return new RegExp(`^${expression}${anchored ? '$' : ''}`).test(pathname);
  });
  rules.sort((a, b) => b.path.replace(/[\*$]/g, '').length - a.path.replace(/[\*$]/g, '').length || Number(b.allow) - Number(a.allow));
  return rules[0]?.allow ?? true;
}

const robotCache = new Map();
export async function canFetch(url) {
  const parsed = new URL(url);
  if (!['https:', 'http:'].includes(parsed.protocol)) return { allowed: false, reason: 'unsupported_protocol' };
  if (!robotCache.has(parsed.origin)) {
    const robot = await fetchText(`${parsed.origin}/robots.txt`, {}, true);
    robotCache.set(parsed.origin, robot);
  }
  const robot = robotCache.get(parsed.origin);
  if (robot.error || robot.status !== 200 || new URL(robot.url).origin !== parsed.origin) return { allowed: false, reason: `robots_${robot.error || robot.status}` };
  return { allowed: robotsAllowed(robot.text, `${parsed.pathname}${parsed.search}`), reason: 'robots_disallow' };
}

const officialHosts = new Set([
  'apple.com', 'samsung.com', 'news.samsung.com', 'mi.com', 'asus.com', 'acer.com',
  'lenovo.com', 'huawei.com', 'honor.com', 'oppo.com', 'vivo.com', 'realme.com',
  'tecno-mobile.com', 'infinixmobility.com', 'motorola.com', 'nokia.com', 'oneplus.com',
  'nothing.tech', 'poco.com', 'redmi.com', 'google.com', 'store.google.com',
  'dell.com', 'hp.com', 'msi.com', 'gigabyte.com', 'framework.com', 'razer.com',
]);
const ptgHost = 'www.pinoytechnoguide.com';
const ptgUrl = value => {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && url.hostname === ptgHost && /^\/(?:smartphones|tablets)\/[a-z0-9-]+\/?$/.test(url.pathname);
  } catch { return false; }
};
function officialUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && [...officialHosts].some(host => url.hostname === host || url.hostname.endsWith(`.${host}`));
  } catch { return false; }
}

const fieldAliases = [
  [/^(?:display technology|display type|screen type|panel type)\b/i, 'display_technology'],
  [/^(?:display brightness|brightness)\b/i, 'display_brightness'],
  [/^(?:display protection|screen protection|glass protection)\b/i, 'display_protection'],
  [/^(?:display color|colour gamut|color gamut)\b/i, 'display_color'],
  [/^(?:display resolution|resolution)\b/i, 'resolution'],
  [/^(?:display refresh rate|refresh rate|refresh)\b/i, 'refresh_hz'],
  [/^(?:battery type|battery chemistry)\b/i, 'battery_technology'],
  [/^(?:battery life|maximum battery run time)\b/i, 'battery_life'],
  [/^(?:ram type|memory type)\b/i, 'ram_type'],
  [/^(?:storage type|storage technology)\b/i, 'storage_type'],
  [/^(?:battery(?: capacity)?|typical battery)\b/i, 'battery_capacity'],
  [/^(?:ram|memory)\b/i, 'ram_gb'],
  [/^(?:storage|internal storage|rom)\b/i, 'internal_storage_gb'],
  [/^(?:expansion|expandable storage|card slot)\b/i, 'storage_expansion'],
  [/^(?:display size|screen size|display)\b/i, 'display_inches'],
  [/^(?:processor|chipset|soc)\b/i, 'processor'],
  [/^(?:cpu)\b/i, 'cpu'],
  [/^(?:gpu|graphics|graphics card)\b/i, 'gpu'],
  [/^(?:operating system|os)\b/i, 'operating_system'],
  [/^(?:display )?resolution\b/i, 'resolution'],
  [/^(?:weight)\b/i, 'weight'],
  [/^(?:dimensions|dimension)\b/i, 'dimensions'],
  [/^(?:charging|wired charging)\b/i, 'charging'],
  [/^(?:wi-?fi)\b/i, 'wifi'],
  [/^(?:bluetooth)\b/i, 'bluetooth'],
  [/^(?:nfc)\b/i, 'nfc'],
  [/^(?:sim|sim card)\b/i, 'sim'],
  [/^(?:main camera sensor)\b/i, 'main_camera_sensor'],
  [/^(?:ultrawide camera|ultra-wide camera)\b/i, 'ultrawide_camera'],
  [/^(?:telephoto camera|periscope camera)\b/i, 'telephoto_camera'],
  [/^(?:front camera|selfie camera)\b/i, 'front_camera'],
  [/^(?:webcam|camera resolution)\b/i, 'webcam'],
  [/^(?:rear camera|main camera|camera)\b/i, 'rear_camera'],
  [/^(?:video recording|video)\b/i, 'video_recording'],
  [/^(?:build materials|materials|build)\b/i, 'materials'],
  [/^(?:water resistance|waterproof|ip rating)\b/i, 'ip_rating'],
  [/^(?:durability)\b/i, 'ip_rating'],
  [/^(?:cellular|network|mobile network)\b/i, 'cellular'],
  [/^(?:location|positioning|gnss)\b/i, 'gnss'],
  [/^(?:sound|audio|speaker)\b/i, 'audio'],
  [/^(?:sensors|sensor)\b/i, 'sensors'],
  [/^(?:stylus|pen support)\b/i, 'tablet_stylus'],
  [/^(?:keyboard compatibility|keyboard support)\b/i, 'tablet_keyboard'],
  [/^(?:keyboard)\b/i, 'keyboard'],
  [/^(?:touchpad|trackpad)\b/i, 'touchpad'],
  [/^(?:ethernet|wired lan)\b/i, 'ethernet'],
  [/^(?:warranty)\b/i, 'warranty'],
  [/^(?:touchscreen)\b/i, 'touchscreen'],
  [/^(?:usb port|usb|usb connector)\b/i, 'usb'],
  [/^(?:ports|interface)\b/i, 'ports'],
];
function parseField(label, value, category = 'smartphones') {
  let key = fieldAliases.find(([pattern]) => pattern.test(label))?.[1];
  if (!key || !value || value.length > 200) return null;
  if ((key === 'ram_gb' || key === 'internal_storage_gb') && (/storage.*ram|ram.*storage/i.test(label) || (value.match(/\b\d{1,4}\s*GB\b/gi) || []).length !== 1)) return null;
  let result = clean(value);
  let unit = null;
  if (key === 'processor') key = category === 'laptops' ? 'cpu' : 'chipset';
  if (key === 'battery_capacity') {
    const found = result.match(/\b([\d,]+(?:\.\d+)?)\s*(mAh|Wh)\b/i);
    if (!found) return null;
    result = found[1].replace(/,/g, '');
    unit = found[2].toLowerCase() === 'mah' ? 'mAh' : 'Wh';
    key = unit === 'Wh' ? 'battery_wh' : 'battery_mah';
  }
  if (key === 'ram_gb' || key === 'internal_storage_gb') {
    const found = result.match(/\b(\d{1,4})\s*GB\b/i);
    if (!found) return null;
    result = found[1]; unit = 'GB';
  }
  if (key === 'display_inches') {
    const found = result.match(/\b(\d{1,2}(?:\.\d{1,2})?)[\s-]*(?:inches|inch|["”])/i);
    if (!found) return null;
    result = found[1]; unit = 'in';
  }
  if (key === 'refresh_hz') {
    const found = result.match(/\b(\d{2,3}(?:\.\d+)?)\s*Hz\b/i);
    if (!found) return null;
    result = found[1]; unit = 'Hz';
  }
  if (key === 'weight') {
    const found = result.match(/\b(\d+(?:\.\d+)?)\s*(kg|g)\b/i);
    if (found) { result = found[1]; unit = found[2].toLowerCase(); }
  }
  if (key === 'dimensions' && !/\b\d+(?:\.\d+)?\s*(?:mm|cm)?\s*[x×]\s*\d+(?:\.\d+)?\s*(?:mm|cm)?\s*[x×]\s*\d+(?:\.\d+)?\s*(?:mm|cm)?\b/i.test(result)) return null;
  if (key === 'front_camera') {
    const found = result.match(/\b(\d+(?:\.\d+)?)\s*(?:MP|megapixels?)\b/i);
    if (!found) return null;
    result = found[1]; unit = 'MP';
  }
  if (!result) return null;
  return { key, value: result, unit, excerpt: `${clean(label)}: ${clean(value)}`.slice(0, 240) };
}

function extractCompositeSpecs(label, value) {
  const result = [];
  const text = clean(value);
  const add = (key, found, unit = null) => { if (found) result.push({ key, value: clean(found), unit, excerpt: `${clean(label)}: ${text}`.slice(0, 240) }); };
  if (/^(?:display|display specifications|screen)$/i.test(clean(label))) {
    const technology = text.match(/\b(Dynamic AMOLED(?:\s+\d+X?)?|Super AMOLED(?:\s+Plus)?|LTPO AMOLED|AMOLED|P-OLED|OLED|IPS(?: LCD)?|TFT(?: LCD)?|LCD|Liquid Retina(?: XDR)?|Mini-LED)\b/i)?.[1];
    add('display_technology', technology);
    const resolution = text.match(/\b(\d{3,4})\s*[x×]\s*(\d{3,4})\b/i);
    add('resolution', resolution ? `${resolution[1]} x ${resolution[2]}` : null);
    const refresh = text.match(/\b(\d{2,3}(?:\.\d+)?)\s*Hz\b/i)?.[1];
    add('refresh_hz', refresh, 'Hz');
    const brightness = text.match(/\b([\d,]+(?:\.\d+)?\s*(?:nits?|cd\/m(?:2|²)))\b/i)?.[1];
    add('display_brightness', brightness);
    const protection = text.match(/\b(Corning Gorilla Glass(?:\s+[\w.-]+)?|Panda Glass(?:\s+[\w.-]+)?|Dragontrail Glass(?:\s+[\w.-]+)?)\b/i)?.[1];
    add('display_protection', protection);
    const color = text.match(/\b(\d+%\s*(?:DCI-P3|sRGB|NTSC|Adobe RGB)|DCI-P3|sRGB)\b/i)?.[1];
    add('display_color', color);
  }
  if (/^(?:rear camera|main camera|camera)$/i.test(clean(label))) {
    const segments = [...text.matchAll(/(\d+(?:\.\d+)?\s*MP\b.*?)(?=\s+\d+(?:\.\d+)?\s*MP\b|$)/gi)].map(match => clean(match[1]));
    const main = segments.find(x => /\bmain\b/i.test(x));
    const ultra = segments.find(x => /ultra[- ]?wide/i.test(x));
    const tele = segments.find(x => /telephoto|periscope/i.test(x));
    add('main_camera_sensor', main);
    add('ultrawide_camera', ultra);
    add('telephoto_camera', tele);
    const video = text.match(/\b(?:up to\s*)?\d{3,4}p(?:\s*@\s*\d+\s*fps)?[^.;,]*|\b(?:up to\s*)?\d+[Kk](?:\s*@\s*\d+\s*fps)?[^.;,]*/i)?.[0];
    add('video_recording', video);
  }
  if (/^(?:battery|typical battery)$/i.test(clean(label))) {
    const chemistry = text.match(/\b(Li[- ]?(?:Po|Ion)|Lithium[- ](?:ion|polymer))\b[^,;]*/i)?.[0];
    add('battery_technology', chemistry);
  }
  return result;
}

function jsonLdObjects(value) {
  if (Array.isArray(value)) return value.flatMap(jsonLdObjects);
  if (!value || typeof value !== 'object') return [];
  return [value, ...jsonLdObjects(value['@graph'] || [])];
}
export function extractPage(html, device, configurations = [], sourceKind = 'official') {
  const $ = load(html);
  $('script:not([type="application/ld+json"]),style,nav,footer').remove();
  const title = clean($('title').first().text() || $('h1').first().text());
  const headings = clean($('h1').map((_, el) => $(el).text()).get().join(' '));
  const model = device.model_name;
  if (!exactModelMention(headings || title, model)) return { status: 'model_mismatch', title, specs: [], prices: [] };
  const entities = [];
  $('script[type="application/ld+json"]').each((_, el) => {
    try { entities.push(...jsonLdObjects(JSON.parse($(el).html() || 'null'))); } catch { /* malformed source markup */ }
  });
  const products = entities.filter(x => String(x['@type'] || '').toLowerCase().includes('product') && exactModelMention(x.name || '', model));
  const bylineDate = clean($('.post-details').first().text()).match(/\bon\s+([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})/)?.[1];
  const parsedDate = bylineDate ? Date.parse(`${bylineDate} UTC`) : NaN;
  const publishedAt = entities.find(x => String(x['@type'] || '').toLowerCase().includes('article') && x.datePublished)?.datePublished || $('meta[property="article:published_time"]').attr('content') || (Number.isFinite(parsedDate) ? new Date(parsedDate).toISOString().slice(0, 10) : null);
  const specs = [];
  $('tr').each((_, row) => {
    const cells = $(row).find('th,td').map((__, el) => clean($(el).text())).get();
    if (cells.length === 2) {
      const field = parseField(cells[0], cells[1], device.category_id);
      if (field) specs.push(field);
      specs.push(...extractCompositeSpecs(cells[0], cells[1]));
    }
  });
  // Xiaomi's official specification pages use paired label/value blocks, not tables.
  $('span.f-bold').each((_, labelElement) => {
    const label = clean($(labelElement).text());
    const valueBlock = $(labelElement).parent().next();
    if (!valueBlock.length) return;
    const firstValue = clean(valueBlock.find('span').first().text());
    const field = parseField(label, firstValue, device.category_id);
    if (field) specs.push(field);
  });
  for (const product of products) {
    for (const property of product.additionalProperty || []) {
      const field = parseField(property.name, property.value, device.category_id);
      if (field) specs.push(field);
    }
  }
  const unambiguous = [];
  for (const key of new Set(specs.map(x => x.key))) {
    const values = specs.filter(x => x.key === key);
    if (new Set(values.map(x => normalized(x.value))).size === 1) unambiguous.push(values[0]);
  }
  const prices = [];
  for (const product of products) {
    for (const offer of (Array.isArray(product.offers) ? product.offers : [product.offers]).filter(Boolean)) {
      if (String(offer.priceCurrency || '').toUpperCase() !== 'PHP') continue;
      const price = Number(String(offer.price || '').replace(/,/g, ''));
      if (!Number.isFinite(price) || price <= 0) continue;
      const offerText = clean(`${product.name || ''} ${offer.name || ''} ${offer.sku || ''}`);
      const matches = configurations.filter(config => {
        const ram = config.ram_gb && new RegExp(`\\b${config.ram_gb}\\s*GB\\b`, 'i').test(offerText);
        const storage = config.internal_storage_gb && new RegExp(`\\b${config.internal_storage_gb}\\s*GB\\b`, 'i').test(offerText);
        return config.sku && offer.sku ? config.sku === offer.sku : ram && storage;
      });
      prices.push({ amount_php: price, configuration_id: matches.length === 1 ? matches[0].configuration_id : null, configuration_match: matches.length === 1 ? 'exact' : 'unspecified', variant_ram_gb: matches.length === 1 ? matches[0].ram_gb : null, variant_storage_gb: matches.length === 1 ? matches[0].internal_storage_gb : null, price_type: 'observed_offer', source_published_at: publishedAt, excerpt: `Product offer: ${offerText}; PHP ${price}`.slice(0, 240) });
    }
  }
  if (sourceKind === 'independent_ph_reference') {
    $('tr').each((_, row) => {
      const cells = $(row).find('th,td').map((__, el) => clean($(el).text())).get();
      if (cells.length !== 2 || cells[0].toLowerCase() !== 'price') return;
      const pattern = /₱\s*([\d,]+(?:\.\d{2})?)\s*Official price of\s*(\d+)\s*GB\s*\+\s*(\d+)\s*GB\s*variant/gi;
      for (const match of cells[1].matchAll(pattern)) {
        const amount = Number(match[1].replace(/,/g, ''));
        const ram = Number(match[2]);
        const storage = Number(match[3]);
        const matching = configurations.filter(x => x.ram_gb === ram && x.internal_storage_gb === storage);
        prices.push({ amount_php: amount, configuration_id: matching.length === 1 ? matching[0].configuration_id : null, configuration_match: matching.length === 1 ? 'exact' : 'source_variant_unmatched', variant_ram_gb: ram, variant_storage_gb: storage, price_type: 'independent_reported_official_price', source_published_at: publishedAt, excerpt: clean(match[0]) });
      }
      if (!prices.length && /official price\b/i.test(cells[1])) {
        const amounts = [...cells[1].matchAll(/₱\s*([\d,]+(?:\.\d{2})?)/g)];
        if (amounts.length === 1) prices.push({ amount_php: Number(amounts[0][1].replace(/,/g, '')), configuration_id: null, configuration_match: 'unspecified', variant_ram_gb: null, variant_storage_gb: null, price_type: 'independent_reported_official_price', source_published_at: publishedAt, excerpt: clean(cells[1]).slice(0, 240) });
      }
    });
  }
  return { status: products.length || unambiguous.length ? 'extracted' : 'no_structured_data', title, specs: unambiguous, prices };
}

async function ptgSitemapMatches(models, brandById) {
  const sitemapPaths = ['smartphones-sitemap.xml', 'smartphones-sitemap2.xml', 'tablets-sitemap.xml'];
  const urls = [];
  for (const path of sitemapPaths) {
    const url = `https://${ptgHost}/${path}`;
    if (!(await canFetch(url)).allowed) return new Map();
    const response = await fetchText(url);
    if (response.status !== 200) continue;
    const $ = load(response.text, { xmlMode: true });
    $('url > loc').each((_, element) => {
      const found = clean($(element).text());
      if (ptgUrl(found)) urls.push(found);
    });
    await sleep(1500);
  }
  const bySlug = new Map();
  for (const url of urls) {
    const parts = new URL(url).pathname.split('/').filter(Boolean);
    const slug = parts.at(-1).replace(/-/g, ' ');
    bySlug.set(`${parts[0]}:${normalized(slug)}`, url);
  }
  const matches = new Map();
  for (const model of models) {
    const brand = brandById.get(model.brand_id) || '';
    const names = [model.model_name, `${brand} ${model.model_name}`];
    const category = model.category_id === 'tablets' ? 'tablets' : 'smartphones';
    const match = names.map(name => bySlug.get(`${category}:${normalized(name)}`)).find(Boolean);
    if (match) matches.set(model.device_id, match);
  }
  const usedUrls = new Map();
  for (const url of matches.values()) usedUrls.set(url, (usedUrls.get(url) || 0) + 1);
  for (const [deviceId, url] of matches) if (usedUrls.get(url) > 1) matches.delete(deviceId);
  return matches;
}

async function discover(model, brand) {
  if (!process.env.BRAVE_SEARCH_API_KEY) return [];
  const q = `"${brand}" "${model.model_name}" Philippines official specs price`;
  const url = `https://api.search.brave.com/res/v1/web/search?${new URLSearchParams({ q, country: 'PH', count: '10' })}`;
  const result = await fetchText(url, { 'x-subscription-token': process.env.BRAVE_SEARCH_API_KEY, accept: 'application/json' });
  if (result.status !== 200) return [];
  try {
    return (JSON.parse(result.text).web?.results || []).map(x => x.url).filter(officialUrl).slice(0, 3);
  } catch { return []; }
}

export function gsmarenaReferenceUrl(candidate, model, brand) {
  try {
    const parsed = new URL(candidate);
    const slug = parsed.pathname.match(/^\/([a-z0-9_+-]+)-\d+\.php$/i)?.[1]?.replace(/_/g, ' ');
    return parsed.protocol === 'https:' && ['www.gsmarena.com', 'm.gsmarena.com'].includes(parsed.hostname)
      && !!slug && exactModelMention(slug, model) && boundaryMatch(slug, brand);
  } catch { return false; }
}

// GSMArena is a human review reference only. Its terms do not permit copying
// page content or images into our database or website without permission.
async function discoverGsmaReference(model, brand) {
  if (!process.env.BRAVE_SEARCH_API_KEY) return [];
  const q = `site:gsmarena.com "${brand} ${model.model_name}"`;
  const url = `https://api.search.brave.com/res/v1/web/search?${new URLSearchParams({ q, count: '5' })}`;
  const result = await fetchText(url, { 'x-subscription-token': process.env.BRAVE_SEARCH_API_KEY, accept: 'application/json' });
  if (result.status !== 200) return [];
  try {
    return (JSON.parse(result.text).web?.results || []).map(x => x.url)
      .filter(candidate => gsmarenaReferenceUrl(candidate, model.model_name, brand)).slice(0, 1);
  } catch { return []; }
}

async function main() {
  const tables = JSON.parse(await readFile(inventoryPath, 'utf8')).tables;
  const brandById = new Map(tables.brands.map(x => [x.brand_id, x.brand_name]));
  const sourceById = new Map(tables.data_sources.map(x => [x.source_id, x]));
  const evidenceByDevice = new Map();
  for (const evidence of tables.device_source_evidence) {
    const source = sourceById.get(evidence.source_id);
    if (source?.source_url) evidenceByDevice.set(evidence.device_id, [...(evidenceByDevice.get(evidence.device_id) || []), source.source_url]);
  }
  const configsByDevice = new Map();
  for (const config of tables.device_configurations) configsByDevice.set(config.device_id, [...(configsByDevice.get(config.device_id) || []), config]);
  const all = tables.device_models.filter(x => ['smartphones', 'tablets', 'laptops'].includes(x.category_id));
  const requested = requestedDeviceId ? all.filter(x => x.device_id === requestedDeviceId) : all;
  if (requestedDeviceId && requested.length !== 1) throw new Error(`Expected one inventory record for ${requestedDeviceId}; found ${requested.length}`);
  const selected = limit > 0 ? requested.slice(0, limit) : requested;
  const ptgModels = selected.filter(x => ['smartphones', 'tablets'].includes(x.category_id));
  const ptgMatches = await ptgSitemapMatches(ptgModels, brandById);
  const discoveryCandidates = selected.filter(x => !evidenceByDevice.has(x.device_id) && !ptgMatches.has(x.device_id));
  // Rotate discovery over the full queue so repeated scheduled runs cover every model.
  const week = Math.floor(Date.now() / (7 * 86400_000));
  const rotating = discoveryCandidates.length ? [...discoveryCandidates.slice((week * discoveryLimit) % discoveryCandidates.length), ...discoveryCandidates.slice(0, (week * discoveryLimit) % discoveryCandidates.length)] : [];
  const discoverIds = new Set(rotating.slice(0, discoveryLimit).map(x => x.device_id));
  const gsmStart = all.length ? (week * gsmarenaLimit) % all.length : 0;
  const gsmRotation = [...all.slice(gsmStart), ...all.slice(0, gsmStart)];
  const gsmIds = new Set(gsmRotation.slice(0, gsmarenaLimit).map(x => x.device_id));
  const ptgCandidates = selected.filter(x => ptgMatches.has(x.device_id));
  const ptgStart = ptgCandidates.length ? (week * ptgLimit) % ptgCandidates.length : 0;
  const ptgRotation = [...ptgCandidates.slice(ptgStart), ...ptgCandidates.slice(0, ptgStart)];
  const ptgFetchIds = new Set(ptgRotation.slice(0, ptgLimit).map(x => x.device_id));
  const result = { run_at: now, inventory_count: all.length, selected_count: selected.length, models: [], fetches: [], observations: [], prices: [], discovery: [] };
  for (const [device_id, source_url] of ptgMatches) result.discovery.push({ device_id, source_url, source_kind: 'independent_ph_reference', status: 'unreviewed_sitemap_candidate' });
  const lastRequest = new Map();
  for (const [index, model] of selected.entries()) {
    const brand = brandById.get(model.brand_id) || '';
    const known = [...new Set(evidenceByDevice.get(model.device_id) || [])].filter(officialUrl);
    const discovered = discoverIds.has(model.device_id) ? await discover(model, brand) : [];
    const gsmReferences = gsmIds.has(model.device_id) ? await discoverGsmaReference(model, brand) : [];
    const urls = [...new Set([...known, ...discovered])].slice(0, 3).map(url => ({ url, source_kind: 'official' }));
    if (ptgFetchIds.has(model.device_id)) urls.push({ url: ptgMatches.get(model.device_id), source_kind: 'independent_ph_reference' });
    result.models.push({ device_id: model.device_id, brand, model_name: model.model_name, category: model.category_id, status: urls.length ? 'source_queued' : ptgMatches.has(model.device_id) ? 'source_candidate' : 'needs_source_discovery' });
    for (const url of discovered) result.discovery.push({ device_id: model.device_id, source_url: url, source_kind: 'official', status: 'unreviewed_search_candidate' });
    for (const url of gsmReferences) result.discovery.push({ device_id: model.device_id, source_url: url, source_kind: 'gsmarena_review_link', status: 'unreviewed_link_candidate' });
    for (const { url, source_kind } of urls) {
      const robot = await canFetch(url);
      if (!robot.allowed) { result.fetches.push({ device_id: model.device_id, source_url: url, source_kind, status: robot.reason }); continue; }
      const origin = new URL(url).origin;
      const elapsed = Date.now() - (lastRequest.get(origin) || 0);
      if (elapsed < 1500) await sleep(1500 - elapsed);
      lastRequest.set(origin, Date.now());
      const page = await fetchText(url);
      if (page.error || page.status !== 200 || !page.contentType.toLowerCase().includes('text/html')) {
        result.fetches.push({ device_id: model.device_id, source_url: url, source_kind, status: page.error || `http_${page.status}`, http_status: page.status || null });
        continue;
      }
      if (!(officialUrl(page.url) || ptgUrl(page.url)) || !(await canFetch(page.url)).allowed) {
        result.fetches.push({ device_id: model.device_id, source_url: url, source_kind, status: 'redirect_not_allowed' });
        continue;
      }
      const extracted = extractPage(page.text, model, configsByDevice.get(model.device_id) || [], source_kind);
      result.fetches.push({ device_id: model.device_id, source_url: page.url, source_kind, status: extracted.status, http_status: 200, page_title: extracted.title });
      for (const spec of extracted.specs) result.observations.push({ device_id: model.device_id, ...spec, source_url: page.url, source_kind, observed_at: now, local_availability_verified: false });
      for (const price of extracted.prices) result.prices.push({ device_id: model.device_id, ...price, source_url: page.url, source_kind, observed_at: now, local_availability_verified: false });
    }
    if ((index + 1) % 25 === 0) console.log(`Processed ${index + 1}/${selected.length} models`);
  }
  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(result, null, 2)}\n`);
  console.log(JSON.stringify({ inventory: all.length, selected: selected.length, fetched: result.fetches.length, extracted: result.fetches.filter(x => x.status === 'extracted').length, specs: result.observations.length, prices: result.prices.length, discovery: result.discovery.length, output: outputPath }, null, 2));
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) main().catch(error => { console.error(error); process.exitCode = 1; });
