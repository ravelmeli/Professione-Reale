import { bundle } from '@remotion/bundler';
import { renderStill, selectComposition } from '@remotion/renderer';
import fs from 'fs';
const out = process.argv[2] || '/tmp/claude-0/stills';
fs.mkdirSync(out, { recursive: true });
const serveUrl = await bundle({ entryPoint: new URL('../src/index.ts', import.meta.url).pathname, webpackOverride: (c) => c });
const comp = await selectComposition({ serveUrl, id: 'First90', browserExecutable: '/opt/pw-browsers/chromium', chromiumOptions: { gl: 'swangle' } });
const starts = JSON.parse(fs.readFileSync(new URL('./starts.json', import.meta.url)));
const end = starts.end;
let n = 0;
for (let i = 0; i < starts.s.length; i++) {
  const a = starts.s[i], b = i + 1 < starts.s.length ? starts.s[i + 1] : end;
  for (const [k, q] of [['a', 0.03], ['b', 0.5], ['c', 0.96]]) {
    const frame = Math.min(comp.durationInFrames - 1, Math.round((a + (b - a) * q) * 30));
    await renderStill({ composition: comp, serveUrl, output: `${out}/b${String(i + 1).padStart(2, '0')}${k}.jpg`, frame, imageFormat: 'jpeg', jpegQuality: 70, browserExecutable: '/opt/pw-browsers/chromium', chromiumOptions: { gl: 'swangle' }, scale: 0.34 });
    n++;
  }
}
console.log('stills', n);
