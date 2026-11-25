#!/usr/bin/env node
// Curated manufacturer images for the verified public catalog.
import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { load } from 'cheerio';
import sharp from 'sharp';
import { canFetch } from './enrich_devices.mjs';

const root = resolve(import.meta.dirname, '..');
const sourcesPath = resolve(root, 'research/catalog-image-sources.json');
const catalogPath = resolve(root, 'lib/catalog/public-inventory.json');
const manifestPath = resolve(root, 'lib/catalog/image-manifest.json');
const force = process.argv.includes('--force');
const selectedId = process.argv.includes('--device-id') ? process.argv[process.argv.indexOf('--device-id') + 1] : null;
const agent = 'DeviceIQResearchBot/1.0 (+https://github.com/ynee6969/Device-IQ; catalog imagery)';
const allowedHosts = new Set(['images.samsung.com', 'dlcdnwebimgs.asus.com']);

function reusableRights(source) {
  if (source.rightsStatus === 'LICENSED') {
    return Boolean(source.licenseUrl && source.usageTerms && source.credit);
  }
  if (source.rightsStatus === 'PERMISSION_GRANTED') {
    return Boolean(source.permissionEvidenceUrl && source.usageTerms && source.credit);
  }
  return false;
}

async function get(url, maxBytes, wantImage = false) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 20000);
  try {
    const response = await fetch(url, { signal: controller.signal, headers: { 'user-agent': agent } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    if (Number(response.headers.get('content-length') || 0) > maxBytes) throw new Error('Response too large');
    const type = response.headers.get('content-type') || '';
    if (!type.includes(wantImage ? 'image/' : 'text/html')) throw new Error(`Unexpected content type: ${type}`);
    const bytes = Buffer.from(await response.arrayBuffer());
    if (bytes.length > maxBytes) throw new Error('Response too large');
    return { bytes, finalUrl: response.url };
  } finally { clearTimeout(timer); }
}

function productImages(object) {
  if (!object || typeof object !== 'object') return [];
  const objects = [object, ...(Array.isArray(object['@graph']) ? object['@graph'] : [])];
  return objects.flatMap(item => {
    if (item['@type'] !== 'Product' && !(Array.isArray(item['@type']) && item['@type'].includes('Product'))) return [];
    const images = Array.isArray(item.image) ? item.image : [item.image];
    return images.map(image => typeof image === 'string' ? image : image?.url).filter(Boolean);
  });
}

async function assetFor(source) {
  if (source.method === 'direct') return source.assetUrl;
  if (!(await canFetch(source.pageUrl)).allowed) throw new Error('Source page blocked by robots.txt');
  const page = await get(source.pageUrl, 8_000_000);
  const $ = load(page.bytes.toString('utf8'));
  if (source.method === 'og') {
    const image = $('meta[property="og:image"]').attr('content');
    if (!image) throw new Error('No og:image on source page');
    return new URL(image, page.finalUrl).href;
  }
  if (source.method === 'product') {
    const images = [];
    $('script[type="application/ld+json"]').each((_, el) => {
      try { images.push(...productImages(JSON.parse($(el).html()))); } catch { /* malformed JSON-LD */ }
    });
    if (!images.length) throw new Error('No Product image on source page');
    return new URL(images[0], page.finalUrl).href;
  }
  throw new Error(`Unsupported source method: ${source.method}`);
}

async function main() {
  const sources = JSON.parse(await readFile(sourcesPath, 'utf8'));
  const catalog = JSON.parse(await readFile(catalogPath, 'utf8'));
  const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
  const models = new Map(catalog.map(device => [device.id, device]));
  const seen = new Set();
  const failures = [];
  for (const source of sources) {
    if (selectedId && source.deviceId !== selectedId) continue;
    const device = models.get(source.deviceId);
    if (!device || seen.has(source.deviceId)) throw new Error(`Unknown or duplicate device ID: ${source.deviceId}`);
    seen.add(source.deviceId);
    const file = resolve(root, `public/catalog-images/${source.deviceId}.webp`);
    try {
      if (source.method !== 'existing' && !reusableRights(source)) {
        throw new Error('Image reuse rights are not documented; add an approved license or written permission first');
      }
      if (source.method === 'existing') {
        const prior = manifest[source.existingImageId];
        if (!prior) throw new Error(`Missing existing image ${source.existingImageId}`);
        if (!prior.licenseUrl && !prior.permissionEvidenceUrl) throw new Error('Existing image has no documented reuse license or written permission');
        await access(resolve(root, `public${prior.path}`));
        manifest[source.deviceId] = prior;
        console.log(`Existing: ${device.brand} ${device.model}`);
        continue;
      }
      if (!force && manifest[source.deviceId]) { await access(file); console.log(`Cached: ${device.brand} ${device.model}`); continue; }
      if (!(await canFetch(source.pageUrl)).allowed) throw new Error('Source page blocked by robots.txt');
      const assetUrl = await assetFor(source);
      const asset = new URL(assetUrl);
      if (asset.protocol !== 'https:' || !allowedHosts.has(asset.hostname)) throw new Error(`Unapproved image host: ${asset.hostname}`);
      if (!(await canFetch(asset.href)).allowed) throw new Error('Image blocked by robots.txt');
      const image = await get(asset.href, 15_000_000, true);
      const finalHost = new URL(image.finalUrl).hostname;
      if (!allowedHosts.has(finalHost)) throw new Error(`Image redirected to unapproved host: ${finalHost}`);
      const meta = await sharp(image.bytes).metadata();
      if (!meta.width || !meta.height || meta.width < 160 || meta.height < 160) throw new Error('Image dimensions too small');
      await mkdir(dirname(file), { recursive: true });
      await sharp(image.bytes).rotate().resize({ width: 900, height: 650, fit: 'inside', withoutEnlargement: true }).webp({ quality: 84 }).toFile(file);
      manifest[source.deviceId] = { path: `/catalog-images/${source.deviceId}.webp`, sourcePage: source.pageUrl, assetUrl: asset.href, scope: source.scope,
        credit: source.credit, usageTerms: source.usageTerms,
        ...(source.licenseUrl ? { licenseUrl: source.licenseUrl } : {}),
        ...(source.rightsCheckedAt ? { rightsCheckedAt: source.rightsCheckedAt } : {}),
        ...(source.permissionEvidenceUrl ? { permissionEvidenceUrl: source.permissionEvidenceUrl } : {}) };
      console.log(`Added: ${device.brand} ${device.model} (${meta.width}×${meta.height})`);
    } catch (error) { failures.push({ device: `${device.brand} ${device.model}`, error: String(error.message || error) }); console.error(`Failed: ${device.brand} ${device.model}: ${error.message || error}`); }
  }
  await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
  console.log(JSON.stringify({ mapped: seen.size - failures.length, curated: selectedId ? 1 : sources.length, catalog: catalog.length, failures }, null, 2));
  if (seen.size !== (selectedId ? 1 : sources.length) || failures.length) process.exitCode = 1;
}

main().catch(error => { console.error(error); process.exitCode = 1; });
