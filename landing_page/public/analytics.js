// Vercel Web Analytics (plain HTML setup, no package needed).
// https://vercel.com/docs/analytics/quickstart
//
// The tracking script is served by Vercel at /_vercel/insights/script.js, so
// it only exists on Vercel deployments. Skip it on Firebase Hosting and local
// previews, where the request would 404.
(function () {
  window.va =
    window.va ||
    function () {
      (window.vaq = window.vaq || []).push(arguments);
    };

  var host = location.hostname;
  var notVercel =
    host === "localhost" ||
    host === "127.0.0.1" ||
    /\.(web\.app|firebaseapp\.com)$/.test(host);
  if (notVercel) return;

  var script = document.createElement("script");
  script.defer = true;
  script.src = "/_vercel/insights/script.js";
  document.head.appendChild(script);
})();
