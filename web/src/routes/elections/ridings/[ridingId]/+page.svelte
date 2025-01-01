<script>
	import { page } from '$app/stores';

	import Page from '$lib/components/Page.svelte';
	import Title from '$lib/components/Title.svelte';
	import SubTitle from '$lib/components/SubTitle.svelte';
	import Riding from '$lib/components/Riding.svelte';
	import Paragraph from '$lib/components/Paragraph.svelte';
	import LargeCard from '$lib/components/LargeCard.svelte';
	import HorizontalBar from '$lib/components/HorizontalBar.svelte';

	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	import { getSortedElectionsFromRiding, getSortedElectionRidingRuns } from '$lib/stats.js';
	import { formatString } from '$lib/utils.js';
	import { PARTIES, PROVINCES, ELECTION_TYPE } from '$lib/constants.js';

	$: riding = ridings[$page.params.ridingId];
	$: electionData = getSortedElectionsFromRiding($page.params.ridingId)
		.toReversed()
		.map((electionId) => {
			const election = elections[electionId];
			return {
				...election,
				barData: getSortedElectionRidingRuns(electionId, $page.params.ridingId).map((run) => {
					const candidate = candidates[run.candidate];
					const party = parties[run.party];
					return {
						primaryLabel: `${candidate.first_name} ${candidate.last_name}`,
						primaryLink: `/elections/candidates/${run.candidate}`,
						secondaryLabel: `${PARTIES[party.name]}`,
						secondaryLink: `/elections/parties/${run.party}`,
						count: run.votes,
						color: party.color
					};
				})
			};
		});
</script>

<svelte:head>
	<title>{formatString(riding.name)}</title>
</svelte:head>

<Page>
	<Title text={formatString(riding.name)} />
	<SubTitle
		text={PROVINCES[riding.province] +
			', ' +
			riding.start_date.year +
			'–' +
			(riding.end_date ? riding.end_date.year : '')}
	/>

	<div
		class="flex flex-col-reverse sm:flex-row justify-center w-full mt-6 sm:mt-8 space-x-0 space-y-4 space-y-reverse sm:space-y-0 sm:space-x-8"
	>
		{#if riding.summary}
			<div class="grow">
				<Paragraph wikiLink={riding.summary_url} paragraphs={riding.summary} />
			</div>
		{:else}
			<p class="grow">No summary available for this riding.</p>
		{/if}
		<div class="bg-sol-light2 dark:bg-sol-dark2 rounded-lg p-2 sm:min-w-56">
			<Riding ridingId={$page.params.ridingId} />
		</div>
	</div>

	<div class="flex flex-col space-y-8 mt-8 sm:mt-12">
		{#each electionData as election}
			<LargeCard title={election.date.year + ' ' + ELECTION_TYPE[election.type]}>
				<HorizontalBar data={election.barData} showTotal={false} />
			</LargeCard>
		{/each}
	</div>
</Page>
