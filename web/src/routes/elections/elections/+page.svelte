<script>
    import Page from '$lib/components/Page.svelte';

    import ridings from '$lib/artifacts/riding.json';
    import runs from '$lib/artifacts/run.json';
    import candidates from '$lib/artifacts/candidate.json';
    import parties from '$lib/artifacts/party.json';
    import elections from '$lib/artifacts/election.json';
	import { onMount } from 'svelte';
    import { MONTHS } from '$lib/constants.js';

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
</script>

<svelte:head>
    <title>Elections List</title>
</svelte:head>

<Page>
    <p class="mt-6 mb-2 font-bold text-2xl text-sol-dark3">Federal Elections</p>
    <div class="flex flex-row mb-6">
        <input type="checkbox" id="check" bind:checked={checked}/>
        <label for="check" class="ml-2 font-light text-sol-dark3 text-sm grow select-none">Show by-elections</label>
        <button class="flex flex-row hover:cursor-pointer" on:click={() => {sort_ascending = !sort_ascending;}}>
            <p class="font-black text-sol-dark3 text-sm mr-2">Sort dates:</p>
            <p class="font-light text-sol-dark3 text-sm">{sort_ascending ? "Ascending" : "Descending"}</p>
        </button>
    </div>
    {#if sortedElections !== undefined}
    <div class="space-y-2">
        {#each (sort_ascending ? sortedElections : sortedElections.toReversed()) as [electionId, election]}
            {#if checked || election.type === "GENERAL"}
            <a
            class={`flex flex-row items-center rounded px-4 py-1 w-full hover:cursor-pointer hover:bg-sol-light2 border-sol-light1 border ${election.type === "GENERAL" ? "bg-sol-light2" : ""}`}
            href={`/elections/elections/${electionId}`}
            >
                <p class="font-semibold mr-4 text-sm text-sol-dark3">
                    {election.date.year}
                </p>
                <p class="font-light grow text-xs text-sol-dark3">
                    {MONTHS[election.date.month]} {election.date.day}
                </p>
                <p class="font-bold text-xs text-sol-dark3">
                    {ELECTION_TYPE_DISPLAY[election.type]}
                </p>
            </a>
            {/if}
        {/each}
    </div>
    {/if}
</Page>
