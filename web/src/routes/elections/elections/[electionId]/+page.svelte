<script>
    import Map from '$lib/components/Map.svelte';
    import Page from '$lib/components/Page.svelte';

    import { page } from '$app/stores';

    import elections from '$lib/artifacts/election.json';

    let election = elections[$page.params.electionId];
    let selectedRiding = null;
</script>

<Page>
    {election.date.year}-{election.date.month}-{election.date.day} Election
    <Map bind:selectedRiding={selectedRiding} electionId={$page.params.electionId}/>
</Page>
