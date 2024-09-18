<script>
    import ArrowUp from '~icons/mdi/arrow-up'
    import ArrowDown from '~icons/mdi/arrow-down'

    import Page from '$lib/components/Page.svelte';

    import elections from '$lib/artifacts/election.json';
    import parties from '$lib/artifacts/party.json';

    import { MONTHS, FILL_COLOURS } from '$lib/constants.js';

    import { getTopNSeatCounts } from '$lib/stats.js';

    const ELECTION_TYPE_DISPLAY = {
        "GENERAL": "General Election",
        "BYELECTION": "By-Election",
    };

    let checked = false;
    let sort_ascending = false;

    $: sortedElections = Object.entries(elections).sort((a, b) => {
        if (a[1].date.year === b[1].date.year) {
            if (a[1].date.month === b[1].date.month) {
                return a[1].date.day - b[1].date.day;
            }
            return a[1].date.month - b[1].date.month;
        }
        return a[1].date.year - b[1].date.year;
    });

    let electionResults = {};
    for (const [electionId, election] of Object.entries(elections)) {
        if (election.type === "GENERAL") {
            electionResults[electionId] = {
                counts: getTopNSeatCounts(electionId, 3),
                maxCount: Math.max(...Object.values(getTopNSeatCounts(electionId, 3)).map(([_, count]) => count)),
            };
        }
    }
</script>

<svelte:head>
    <title>Elections List</title>
</svelte:head>

<Page>
    <p class="mt-6 mb-2 font-bold text-2xl text-sol-dark3">Federal Elections</p>
    {#if sortedElections !== undefined}
    <div class="flex flex-col items-center">
        <div class="flex flex-row w-full border-sol-light2 py-3">
            <button class="flex flex-row items-center hover:cursor-pointer" on:click={() => {sort_ascending = !sort_ascending;}}>
                <p class="font-black text-sol-dark3 text-sm mr-2">Sort dates:</p>
                <p class="font-bold text-sol-dark3 text-sm">
                {#if sort_ascending}
                    <ArrowUp />
                {:else}
                    <ArrowDown />
                {/if}
                <p/>
            </button>
            <div class="grow" />
            <div class="flex flex-row">
                <input type="checkbox" id="check" bind:checked={checked}/>
                <label for="check" class="ml-2 font-light text-sol-dark3 text-sm grow select-none">Show by-elections</label>
            </div>
        </div>
        {#each (sort_ascending ? sortedElections : sortedElections.toReversed()) as [electionId, election]}
            {#if checked || election.type === "GENERAL"}
            <a
                class="flex flex-row items-center hover:cursor-pointer hover:bg-sol-light2 border-sol-light2 py-3 border-t px-4 w-full"
                href={`/elections/elections/${electionId}`}
            >
                <p class="font-semibold mr-6 text-sm text-sol-dark3">
                    {election.date.year}
                </p>
                <p class="font-light grow text-xs text-sol-dark3">
                    {MONTHS[election.date.month]} {election.date.day}
                </p>
                {#if election.type == "GENERAL"}
                <div class="flex flex-row mr-8">
                    {#each electionResults[electionId].counts as [party, seats]}
                    <div class="px-[1px] h-5 w-3 flex flex-col justify-end">
                        <div
                            class={`${FILL_COLOURS[parties[party].color]}`}
                            style={`height: ${seats * 100 / electionResults[electionId].maxCount}%`}
                        />
                    </div>
                    {/each}
                </div>
                {/if}
                <p class="font-bold text-xs text-sol-dark3">
                    {ELECTION_TYPE_DISPLAY[election.type]}
                </p>
            </a>
            {/if}
        {/each}
    </div>
    {/if}
</Page>
