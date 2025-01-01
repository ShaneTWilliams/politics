<script>
	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	export let title, subtitle, link;
</script>

<div class="flex flex-row w-full">
	<a
		href={link}
		class="rounded-lg bg-sol-light2 dark:bg-sol-dark2 grow flex flex-row sm:flex-col py-2 sm:py-4 px-4 sm:px-6 text-left space-x-4 sm:space-x-0 sm:space-y-1 border border-dashed hover:border-sol-dark2 hover:dark:border-sol-light1 border-transparent"
	>
		<div
			class="flex flex-row items-center justify-center rounded w-16 min-w-16 h-16 sm:w-full sm:h-48 text-5xl svg-shadow text-sol-light3 dark:text-sol-dark3 sm:py-2"
		>
			<slot />
		</div>
		<div class="flex flex-col items-start">
			<p class="text-lg sm:text-xl font-black text-sol-dark3 dark:text-sol-light3">
				{title}
			</p>
			<p class="text-xs sm:text-sm text-sol-light1 dark:text-sol-light1">
				{subtitle}
			</p>
		</div>
	</a>
</div>
