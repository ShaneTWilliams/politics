import adapter from '@sveltejs/adapter-vercel';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';


export default {
	kit: {
		adapter: adapter({

		}),
	},
	onwarn: (warning, handler) => {
		if (warning.code === 'a11y-click-events-have-key-events') return
		if (warning.code === 'a11y-no-static-element-interactions') return
		handler(warning)
	},
};
