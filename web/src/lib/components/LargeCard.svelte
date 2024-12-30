<script>
    import { formatString } from '$lib/utils.js';

    export let title, subtitle = null;
</script>

<div class="flex flex-col">
    <div class="flex flex-row">
        <div class="flex flex-col rounded-t-lg bg-sol-light3 dark:bg-sol-dark3 mb-1 ml-1">
            <p class="font-black text-md mr-3">
                {title}
            </p>
            {#if subtitle}
            <p class="font-light text-sm text-sol-light0">
                {formatString(subtitle)}
            </p>
            {/if}
        </div>
    </div>
    <div class="flex flex-col py-2 sm:py-3 sm:px-2 bg-sol-light2 dark:bg-sol-dark2 rounded-lg">
        <slot/>
    </div>
</div>
