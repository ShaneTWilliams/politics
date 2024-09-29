<script>
    import Page from '$lib/components/Page.svelte';
    import Map from '$lib/components/Map.svelte';
    import Card from '../lib/components/Card.svelte';

    import elections from '$lib/artifacts/election.json';

    const latestGeneralElectionId = Object.keys(elections).filter(
        electionId => elections[electionId].type === 'GENERAL'
    ).sort(
        (a, b) => elections[b].date - elections[a].date
    )[0];
</script>

<Page>
    <div class="mt-6 p-6 bg-sol-light2 dark:bg-sol-dark2 rounded-xl flex flex-col items-left">
        <div class="w-full flex flex-row justify-center">
            <div class="w-[600px]">
                <Map
                electionId={latestGeneralElectionId}
                detail={false}
                viewId={null}
                clickable={false}
                />
            </div>
        </div>
        <div class="text-left ml-6 text-2xl font-bold">
            Elections Data
        </div>
        <a href="/elections" class="ml-6 text-lg font-bold flex flex-row items-center justify-center border border-sol-dark2 dark:border-sol-light2 w-min px-6 py-3 border-2 rounded-2xl mt-3 hover:bg-sol-dark2 dark:hover:bg-sol-light2 hover:text-sol-light3 dark:hover:text-sol-dark3">
            <p>
                Explore
            </p>
        </a>
    </div>
</Page>
