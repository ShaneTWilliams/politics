<script>
	import { FILL_COLOURS } from '$lib/constants.js';
	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	export let partyId;
</script>

{#if partyId}
	<div class={`h-3 w-3 rounded mr-2 ${FILL_COLOURS[parties[partyId].color]}`} />
{/if}
