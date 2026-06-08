const CACHE_NAME = 'treino-v1';
const urlsToCache = [
  './index.html',
  './manifest.json',
  './icon.svg'
];

// Instalação: Cache dos arquivos essenciais
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// Interceptando requisições para funcionar offline
self.addEventListener('fetch', event => {
  // Ignora requisições para a API do Supabase no Service Worker
  if (event.request.url.includes('supabase.co')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Retorna do cache se encontrar, senão busca na rede
        return response || fetch(event.request);
      })
  );
});
