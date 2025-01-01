<script>
	import Page from '$lib/components/Page.svelte';
	import Election2021 from '$lib/components/icons/Election2021.svelte';
	import HomeCard from '$lib/components/HomeCard.svelte';

	import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

	const latestGeneralElectionId = Object.keys(elections)
		.filter((electionId) => elections[electionId].type === 'GENERAL')
		.sort((a, b) => elections[b].date - elections[a].date)[0];
</script>

<svelte:head>
	<title>Shane Williams</title>
</svelte:head>

<Page>
	<div class="flex flex-col">
		<HomeCard title="Elections Data" buttonText="Explore" link="/elections" >
			<div class="w-full max-w-[600px]">
				<Election2021 />
			</div>
		</HomeCard>
	</div>
</Page>
