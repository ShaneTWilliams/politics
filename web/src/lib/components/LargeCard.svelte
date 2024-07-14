<script>
    import { formatString } from '$lib/utils.js';

    export let title, subtitle = null;
</script>

<div>
    <div class="flex flex-row">
        <div class="flex flex-row rounded-t-lg bg-sol-light3 mb-2 ml-4 text-sm">
            <p class="font-black text-lg mr-3">
                {title}
            </p>
            {#if subtitle}
            <p class="font-light text-lg text-sol-light0 italic">
                &mdash; {formatString(subtitle)}
            </p>
            {/if}
        </div>
    </div>
    <div class="flex flex-col p-3 bg-sol-light2 rounded-lg">
        <slot/>
    </div>
</div>
