const C='valiryan-v1',F=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(F)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C&&x!=='valiryan-share').map(x=>caches.delete(x)))));self.clients.claim()});
self.addEventListener('fetch',e=>{
 const r=e.request,u=new URL(r.url);
 if(r.method==='POST'&&u.pathname.endsWith('/share-target')){
  e.respondWith((async()=>{
   try{
    const fd=await r.formData(),c=await caches.open('valiryan-share');let i=0;
    for(const f of fd.getAll('media')){
     if(f&&typeof f!=='string')await c.put(new Request(new URL('./__shared/file/'+(i++),self.registration.scope).href),new Response(f,{headers:{'x-name':encodeURIComponent(f.name||'shared'),'content-type':f.type||'application/octet-stream'}}));
    }
    const t=['title','text','url'].map(k=>fd.get(k)).filter(x=>typeof x==='string'&&x).join(' ');
    if(t)await c.put(new Request(new URL('./__shared/text',self.registration.scope).href),new Response(t));
   }catch(_){}
   return Response.redirect(new URL('./index.html?shared=1',self.registration.scope).href,303);
  })());
  return;
 }
 if(r.method!=='GET')return;
 e.respondWith(fetch(r).then(res=>{if(res.ok&&u.origin===location.origin){const cp=res.clone();caches.open(C).then(c=>c.put(r,cp))}return res}).catch(()=>caches.match(r).then(m=>m||caches.match('./index.html'))));
});
