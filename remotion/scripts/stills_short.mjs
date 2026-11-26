import { bundle } from '@remotion/bundler';
import { renderStill, selectComposition } from '@remotion/renderer';
import fs from 'fs';
const out = process.argv[2] || '/tmp/claude-0/stills_short'; const from = +process.argv[3] || 0, to = +process.argv[4] || 9999;
fs.mkdirSync(out, { recursive: true });
const serveUrl = await bundle({ entryPoint: new URL('../src/index.ts', import.meta.url).pathname });
const comp = await selectComposition({ serveUrl, id: 'Short', browserExecutable: '/opt/pw-browsers/chromium', chromiumOptions: { gl: 'swangle' } });
const items = JSON.parse(fs.readFileSync('/tmp/claude-0/items.json'));
for (let i = from; i < Math.min(items.length, to); i++) {
  if (fs.existsSync(`${out}/i${String(i).padStart(3, '0')}.jpg`)) continue;
  const a = items[i], b = i + 1 < items.length ? items[i + 1] : 84.63;
  const frame = Math.min(comp.durationInFrames - 1, Math.round((a + (b - a) * 0.55) * 30));
  await renderStill({ composition: comp, serveUrl, output: `${out}/i${String(i).padStart(3, '0')}.jpg`, frame, imageFormat: 'jpeg', jpegQuality: 70, browserExecutable: '/opt/pw-browsers/chromium', chromiumOptions: { gl: 'swangle' }, scale: 0.4 });
}
console.log('ok');
