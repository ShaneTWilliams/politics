<script>
	import { page } from '$app/stores';

	import Page from '$lib/components/Page.svelte';
	import SmallStat from '$lib/components/SmallStat.svelte';
	import Title from '$lib/components/Title.svelte';
	import PartySquareListTile from '$lib/components/PartySquareListTile.svelte';
	import Heading from '$lib/components/Heading.svelte';
	import SubTitle from '$lib/components/SubTitle.svelte';
	import List from '$lib/components/List.svelte';

	import {
		getPartyFromCandidateAndParliament,
		getByelectionsFromParliament,
		getGeneralElectionFromParliament,
		getGeneralElectionVictor
	} from '$lib/stats.js';
	import { ordinalSuffix, formatNumber, formatString, formatDate, isSm } from '$lib/utils.js';
	import { PARTIES, GOVERNMENT_TYPE } from '$lib/constants.js';

	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	let innerWidth;

	$: parliament = parliaments[$page.params.parliamentId];

	$: primeMinisters = parliament.prime_ministers.map((pmId) => {
		return {
			partyId: getPartyFromCandidateAndParliament(pmId, $page.params.parliamentId),
			label: `${candidates[pmId].first_name} ${candidates[pmId].last_name}`,
			link: `/elections/candidates/${pmId}`
		};
	});
	$: oppoLeaders = parliament.oppo_leaders.map((oppoId) => {
		return {
			partyId: getPartyFromCandidateAndParliament(oppoId, $page.params.parliamentId),
			label: `${candidates[oppoId].first_name} ${candidates[oppoId].last_name}`,
			link: `/elections/candidates/${oppoId}`
		};
	});
	$: govParties = parliament.gov_parties.map((partyId) => {
		return {
			partyId: partyId,
			label: PARTIES[parties[partyId].name],
			link: `/elections/parties/${partyId}`
		};
	});
	$: oppoParties = parliament.oppo_parties.map((partyId) => {
		return {
			partyId: partyId,
			label: PARTIES[parties[partyId].name],
			link: `/elections/parties/${partyId}`
		};
	});

	$: generalElectionId = getGeneralElectionFromParliament($page.params.parliamentId);
	$: generalElection = elections[generalElectionId];
	$: generalElectionListData = [
		{
			title: `${generalElection.date.year} General Election`,
			subtitle: PARTIES[parties[getGeneralElectionVictor(generalElectionId)].name] + ' Victory',
			link: `/elections/elections/${generalElectionId}`,
			element: null,
			category: isSm(innerWidth) ? '' : formatDate(generalElection.date)
		}
	];

	$: byelectionListData = getByelectionsFromParliament($page.params.parliamentId).map(
		(byelectionId) => {
			const byelection = elections[byelectionId];
			return {
				title: `${formatString(ridings[byelection.riding].name)}`,
				subtitle: PARTIES[parties[runs[byelection.runs[0]].party].name] + ' Victory',
				link: `/elections/elections/${byelectionId}`,
				element: null,
				category: isSm(innerWidth) ? byelection.date.year : formatDate(byelection.date)
			};
		}
	);
</script>

<svelte:head>
	<title>{ordinalSuffix(parliament.number)} Parliament</title>
</svelte:head>
<svelte:window bind:innerWidth />

<Page>
	<Title text={`${ordinalSuffix(parliament.number)} Parliament`} />
	<SubTitle
		text={`${GOVERNMENT_TYPE[parliament.government_type]} Government, ${parliament.start_date.year}-${parliament.end_date ? parliament.end_date.year : ''}`}
	/>

	<Heading text="Statistics" />
	<div class="flex flex-row space-x-3 sm:space-x-6 mb-2 overflow-x-scroll">
		<SmallStat name="Sessions" value={formatNumber(parliament.sessions)} />
		<SmallStat name="Throne Speeches" value={formatNumber(parliament.throne_speeches)} />
		<SmallStat name="Budgets/ESs" value={formatNumber(parliament.budgets)} />
		<SmallStat name="Senate Appts." value={formatNumber(parliament.senate_nominations)} />
	</div>

	<div class="flex flex-col sm:flex-row sm:space-x-6 w-full">
		<div class="flex flex-col sm:w-1/2">
			<Heading text="Government Parties" />
			<PartySquareListTile data={govParties} />
		</div>
		<div class="flex flex-col sm:w-1/2">
			<Heading text="Prime Ministers" />
			<PartySquareListTile data={primeMinisters} />
		</div>
	</div>

	<div class="flex flex-col sm:flex-row sm:space-x-6 w-full">
		<div class="flex flex-col sm:w-1/2">
			<Heading text="Opposition Parties" />
			<PartySquareListTile data={oppoParties} />
		</div>
		<div class="flex flex-col sm:w-1/2">
			<Heading text="Opposition Leaders" />
			<PartySquareListTile data={oppoLeaders} />
		</div>
	</div>

	<Heading text="General Election" />
	<List data={generalElectionListData} emptyText="" hideSubtitleForSm={true} />

	<Heading text="Byelections" />
	<List data={byelectionListData} emptyText="" hideSubtitleForSm={true} />
</Page>
