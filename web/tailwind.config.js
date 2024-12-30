/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'sol-dark3': '#002027',
        'sol-dark2': '#073642',
        'sol-dark1': '#586e75',
        'sol-dark0': '#657b83',

        'sol-light0': '#839496',
        'sol-light1': '#93a1a1',
        'sol-light2': '#eee8d5',
        'sol-light3': '#fdf6e3',

        'sol-red': '#dc322f',
        'sol-orange': '#cb4b16',
        'sol-yellow': '#b58900',
        'sol-green': '#859900',
        'sol-cyan': '#2aa198',
        'sol-blue': '#268bd2',
        'sol-violet': '#6c71c4',
        'sol-magenta': '#d33682',
      }
    },
  },
  plugins: [],
}

