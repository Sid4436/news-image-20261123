// news-image-20261123: copies the pre-rendered entry.png (made by render.py) to the output dir.
// Byte-identical on every run: no rendering, no timestamps, just a copy.
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const out = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const src = fileURLToPath(new URL('./entry.png', import.meta.url));
mkdirSync(out, { recursive: true });
copyFileSync(src, join(out, 'entry.png'));
