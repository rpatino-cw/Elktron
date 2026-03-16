// Browser-Sync config for escort-bot development
// Serves from hackathon root so ../glb/ paths resolve correctly
// Usage: cd escort-bot && browser-sync start --config bs-config.js
// URL: http://localhost:8081/escort-bot/assembly.html
module.exports = {
  server: "..",
  files: ["*.html", "*.css", "*.js"],
  port: 8081,
  open: false,
  notify: false,
  ui: { port: 8082 },
  ghostMode: false,
  reloadDebounce: 300,
  startPath: "/escort-bot/assembly.html"
};
