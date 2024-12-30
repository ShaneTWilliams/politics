<script>
    import Page from '$lib/components/Page.svelte';

    import headshot from '$lib/static/edited.jpg'
</script>

<svelte:head>
    <title>About Shane Williams</title>
</svelte:head>

<Page>
    <div class="flex flex-row mt-8 space-x-8 px-8">
        <div class="flex flex-col grow">
            <p class="font-bold text-3xl mb-4">
                About Me
            </p>
            <p>
                I'm a firmware developer from St. John's, Newfoundland.
            </p>
        </div>
        <img src={headshot} alt="" class="w-72 h-72 rounded-2xl" />
    </div>
</Page>
