// Service Worker for PWA offline support
const CACHE_NAME = 'conductor-v2';
const urlsToCache = [
  '/',
  '/static/app.js',
  '/static/manifest.json',
  '/static/icon.svg'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  // Only cache GET requests for same-origin static assets
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  const isStatic = url.pathname.startsWith('/static/') || url.pathname === '/';

  if (isStatic) {
    event.respondWith(
      caches.match(event.request)
        .then(response => response || fetch(event.request).then(networkResponse => {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return networkResponse;
        }).catch(() => new Response('Offline', { status: 503, statusText: 'Service Unavailable' })))
    );
  }
});
