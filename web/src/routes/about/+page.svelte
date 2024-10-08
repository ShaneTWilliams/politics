<script>
    import Page from '$lib/components/Page.svelte';
    import headshot from '$lib/static/moreblur.jpg'
</script>

<svelte:head>
    <title>About Shane Williams</title>
</svelte:head>

<Page>
    About Me
    <img src={headshot} alt="" class="w-48 h-48 rounded-2xl headshot" />
</Page>
