<script>
    import Page from '$lib/components/Page.svelte';
    import Card from '$lib/components/Card.svelte';
    import Labrador from '$lib/components/Labrador.svelte';

    import Ballot from '$static/Ballot.svelte';
    import Sign from '$static/Sign.svelte';
    import Silhouette from '$static/Silhouette.svelte';
    import Seating from '$static/SeatingChart.svelte';

    import LucideInfo from '~icons/lucide/info';
</script>

<svelte:head>
    <title>Federal Elections Visualizer</title>
</svelte:head>

<Page>
    <div class="flex flex-col items-center">
        <div class="flex flex-col items-center w-full mt-4 max-w-3xl space-y-4">
            <a href="/blog" class="flex flex-row items-center w-full rounded-lg bg-sol-light2 dark:bg-sol-dark2 py-2 px-4 flex flex-row text-sol-dark3 font-bold dark:text-sol-light3 text-sm mt-2">
                <LucideInfo class="text-lg mr-2" />
                <p>
                    Click here to read the accompanying blog post!
                </p>
            </a>
            <div class="flex flex-row w-full space-x-4">
                <Card title="Elections" subtitle="All of Canada's general and by-elections" link={"/elections/elections"} >
                    <Ballot />
                </Card>
                <Card title="Candidates" subtitle="Every election candidate since 1867" link={"/elections/candidates"} >
                    <Silhouette />
                </Card>
            </div>
            <div class="flex flex-row w-full space-x-4">
                <Card title="Ridings" subtitle="Every electoral district in our history" link={"/elections/ridings"} >
                    <Labrador />
                </Card>
                <Card title="Parties" subtitle="Registered political parties" link={"/elections/parties"} >
                    <Sign />
                </Card>
            </div>
            <div class="flex flex-row w-full">
                <Card title="Parliaments" subtitle="Canada's 44 parliaments, summarized" link={"/"} >
                    <div class="p-4 h-full">
                        <Seating />
                    </div>
                </Card>
            </div>
        </div>
    </div>
</Page>
