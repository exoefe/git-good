// Node 18+
// Scans images/*/** and builds public/gallery.json
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const IMAGES_DIR = path.join(ROOT, 'images');
const OUT = path.join(ROOT, 'public', 'gallery.json');

function findAllImages(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const out = [];
  for (const e of entries) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...findAllImages(p));
    else if (/\.(png|jpe?g|gif|webp|avif|svg)$/i.test(e.name)) out.push(p);
  }
  return out;
}

function readMeta(folder) {
  const yfile = path.join(folder, 'meta.yaml');
  if (!fs.existsSync(yfile)) return {};
  const raw = fs.readFileSync(yfile, 'utf8');
  // ultra-minimal YAML: key: value per line
  const meta = {};
  raw.split(/\r?\n/).forEach(line => {
    const m = line.match(/^\s*([A-Za-z0-9_-]+)\s*:\s*(.*)\s*$/);
    if (m) meta[m[1].toLowerCase()] = m[2].replace(/^"|"$/g, '');
  });
  return meta;
}

const imgs = findAllImages(IMAGES_DIR);
const items = imgs.map(abs => {
  const rel = abs.replace(ROOT + path.sep, '').split(path.sep).join('/');
  const parts = rel.split('/');
  const user = parts[1]; // images/<user>/file
  const folder = path.join(IMAGES_DIR, user);
  const meta = readMeta(folder);
  return {
    user,
    src: '/' + rel,      // served from repo root in Pages build
    theme: meta.theme || '',
    caption: meta.caption || '',
    credit: meta.credit || ''
  };
});

// deterministic order: by user, then filename
items.sort((a, b) => (a.user + a.src).localeCompare(b.user + b.src));

fs.writeFileSync(OUT, JSON.stringify(items, null, 2));
console.log(`Wrote ${items.length} items to ${path.relative(ROOT, OUT)}`);

