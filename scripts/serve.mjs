import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { createReadStream } from 'node:fs';
import { dirname, extname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '../docs');
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.xml':'application/xml','.pdf':'application/pdf','.mp4':'video/mp4','.json':'application/json; charset=utf-8','.txt':'text/plain; charset=utf-8'};
const server = createServer(async (req, res) => {
  try {
    if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405, {Allow:'GET, HEAD'}); res.end(); return; }
    let path = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    if (path === '/portfolio') { res.writeHead(302, {Location:'/portfolio/'}); res.end(); return; }
    if (path.startsWith('/portfolio/')) path = path.slice('/portfolio'.length);
    let file = resolve(root, '.' + path);
    if (file !== root && !file.startsWith(root + sep)) { res.writeHead(403); res.end(); return; }
    let info = await stat(file);
    if (info.isDirectory()) { file = resolve(file, 'index.html'); info = await stat(file); }
    const headers = {'Content-Type':types[extname(file)] || 'application/octet-stream', 'Cache-Control':'no-store', 'Accept-Ranges':'bytes'};
    let start = 0, end = info.size - 1, status = 200;
    if (req.headers.range) {
      const range = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
      if (!range || (!range[1] && !range[2])) { res.writeHead(416, {'Content-Range':`bytes */${info.size}`}); res.end(); return; }
      if (!range[1]) start = Math.max(0, info.size - Number(range[2]));
      else { start = Number(range[1]); if (range[2]) end = Math.min(end, Number(range[2])); }
      if (start > end || start >= info.size || !Number.isSafeInteger(start) || !Number.isSafeInteger(end)) { res.writeHead(416, {'Content-Range':`bytes */${info.size}`}); res.end(); return; }
      status = 206;
      headers['Content-Range'] = `bytes ${start}-${end}/${info.size}`;
    }
    headers['Content-Length'] = end - start + 1;
    res.writeHead(status, headers);
    if (req.method === 'HEAD') { res.end(); return; }
    const stream = createReadStream(file, {start, end});
    stream.on('error', () => res.destroy());
    res.on('close', () => stream.destroy());
    stream.pipe(res);
  } catch {
    if (res.headersSent) { res.destroy(); return; }
    res.writeHead(404, {'Content-Type':'text/html; charset=utf-8'});
    res.end(req.method === 'HEAD' ? undefined : await readFile(resolve(root, '404.html')));
  }
});
server.listen(4173, '127.0.0.1', () => console.log('Portfolio preview: http://127.0.0.1:4173/portfolio/'));
