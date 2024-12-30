import adapter from '@sveltejs/adapter-vercel';

export default {
	kit: {
		adapter: adapter()
	},
	onwarn: (warning, handler) => {
		handler(warning)
	},
};
