<script>
	import { browser } from '$app/environment';

	import CharmCross from '~icons/charm/cross';

	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	import HorizontalBar from './HorizontalBar.svelte';
	import Map from './Map.svelte';
	import MapleLeaf from '$lib/components/icons/MapleLeaf.svelte';

	import { PARTIES, PROVINCES } from '$lib/constants.js';
	import { formatString, isSm, arrayRange } from '$lib/utils.js';

	export let electionId,
		focusParty = null;
	let innerWidth;

	$: election = elections[electionId];
	$: hoveredRiding = null;
	$: selectedRiding = null;

	const BIG_DETAIL_VIEW_IDS = [
		'MONTREAL',
		'SOUTHERN_QUEBEC',
		'TORONTO',
		'GOLDEN_HORSESHOE',
		'OTTAWA',
		'CALGARY',
		'EDMONTON',
		'VANCOUVER'
	];
	const SMALL_DETAIL_VIEW_IDS = [
		'ST_JOHNS',
		'PEI',
		'MONCTON',
		'HALIFAX',
		'QUEBEC_CITY',
		'LONDON',
		'TROIS_RIVIERES',
		'REGINA',
		'WINNIPEG',
		'ESSEX',
		'SASKATOON',
		'VICTORIA'
	];

	$: relevant_runs = [];
	$: max_votes = 0;
	$: if (selectedRiding !== null) {
		relevant_runs = [];
		max_votes = 0;
		for (const run_id of election.runs) {
			let run = runs[run_id];
			if (run.riding == selectedRiding) {
				relevant_runs.push(run);
				if (run.votes > max_votes) {
					max_votes = run.votes;
				}
			}
		}
	}
	$: relevantRunsBarData = relevant_runs.map((run) => {
		return {
			primaryLabel:
				candidates[run.candidate].first_name + ' ' + candidates[run.candidate].last_name,
			primaryLink: `/elections/candidates/${run.candidate}`,
			secondaryLabel: PARTIES[parties[run.party].name],
			secondaryLink: `/elections/parties/${run.party}`,
			count: run.result == 'ACCLAIMED' ? 'Acclaimed' : run.votes,
			color: parties[run.party].color
		};
	});

	// Determine if we're stuck to the bottom of the screen.
	let stickyElement, stuck;
	$: if (browser && stickyElement) {
		const observer = new IntersectionObserver(([e]) => (stuck = e.intersectionRatio < 1), {
			threshold: [1]
		});
		observer.observe(stickyElement);
	}

	$: mainMapDoneLoading = false;
	$: bigDetailMapsDoneLoading = Array(BIG_DETAIL_VIEW_IDS.length).fill(false);
	$: smallDetailMapsDoneLoading = Array(SMALL_DETAIL_VIEW_IDS.length).fill(false);
	$: allDoneLoading =
		mainMapDoneLoading &&
		bigDetailMapsDoneLoading.flat().every((x) => x) &&
		smallDetailMapsDoneLoading.flat().every((x) => x);
</script>

<svelte:window bind:innerWidth />

<div class="w-full">
	{#if !allDoneLoading}
		<div class="w-full flex flex-col items-center justify-center h-96">
			<div class="animate-bounce h-6 w-6 fill-sol-dark2 dark:fill-sol-light2">
				<MapleLeaf />
			</div>
		</div>
	{/if}
	<div class={`w-full ${allDoneLoading ? '' : 'opacity-0 h-0'}`}>
		<Map
			bind:selectedRiding
			bind:hoveredRiding
			bind:doneLoading={mainMapDoneLoading}
			{electionId}
			detail={false}
			viewId={null}
			clickable={true}
			{focusParty}
		/>

		{#if election.type == 'GENERAL'}
			<div class="flex flex-col space-y-2 mb-4 px-2 mt-4">
				{#each [0, 1] as row}
					<div class="flex flex-col space-y-2 sm:space-y-0 sm:flex-row sm:space-x-4 w-full">
						{#each [0, 1] as group}
							<div class="flex flex-row space-x-4 w-full min-h-24">
								{#each [0, 1] as col}
									<Map
										bind:selectedRiding
										bind:hoveredRiding
										bind:doneLoading={bigDetailMapsDoneLoading[row * 4 + group * 2 + col]}
										{electionId}
										detail={true}
										viewId={BIG_DETAIL_VIEW_IDS[row * 4 + group * 2 + col]}
										clickable={true}
										{focusParty}
									/>
								{/each}
							</div>
						{/each}
					</div>
				{/each}
			</div>
			<div class="flex flex-col space-y-2 mb-4 px-2">
				{#each [0, 1] as row}
					<div class="flex flex-col space-y-2 sm:space-y-0 sm:flex-row sm:space-x-4 w-full">
						{#each [0, 1] as group}
							<div class="flex flex-row space-x-4 w-full">
								{#each [0, 1, 2] as col}
									<Map
										bind:selectedRiding
										bind:hoveredRiding
										bind:doneLoading={smallDetailMapsDoneLoading[row * 6 + group * 3 + col]}
										{electionId}
										detail={true}
										viewId={SMALL_DETAIL_VIEW_IDS[row * 6 + group * 3 + col]}
										clickable={true}
										{focusParty}
									/>
								{/each}
							</div>
						{/each}
					</div>
				{/each}
			</div>
		{/if}

		{#if selectedRiding}
			<div class="pb-4 mt-8 sticky -bottom-[1px]" bind:this={stickyElement}>
				<div
					class={`flex flex-col items-center bg-sol-light2 dark:bg-sol-dark2 p-2 pb-4 rounded-lg w-full ${stuck ? 'shadow-[rgba(0,0,0,0.15)_0px_0px_30px_10px]' : ''}`}
				>
					<div class="flex flex-row w-full mb-2 px-4 pt-2 text-sm sm:text-md">
						<div class="flex flex-col items-center w-full grow">
							<a
								class="font-black hover:underline decoration-dotted"
								href={`/elections/ridings/${selectedRiding}`}
							>
								{formatString(ridings[selectedRiding].name)}, {PROVINCES[
									ridings[selectedRiding].province
								]}
							</a>
						</div>
						<button on:click={() => (selectedRiding = null)} class="ml-2 hover:cursor-pointer">
							<CharmCross />
						</button>
					</div>
					<HorizontalBar data={relevantRunsBarData} showTotal={relevant_runs.length > 1} />
				</div>
			</div>
		{:else}
			<div class="">
				<p class="text-center text-sm italic text-sol-light1 dark:text-sol-dark1 mt-16">
					Click on a riding to view regional statistics
				</p>
			</div>
		{/if}
	</div>
</div>
