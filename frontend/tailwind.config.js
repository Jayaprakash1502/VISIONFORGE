/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        vf: {
          bg: '#F7F6FB',
          card: '#FFFFFF',
          border: '#E2DFEC',
          primary: '#8B7FC7',
          primaryHover: '#A99BE0',
          text: '#242331',
          muted: '#AAA6BA',
          success: '#5FBF9F',
          warning: '#D6AE62',
          critical: '#D87586',
        }
      }
    },
  },
  plugins: [],
}
