<script>
	import LucideInfo from '~icons/lucide/info';

	import Page from '$lib/components/Page.svelte';
	import Card from '$lib/components/Card.svelte';

	import Ballot from '$lib/components/icons/Ballot.svelte';
	import Sign from '$lib/components/icons/Sign.svelte';
	import Silhouette from '$lib/components/icons/Silhouette.svelte';
	import SeatingChart from '$lib/components/icons/SeatingChart.svelte';
	import Labrador from '$lib/components/icons/Labrador.svelte';
</script>

<svelte:head>
	<title>Federal Elections Visualizer</title>
</svelte:head>

<Page>
	<div class="flex flex-col items-center">
		<div class="flex flex-col items-center w-full mt-4 max-w-3xl space-y-4">
			<a
				href="/blog"
				class="flex flex-row items-center w-full rounded-lg bg-sol-light3 dark:bg-sol-dark3 border-sol-light2 dark:border-sol-dark2 border-2 hover:bg-sol-light2 hover:dark:bg-sol-dark2 py-2 px-4 flex flex-row text-sol-dark3 font-bold dark:text-sol-light1 mt-2 text-xs sm:text-sm"
			>
				<LucideInfo class="mr-2 flex-none" />
				<p>Click here to read the accompanying blog post!</p>
			</a>
			<div class="flex flex-col sm:flex-row w-full space-y-4 sm:space-y-0 sm:space-x-4">
				<Card
					title="Elections"
					subtitle="All of Canada's general and by-elections"
					link={'/elections/elections'}
				>
					<Ballot />
				</Card>
				<Card
					title="Candidates"
					subtitle="Every election candidate since 1867"
					link={'/elections/candidates'}
				>
					<Silhouette />
				</Card>
			</div>
			<div class="flex flex-col sm:flex-row w-full space-y-4 sm:space-y-0 sm:space-x-4">
				<Card
					title="Ridings"
					subtitle="Every federal electoral district in Canada's history"
					link={'/elections/ridings'}
				>
					<Labrador />
				</Card>
				<Card
					title="Parties"
					subtitle="Declared Canadian political parties"
					link={'/elections/parties'}
				>
					<Sign />
				</Card>
			</div>
			<div class="flex flex-row w-full">
				<Card
					title="Parliaments"
					subtitle="Canada's 44 parliaments summarized"
					link={'/elections/parliaments'}
				>
					<SeatingChart />
				</Card>
			</div>
		</div>
	</div>
</Page>
