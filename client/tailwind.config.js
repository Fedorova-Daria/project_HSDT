// tailwind.config.js
import typography from '@tailwindcss/typography';

export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [typography], // Убедись, что плагины правильно подключены
};