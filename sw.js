// Rachna Studio service worker: app offline bhi khule (network-first, cache fallback)
const CACHE='rachna-v3';
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['./','index.html','video.html','manifest.webmanifest','icon.svg'])));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==CACHE).map(x=>caches.delete(x)))));self.clients.claim()});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.hostname.includes('pollinations'))return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();if(r.ok&&(u.origin===location.origin||u.hostname.includes('fonts.')))caches.open(CACHE).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request)));
});
