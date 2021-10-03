/** @type {import('next').NextConfig} */
const withPWA = require('next-pwa');

module.exports = withPWA({
  // disable default icon of nextjs at a bottom of page
  devIndicators: {
    autoPrerender: false,
  },
  pageExtensions: ['tsx'],
  pwa: {
    dest: 'public',
  },
});