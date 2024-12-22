<script>
    import { FILL_COLOURS } from "$lib/constants.js";
    import { formatNumber } from "$lib/utils.js";

    export let data, showTotal, minimumPercent = 0;

    let max_seats, total_seats;
    $: {
        total_seats = 0;
        max_seats = 0;

        if (data)
        {
            for (const row of data) {
                if (typeof row.count === "number") {
                    total_seats += row.count;
                    if (row.count > max_seats) {
                        max_seats = row.count;
                    }
                } else {
                    max_seats = 0;
                    total_seats = undefined;
                    break;
                }
            }
        }
    }
</script>

<div class="flex flex-col items-start sm:items-end w-full lg:text-sm text-xs text-nowrap">
    {#if data}
    <table class="table-auto border-separate border-spacing-x-4 w-full">
    {#each data as row}
    <tr class="">
        <td class="space-y-1 flex-col flex text-left">
            {#if row.primaryLink}
            <div class="flex flex-row">
                <a href={row.primaryLink} class="flex-none h-5 hover:underline decoration-dashed">
                    {row.primaryLabel}
                </a>
            </div>
            {:else}
            <p class="h-5">
                {row.primaryLabel}
            </p>
            {/if}
        </td>
        {#if row.secondaryLabel}
        <td class="">
            {#if row.secondaryLink}
            <a href={row.secondaryLink} class="flex-none text-left font-bold h-5 hover:underline decoration-dashed hidden sm:block">
                {row.secondaryLabel}
            </a>
            {:else}
            <p class="flex-none font-bold h-5">
                {row.secondaryLabel}
            </p>
            {/if}
        </td>
        {/if}
        <td class="rounded h-5 border border-sol-light2 dark:border-sol-dark2 border-2 w-full hidden sm:table-cell">
            <div
                class={`h-full rounded hover:opacity-80 ${FILL_COLOURS[row.color]}`}
                style={`width: ${Math.max(row.count * 100 / max_seats, minimumPercent)}%`}
                role="none"
            />
        </td>
        <td class="flex-none text-right">
            { formatNumber(row.count) }
        </td>
    </tr>
    {/each}
    {#if showTotal && total_seats != undefined}
    <tr>
        <td />
        {#if data.some((row) => row.secondaryLink)}
        <td class="hidden sm:table-cell"/>
        {/if}
        <td class="w-full hidden sm:table-cell"/>
        <td class="font-black border-t border-sol-light1 dark:border-sol-dark1 pt-1 leading-none text-right">
            { formatNumber(total_seats) }
        </td>
    </tr>
    {/if}
    </table>
    {/if}
</div>
