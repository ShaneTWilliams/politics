<script>
	import Page from '$lib/components/Page.svelte';
	import List from '$lib/components/List.svelte';
	import Title from '$lib/components/Title.svelte';
	import PartySquare from '$lib/components/PartySquare.svelte';

	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	import { PARTIES } from '$lib/constants.js';

	let searchBarContents = '';
	let onlyWinners = true;

	$: sortedParties = Object.entries(parties)
		.filter(([partyId, party]) => {
			let match = true;
			for (const token of searchBarContents.split(' ')) {
				if (!party.name.toLowerCase().includes(token.toLowerCase())) {
					match = false;
				}
			}
			return match;
		})
		.filter(([partyId, party]) => {
			return party.has_won_election || !onlyWinners;
		})
		.sort((a, b) => {
			if (a[1].name < b[1].name) {
				return -1;
			}
			if (a[1].name > b[1].name) {
				return 1;
			}
			return 0;
		});

	$: listData = sortedParties
		? sortedParties.map(([partyId, party]) => {
				return {
					link: `/elections/parties/${partyId}`,
					title: PARTIES[party.name],
					subtitle: '',
					category: '',
					element: PartySquare,
					elementProps: { partyId }
				};
			})
		: [];
</script>

<svelte:head>
	<title>Canadian Political Parties</title>
</svelte:head>

<Page>
	<Title text="Political Parties" />
	<List data={listData}>
		<div class="flex flex-row space-x-2 items-start px-5 py-3 w-full overflow-x-scroll">
			<input
				class="rounded-lg w-48 text-sm px-3 py-1 bg-sol-light2 dark:bg-sol-dark2"
				type="text"
				placeholder="Party Name"
				bind:value={searchBarContents}
			/>
			<div class="grow" />
			<div class="flex flex-row items-center">
				<input type="checkbox" id="check" bind:checked={onlyWinners} />
				<label for="check" class="ml-2 font-light text-sm grow select-none text-nowrap"
					>Show only parties that have won seats</label
				>
			</div>
		</div>
	</List>
</Page>
