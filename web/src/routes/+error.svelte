<script>
	import Page from '$lib/components/Page.svelte';
    import Button from '$lib/components/Button.svelte';
</script>

<svelte:head>
	<title>Error 404</title>
</svelte:head>

<Page>
    <div class="flex flex-col w-full items-center mt-12 space-y-6">
        <p class="text-9xl text-right">404</p>
        <p class="text-md">The requested page doesn't exist!</p>
        <Button link="/" text="Go home" />
    </div>
</Page>
