import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFile, access } from 'node:fs/promises';
import { resolve } from 'node:path';
import sharp from 'sharp';

const root = resolve(import.meta.dirname, '..');
const catalog = JSON.parse(await readFile(resolve(root, 'lib/catalog/public-inventory.json'), 'utf8'));
const manifest = JSON.parse(await readFile(resolve(root, 'lib/catalog/image-manifest.json'), 'utf8'));

test('every public catalog device has a readable local image and source', async () => {
  for (const device of catalog) {
    const image = manifest[device.imageId];
    assert.ok(image, `Missing image for ${device.brand} ${device.model}`);
    assert.match(image.path, /^\/catalog-images\/[a-z0-9_-]+\.webp$/);
    assert.match(image.sourcePage, /^https:\/\//);
    assert.match(image.assetUrl, /^https:\/\//);
    const file = resolve(root, `public${image.path}`);
    await access(file);
    const metadata = await sharp(file).metadata();
    assert.ok(metadata.width >= 160 && metadata.height >= 160, `Image too small: ${device.model}`);
  }
});
