<script>
    import Page from '$lib/components/Page.svelte';
    import Map from '$lib/components/Map.svelte';
    import Election2021 from '$lib/components/icons/Election2021.svelte';

    import elections from '$lib/artifacts/election.json';

    const latestGeneralElectionId = Object.keys(elections).filter(
        electionId => elections[electionId].type === 'GENERAL'
    ).sort(
        (a, b) => elections[b].date - elections[a].date
    )[0];
</script>

<svelte:head>
    <title>Shane Williams</title>
</svelte:head>

<Page>
    <div class="mt-6 p-6 bg-sol-light2 dark:bg-sol-dark2 rounded-xl flex flex-col items-left">
        <div class="w-full flex flex-row justify-center">
            <div class="w-[600px]">
                <Election2021 />
            </div>
        </div>
        <div class="flex flex-col sm:ml-4 mt-4">
            <div class="text-left text-xl sm:text-2xl font-bold">
                Elections Data
            </div>
            <a
                href="/elections"
                class="sm:text-lg text-sm font-bold flex flex-row items-center justify-center border border-sol-dark2 dark:border-sol-light2 w-min px-3 py-2 sm:px-4 sm:py-2 border-2 rounded-lg sm:rounded-xl mt-3 hover:bg-sol-dark2 dark:hover:bg-sol-light2 hover:text-sol-light3 dark:hover:text-sol-dark3"
            >
                <p>
                    Explore
                </p>
            </a>
        </div>
    </div>
</Page>
