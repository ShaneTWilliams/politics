<script>
    import { FILL_COLORS } from "$lib/constants.js";
    import { formatNumber } from "$lib/utils.js";

    export let primaryLabels, secondaryLabels, counts, colors, showTotal, minimumPercent = 0;

    $: max_seats = Math.max(...counts);
    $: total_seats = counts.reduce((a, b) => a + b, 0);
</script>

<div class="flex flex-col items-end w-full">
    <div class="flex flex-row space-x-2 w-full">
        <div class="space-y-1">
            {#each primaryLabels as label}
            <p class="flex-none text-right text-sm h-5">
                {label}
            </p>
            {/each}
        </div>
        <div class="space-y-1">
            {#each secondaryLabels as label}
            <p class="flex-none text-left font-bold text-sm h-5">
                {label}
            </p>
            {/each}
        </div>
        <div class="grow space-y-1">
            {#each counts as count, i}
            <div class="rounded h-5 border border-sol-light2 border-2">
                <div
                    class={`h-full rounded hover:opacity-80 ${FILL_COLORS[colors[i]]}`}
                    style={`width: ${Math.max(count * 100 / max_seats, minimumPercent)}%`}
                    role="none"
                />
            </div>
            {/each}
        </div>
        <div class="space-y-1">
            {#each counts as count}
            <p class="flex-none text-sm">
                { formatNumber(count) }
            </p>
            {/each}
        </div>
    </div>
    {#if showTotal}
    <p class="text-sm font-black border-t-2 border-sol-light1 pt-1 leading-none">
        { formatNumber(total_seats) }
    </p>
    {/if}
</div>
