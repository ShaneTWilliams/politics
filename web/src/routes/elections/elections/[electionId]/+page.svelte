<script>
    import Page from '$lib/components/Page.svelte';

    import { page } from '$app/stores';

    import elections from '$lib/artifacts/election.json';
    import ridings from '$lib/artifacts/riding.json';
    import runs from '$lib/artifacts/run.json';
    import parties from '$lib/artifacts/party.json';
    import candidates from '$lib/artifacts/candidate.json';

    import { MONTHS, PARTIES, FILL_COLORS } from '$lib/constants.js';
	import CanadaMap from '$lib/components/CanadaMap.svelte';

    const ELECTION_TYPE = {
        "GENERAL": "General Election",
        "BYELECTION": "By-Election",
    }

    const SEAT_BAR_OFFSET = 3;
    const VOTE_BAR_OFFSET = 10;

    let election = elections[$page.params.electionId];
    let selectedRiding = null;

    let relevant_runs = [];
    let max_votes = 0;
    $: if (selectedRiding !== null) {
        relevant_runs = [];
        max_votes = 0;
        for (const run_id of election.runs) {
            let run = runs[run_id];
            if (run.riding == selectedRiding) {
                relevant_runs.push(run);
                if (run.votes > max_votes) {
                    max_votes = run.votes;
                }
            }
        }
    }

    let hoveredParty = null;
    let party_results = {};
    let max_seats = 0;
    for (const run_id of election.runs) {
        let run = runs[run_id];
        if (run.result === "ELECTED" || run.result === "ACCLAIMED") {
            if (party_results[run.party] === undefined) {
                party_results[run.party] = {
                    count: 0,
                    color: parties[run.party].color,
                };
            }
            party_results[run.party].count += 1;
            if (party_results[run.party].count > max_seats) {
                max_seats = party_results[run.party].count;
            }
        }
    }
    let party_results_sorted = Object.entries(party_results).sort((a, b) => b[1].count - a[1].count);
</script>

<svelte:head>
    <title>{election.date.year} {ELECTION_TYPE[election.type]}</title>
</svelte:head>

<Page>
    <div class="my-8 ml-8">
        <p class="font-bold text-4xl text-sol-dark3">
            {election.type == "GENERAL" ? "General Election" : "By-Election"}
        </p>
        <p class="text-xl text-sol-dark1 font-semibold">
            {MONTHS[election.date.month]} {election.date.day}, {election.date.year}
        </p>
    </div>
    <div class="space-y-2 flex flex-col items-end">
        <div class="flex flex-row space-x-4 w-full">
            <div class="space-y-1">
                {#each party_results_sorted as [party_id, result]}
                <p class="flex-none text-right text-sm h-5">
                    {PARTIES[parties[party_id].name]}
                </p>
                {/each}
            </div>
            <div class="grow space-y-1">
                {#each party_results_sorted as [party_id, result]}
                <div class="border border-sol-light2 rounded h-5">
                    <div
                        class={`h-full rounded hover:opacity-80 ${FILL_COLORS[result.color]}`}
                        style={`width: ${(result.count + SEAT_BAR_OFFSET) * 100 / (max_seats + SEAT_BAR_OFFSET)}%`}
                        on:mouseenter={() => hoveredParty = party_id}
                        on:mouseleave={() => hoveredParty = null}
                        role="none"
                    />
                </div>
                {/each}
            </div>
            <div class="space-y-1">
                {#each party_results_sorted as [party_id, result]}
                <p class="w-4 flex-none text-sm">
                    {result.count}
                </p>
                {/each}
            </div>
        </div>
        <p>
            {max_seats} seats total
        </p>
    </div>
    <CanadaMap bind:selectedRiding={selectedRiding} electionId={$page.params.electionId} {hoveredParty}/>
    {#if selectedRiding !== null}
    <div class="mt-6 mb-2 flex flex-col items-center bg-sol-light2 p-2 rounded">
        <p class="mb-4 font-black">
            {ridings[selectedRiding].name}, {ridings[selectedRiding].province}
        </p>
        <div class="flex flex-row space-x-4 w-full">
            <div class="space-y-1">
            {#each relevant_runs as run}
                <p class="text-sm font-black text-right">
                    {candidates[run.candidate].first_name} {candidates[run.candidate].last_name}
                </p>
            {/each}
            </div>
            <div class="space-y-1">
            {#each relevant_runs as run}
                <p class="text-sm text-left">
                    {PARTIES[parties[run.party].name]}
                </p>
            {/each}
            </div>
            <div class="grow space-y-1">
            {#each relevant_runs as run}
                <div class="border border-sol-light2 rounded h-5">
                    <div
                        class={`h-full rounded hover:opacity-80 ${FILL_COLORS[parties[run.party].color]}`}
                        style={`width: ${run.votes * 100 / max_votes}%`}
                    />
                </div>
            {/each}
            </div>
            <div class="space-y-1">
            {#each relevant_runs as run}
                <p class="text-sm space-y-1">
                    {relevant_runs.length == 1 ? "Acclaimed" : run.votes}
                </p>
            {/each}
            </div>
        </div>
    </div>
    {/if}
</Page>
