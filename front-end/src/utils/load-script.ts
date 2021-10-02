export function loadAsyncScript(src, callback) {
  const script = document.createElement('script');
  script.type = 'text/javascript';
  script.async = true;
  script.setAttribute('src', src);
  script.addEventListener('load', callback);
  document.head.appendChild(script);
}
