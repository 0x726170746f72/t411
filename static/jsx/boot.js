function load_components(e) {
  var s = document.createElement('script');
  s.src = static_root + 'js/components.js';
  s.addEventListener('load', boot);
  s.addEventListener('error', function() { alert('Impossible de charger le site.'); }); // TODO: changer
  document.head.appendChild(s);
}

function boot() {
  document.head.removeChild(this);
  ReactDOM.render(<Root />, $('#root')[0]);
}

window.addEventListener('load', load_components);
