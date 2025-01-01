<script>
	import { onMount } from 'svelte';

	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	export let ridingId;

	let svgElement;
	let x = 0;
	let y = 0;
	let width = 0;
	let height = 0;

	$: geometryMap = ridings[ridingId].geometry_by_year;
	$: latestYear = Object.keys(geometryMap).reduce(function (a, b) {
		return geometryMap[a] > geometryMap[b] ? a : b;
	});
	$: geometryId = geometryMap[latestYear];

	let geometry = null;
	onMount(() => {
		fetch(`/geometry/${geometryId}/detailed.svg`)
			.then((response) => response.text())
			.then((response) => {
				geometry = response;
			})
			.then(() => {
				const bbox = svgElement.getBBox();
				x = bbox.x;
				y = -(bbox.y + bbox.height);
				width = bbox.width;
				height = bbox.height;
			});
	});
</script>

<svg viewBox={`${x} ${y} ${width} ${height}`} class="h-full w-full svg-shadow sm:p-4">
	<g transform="scale(1,-1)" bind:this={svgElement}>
		<g class="fill-sol-light3 dark:fill-sol-dark3">
			{@html geometry}
		</g>
	</g>
</svg>
