import adapter from '@sveltejs/adapter-vercel';

export default {
	kit: {
		adapter: adapter(),
		alias: {
			$static: 'static',
		}
	},
	onwarn: (warning, handler) => {
		if (warning.code === 'a11y-click-events-have-key-events') return
		if (warning.code === 'a11y-no-static-element-interactions') return
		handler(warning)
	},
};
