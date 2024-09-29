<script>
    export let data, page, emptyText;

    $: start_index = page * 100;
    $: end_index = start_index + 100;
</script>

<div class="w-full text-sol-dark3 dark:text-sol-light3">
    <slot/>
    {#each data.slice(start_index, end_index) as item}
    <div class="border-t border-sol-light2 dark:border-sol-dark2" />
    <a
        class="rounded-lg flex flex-row items-center hover:cursor-pointer hover:bg-sol-light2 dark:hover:bg-sol-dark2 py-3 px-4 w-full"
        href={item.link}
    >
        <p class="font-semibold mr-6 text-sm">
            {item.title}
        </p>
        <p class="font-light grow text-xs">
            {item.subtitle}
        </p>
        <svelte:component this={item.element} {...item.elementProps} />
        <pre class="font-bold text-xs">{item.category}</pre>
    </a>
    {/each}
    {#if data.length === 0}
        <div class="text-center py-4 mt-8">
            <p>{emptyText}</p>
        </div>
    {/if}
</div>
