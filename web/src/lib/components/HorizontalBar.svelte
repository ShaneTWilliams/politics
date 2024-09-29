<script>
    import { FILL_COLOURS } from "$lib/constants.js";
    import { formatNumber } from "$lib/utils.js";

    export let primaryLabels, secondaryLabels, counts, colors, showTotal, minimumPercent = 0, primaryLinks = null, secondaryLinks=null;

    let max_seats, total_seats;
    $: {
        total_seats = 0;
        max_seats = 0;
        for (const count of counts) {
            if (typeof count === "number") {
                total_seats += count;
                if (count > max_seats) {
                    max_seats = count;
                }
            } else {
                max_seats = 0;
                total_seats = undefined;
                break;
            }
        }
    }
</script>

<div class="flex flex-col items-end w-full">
    <div class="flex flex-row space-x-4 w-full overflow-hidden text-nowrap">
        <div class="space-y-1 flex flex-col">
            {#each primaryLabels as label, i}
                {#if primaryLinks && primaryLinks[i]}
                <div class="flex flex-row justify-end">
                    <a href={primaryLinks[i]} class="flex-none text-right text-sm h-5 hover:underline decoration-dashed">
                        {label}
                    </a>
                </div>
                {:else}
                <p class="flex-none text-right text-sm h-5">
                    {label}
                </p>
                {/if}
            {/each}
        </div>
        {#if secondaryLabels.length > 0}
        <div class="space-y-1 flex flex-col">
            {#each secondaryLabels as label, i}
            {#if secondaryLinks && secondaryLinks[i]}
            <div class="flex flex-row justify-end">
                <a href={secondaryLinks[i]} class="flex-none text-right font-bold text-sm h-5 hover:underline decoration-dashed">
                    {label}
                </a>
            </div>
            {:else}
            <p class="flex-none text-right font-bold text-sm h-5">
                {label}
            </p>
            {/if}
            {/each}
        </div>
        {/if}
        <div class="grow space-y-1">
            {#each counts as count, i}
            <div class="rounded h-5 border border-sol-light2 dark:border-sol-dark2 border-2">
                <div
                    class={`h-full rounded hover:opacity-80 ${FILL_COLOURS[colors[i]]}`}
                    style={`width: ${Math.max(count * 100 / max_seats, minimumPercent)}%`}
                    role="none"
                />
            </div>
            {/each}
        </div>
        <div class="space-y-1">
            {#each counts as count}
            <p class="flex-none text-sm text-right">
                { formatNumber(count) }
            </p>
            {/each}
            {#if showTotal && total_seats != undefined}
            <p class="text-sm font-black border-t border-sol-light1 dark:border-sol-dark1 pt-1 leading-none">
                { formatNumber(total_seats) }
            </p>
            {/if}
        </div>
    </div>
</div>
