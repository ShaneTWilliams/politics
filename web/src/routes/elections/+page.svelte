<script>
    import Page from '$lib/components/Page.svelte';
    import Card from '$lib/components/Card.svelte';
</script>

<svelte:head>
    <title>Federal Elections</title>
</svelte:head>

<Page>
    <div class="flex flex-col items-center w-full">
        <div class="flex flex-row w-full">
            <Card title="Parliaments" subtitle="Canada's 44 parliaments, summarized" link={"/"} />
            <Card title="Elections" subtitle="All of Canada's general and by-elections" link={"/elections/elections"} />
        </div>
        <div class="flex flex-row w-full">
            <Card title="Ridings" subtitle="Every electoral district in our history" link={"/"} />
            <Card title="Candidates" subtitle="Every election candidate since 1867" link={"/"} />
        </div>
    </div>
</Page>
