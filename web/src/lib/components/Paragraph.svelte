<script>
    export let wikiLink, paragraphs;

    let summaryExpanded = false;
    let innerWidth;

    $: PREVIEW_PARAGRAPH_NUM = innerWidth > 450 ? 2 : 1;
</script>
<svelte:window bind:innerWidth />

<div class="text-justify text-sm text-sol-dark2 space-y-4">
    {#if paragraphs}
    {#each paragraphs as summaryParagraph, i}
        {#if summaryExpanded || i < PREVIEW_PARAGRAPH_NUM}
        <p class="text-sm text-justify	text-sol-dark2 whitespace-break-spaces dark:text-sol-light1">
            {#if i == 0}
            <a
                href={wikiLink}
                target="_blank"
                class="hover:font-bold underline decoration-dotted text-sol-dark3 dark:text-sol-light3"
            >Wikipedia</a>: {summaryParagraph}
            {:else}
                {summaryParagraph}
            {/if}
            {#if summaryExpanded && i == paragraphs.length - 1}
            <button
                on:click={() => {summaryExpanded = false}}
                class="hover:font-bold underline decoration-dotted text-sol-dark3 dark:text-sol-light3"
            >Hide</button>
            {:else if !summaryExpanded && i == PREVIEW_PARAGRAPH_NUM-1 && paragraphs.length > PREVIEW_PARAGRAPH_NUM}
            <button
                on:click={() => {summaryExpanded = true}}
                class="hover:font-bold underline decoration-dotted text-sol-dark3 dark:text-sol-light3"
            >Show more</button>
            {/if}
        </p>
        {/if}
    {/each}
    {/if}
</div>
