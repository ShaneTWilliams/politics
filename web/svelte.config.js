import adapter from '@sveltejs/adapter-vercel';

export default {
	kit: {
		adapter: adapter(),
		alias: {
			$static: 'static',
		}
	},
	onwarn: (warning, handler) => {
		handler(warning)
	},
};
