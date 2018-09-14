var CACHE_NAME = 'static-v1';

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll([
        '/',
        '../../css/bootstrap4.min.css',
        '../../css/custom.css',
        '../../css/bootstrap-select.min.css',
        '/manifest.json',
        '/jquery.min.js',
        '/bootstrap.min.js',
        '/vendor/bootstrap-select.js',
        'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.min.js',
        '/src/candidate.js'
      ]);
    })
  )
});

self.addEventListener('activate', function activator(event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys
        .filter(function (key) {
          return key.indexOf(CACHE_NAME) !== 0;
        })
        .map(function (key) {
          return caches.delete(key);
        })
      );
    })
  );
});

self.addEventListener('fetch', function (event) {
  event.respondWith(
    caches.match(event.request).then(function (cachedResponse) {
      return cachedResponse || fetch(event.request);
    })
  );
});