<script>
	import { page } from '$app/stores';

	import CharmSquareTick from '~icons/charm/square-tick';
	import CharmSquareCross from '~icons/charm/square-cross';

	import Page from '$lib/components/Page.svelte';
	import HorizontalBar from '$lib/components/HorizontalBar.svelte';
	import SmallStat from '$lib/components/SmallStat.svelte';
	import Title from '$lib/components/Title.svelte';
	import PartySquareListTile from '$lib/components/PartySquareListTile.svelte';
	import Heading from '$lib/components/Heading.svelte';
	import LargeCard from '$lib/components/LargeCard.svelte';

	import { getRunsInRiding, isRealParty, isRealOccupation } from '$lib/stats.js';
	import { formatString, formatNumber } from '$lib/utils.js';
	import { PARTIES, PROVINCES, ELECTION_TYPE } from '$lib/constants.js';

	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	$: candidate = candidates[$page.params.candidateId];

	$: candidateRuns = Object.entries(runs).filter(
		([runId, run]) => run.candidate === $page.params.candidateId
	);
	$: jobsAndYears = candidateRuns
		.filter(([runId, run]) => isRealOccupation(run.occupation))
		.map(([runId, run]) => {
			return {
				job: run.occupation,
				year: elections[run.election].date.year
			};
		});
	$: totalVotes = candidateRuns.reduce((acc, [runId, run]) => acc + run.votes, 0);
	$: totalWins = candidateRuns.filter(([runId, run]) => run.result != 'DEFEATED').length;
	$: candidateParties = candidateRuns
		.map(([runId, run]) => run.party)
		.filter((value, index, self) => self.indexOf(value) === index && isRealParty(value))
		.map((partyId) => {
			return {
				partyId: partyId,
				label: PARTIES[parties[partyId].name],
				link: `/elections/parties/${partyId}`
			};
		});
	$: barData = candidateRuns
		.map(([_, candidateRun]) => getRunsInRiding(candidateRun.election, candidateRun.riding))
		.map((electionRuns) =>
			electionRuns.map((run) => {
				return {
					primaryLabel: `${candidates[run.candidate].first_name} ${candidates[run.candidate].last_name}`,
					primaryLink: `/elections/candidates/${run.candidate}`,
					secondaryLabel: `${PARTIES[parties[run.party].name]}`,
					secondaryLink: isRealParty(run.party) ? `/elections/parties/${run.party}` : null,
					count: run.votes > 0 ? run.votes : 'Acclaimed',
					color: parties[run.party].color
				};
			})
		);
</script>

<svelte:head>
	<title>{candidate.first_name} {candidate.last_name}</title>
</svelte:head>

<Page>
	<Title text={`${candidate.first_name} ${candidate.last_name}`} />

	<Heading text="Statistics" />
	<div class="flex flex-row space-x-6 mb-2 overflow-x-scroll">
		<SmallStat name="Races" value={formatNumber(candidateRuns.length)} />
		<SmallStat name="Race Wins" value={formatNumber(totalWins)} />
		<SmallStat name="Total Votes" value={formatNumber(totalVotes)} />
	</div>

	{#if candidateParties.length > 0}
		<Heading text="Affiliated Parties" />
		<PartySquareListTile data={candidateParties} />
	{/if}

	<Heading text="Electoral Record" />
	<div class="flex flex-col w-full">
		{#each candidateRuns as [runId, run], i}
			<div class="flex flex-col items-start rounded w-full mt-2 mb-6">
				<div class="flex flex-row items-center mb-1 text-sm w-full">
					<div class="text-md ml-2 mr-3">
						{#if run.result != 'DEFEATED'}
							<CharmSquareTick class="text-sol-green" />
						{:else if run.result == 'DEFEATED'}
							<CharmSquareCross class="text-sol-red" />
						{/if}
					</div>
					<a class="font-bold mr-2 hover:underline decoration-dotted" href={`/elections/ridings/${run.riding}`}>
						{formatString(ridings[run.riding].name)}
					</a>
					<p class="text-md grow hidden sm:block">
						&mdash; {PROVINCES[ridings[run.riding].province]}
					</p>
					<a class="text-sol-dark1 dark:text-sol-light1 mr-2 grow text-right hover:underline decoration-dotted" href={`/elections/elections/${run.election}`}>
						{elections[run.election].date.year}
						{ELECTION_TYPE[elections[run.election].type]}
					</a>
				</div>
				<div class="flex flex-row items-center w-full">
					<div class="bg-sol-light2 dark:bg-sol-dark2 rounded-lg py-2 sm:py-3 sm:px-2 w-full">
						<HorizontalBar data={barData[i]} showTotal={false} />
					</div>
				</div>
			</div>
		{/each}
	</div>

	{#if jobsAndYears.length > 0}
		<Heading text="Occupation History" />
		<div
			class="rounded-lg bg-sol-light2 dark:bg-sol-dark2 py-3 px-4 text-sm mb-2 overflow-x-scroll sm:w-min"
		>
			<div class="w-min">
				{#each jobsAndYears as jobAndYear}
					<div class="flex flex-row">
						<p class="font-bold grow whitespace-nowrap mr-10">
							{jobAndYear.job == null ? 'Unknown' : jobAndYear.job}
						</p>
						<p class="">{jobAndYear.year}</p>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</Page>
