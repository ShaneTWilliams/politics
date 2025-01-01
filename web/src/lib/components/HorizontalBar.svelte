<script>
	import { FILL_COLOURS } from '$lib/constants.js';
	import { formatNumber } from '$lib/utils.js';

	export let data,
		showTotal,
		minimumPercent = 0,
		pct = false;

	let min_count, max_count, total_count;
	$: {
		total_count = 0;
		max_count = 0;
		min_count = 0;

		if (data) {
			for (const row of data) {
				if (typeof row.count === 'number') {
					total_count += row.count;
					if (row.count > max_count) {
						max_count = row.count;
					}
					if (row.count < min_count) {
						min_count = row.count;
					}
				} else {
					max_count = 0;
					min_count = 0;
					total_count = undefined;
					break;
				}
			}
		}
	}
</script>

<div class="flex flex-col items-start sm:items-end w-full text-xs overflow-y-scroll text-nowrap">
	{#if data}
		<table class="table-auto border-separate border-spacing-x-3 w-full min-w-0">
			{#each data as row}
				<tr>
					<td class="space-y-1 flex-col flex text-left truncate align-middle max-w-56 lg:max-w-max">
						{#if row.primaryLink}
							<a href={row.primaryLink} class="hover:underline decoration-dotted">
								<p class="truncate">
									{row.primaryLabel}
								</p>
							</a>
						{:else}
							<p class="">
								{row.primaryLabel}
							</p>
						{/if}
					</td>
					{#if row.secondaryLabel}
						<td class="hidden sm:table-cell">
							{#if row.secondaryLink}
								<a
									href={row.secondaryLink}
									class="text-left font-bold hover:underline decoration-dotted"
								>
									{row.secondaryLabel}
								</a>
							{:else}
								<p class="font-bold hidden sm:block">
									{row.secondaryLabel}
								</p>
							{/if}
						</td>
					{/if}
					{#if min_count < 0}
						<td
							class="rounded h-5 border border-sol-light2 dark:border-sol-dark2 border-2 hidden sm:table-cell w-full"
						>
							<div class="flex flex-row w-full h-full">
								<div
									class="h-full flex flex-row justify-end"
									style={`width: ${(min_count * 100) / (min_count - max_count)}%`}
								>
									{#if row.count < 0}
										<div
											class={`h-full rounded hover:opacity-80 ${FILL_COLOURS[row.color]}`}
											style={`width: ${(row.count / min_count) * 100}%`}
											role="none"
										/>
									{/if}
								</div>
								<div
									class="h-full flex flex-row"
									style={`width: ${(max_count * 100) / (max_count - min_count)}%`}
								>
									{#if row.count > 0}
										<div
											class={`h-full rounded hover:opacity-80 ${FILL_COLOURS[row.color]}`}
											style={`width: ${(row.count / max_count) * 100}%`}
											role="none"
										/>
									{/if}
								</div>
							</div>
						</td>
					{:else}
						<td
							class="rounded h-5 border border-sol-light2 dark:border-sol-dark2 border-2 w-full hidden sm:table-cell"
						>
							<div
								class={`h-full rounded hover:opacity-80 ${FILL_COLOURS[row.color]}`}
								style={`width: ${Math.max((row.count * 100) / max_count, minimumPercent)}%`}
								role="none"
							/>
						</td>
					{/if}
					<td class="flex-none text-right">
						{formatNumber(row.count, pct)}
					</td>
				</tr>
				<tr>
					{#if min_count < 0}
						<td colspan="3" class="rounded h-1 w-full sm:hidden">
							<div class="flex flex-row w-full h-full">
								<div
									class="h-full flex flex-row justify-end"
									style={`width: ${(min_count * 100) / (min_count - max_count)}%`}
								>
									{#if row.count < 0}
										<div
											class={`h-full rounded-l hover:opacity-80 ${FILL_COLOURS[row.color]}`}
											style={`width: ${(row.count / min_count) * 100}%`}
											role="none"
										/>
									{:else}
										<div class="h-full w-full rounded-l bg-sol-light1/50 dark:bg-sol-dark1/50" />
									{/if}
								</div>
								<div
									class="h-full flex flex-row"
									style={`width: ${(max_count * 100) / (max_count - min_count)}%`}
								>
									{#if row.count > 0}
										<div
											class={`h-full rounded-r hover:opacity-80 ${FILL_COLOURS[row.color]}`}
											style={`width: ${(row.count / max_count) * 100}%`}
											role="none"
										/>
									{:else}
										<div class="h-full w-full rounded-r bg-sol-light1/50 dark:bg-sol-dark1/50" />
									{/if}
								</div>
							</div>
						</td>
					{:else if (row.count * 100) / max_count > 5}
						<td colspan="3" class="rounded h-1 w-full sm:hidden">
							<div
								class={`h-full rounded hover:opacity-80 ${FILL_COLOURS[row.color]}`}
								style={`width: ${Math.max((row.count * 100) / max_count, minimumPercent)}%`}
								role="none"
							/>
						</td>
					{/if}
				</tr>
			{/each}
			{#if showTotal && total_count != undefined}
				<tr>
					<td />
					{#if data.some((row) => row.secondaryLink)}
						<td class="hidden sm:table-cell" />
					{/if}
					<td class="w-full hidden sm:table-cell" />
					<td
						class="font-black border-t border-sol-light1 dark:border-sol-dark1 pt-1 leading-none text-right"
					>
						{formatNumber(total_count)}
					</td>
				</tr>
			{/if}
		</table>
	{/if}
</div>
