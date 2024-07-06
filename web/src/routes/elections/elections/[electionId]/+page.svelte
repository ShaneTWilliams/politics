<script>
    import Map from '$lib/components/Map.svelte';
    import Page from '$lib/components/Page.svelte';

    let selectedRiding = null;
</script>

<Page>
    <Map bind:selectedRiding={selectedRiding}/>
</Page>
