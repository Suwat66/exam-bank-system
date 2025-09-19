const defaultTheme = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
    './**/forms.py'
  ],
  theme: {
    extend: {
      fontFamily: {
        // --- เปลี่ยนชื่อฟอนต์ตรงนี้ ---
        sans: ['Prompt', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}