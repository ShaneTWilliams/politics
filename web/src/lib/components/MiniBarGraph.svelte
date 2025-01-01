<script>
	import { getTopNSeatCounts } from '$lib/stats.js';

	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	import { FILL_COLOURS } from '$lib/constants.js';

	export let electionId;

	$: electionResults = Object.fromEntries(
		Object.entries(elections)
			.filter(([electionId, election]) => {
				return election.type === 'GENERAL';
			})
			.map(([electionId, election]) => {
				return [
					electionId,
					{
						counts: getTopNSeatCounts(electionId, 3),
						maxCount: Math.max(
							...Object.values(getTopNSeatCounts(electionId, 3)).map(([_, count]) => count)
						)
					}
				];
			})
	);
</script>

<div class="flex flex-row mr-8">
	{#each electionResults[electionId].counts as [party, seats]}
		<div class="px-[1px] h-5 w-3 flex flex-col justify-end">
			<div
				class={`${FILL_COLOURS[parties[party].color]}`}
				style={`height: ${(seats * 100) / electionResults[electionId].maxCount}%`}
			/>
		</div>
	{/each}
</div>
