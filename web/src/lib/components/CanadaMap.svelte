<script>
    import Map from "./Map.svelte"

    import candidates from "$lib/artifacts/candidate.json"
    import ridings from "$lib/artifacts/riding.json"
    import parties from "$lib/artifacts/party.json"
    import elections from "$lib/artifacts/election.json"
    import runs from "$lib/artifacts/run.json"

    import { PARTIES, PROVINCES } from "$lib/constants.js"
    import HorizontalBar from "./HorizontalBar.svelte"
    import { formatString } from "$lib/utils.js"

    export let electionId;
    let election = elections[electionId];

    let hoveredRiding = null;
    let selectedRiding = null;
    let detail_view_ids = [
        [
            "ST_JOHNS",
            "PEI",
            "MONCTON",
            "HALIFAX",
            "QUEBEC_CITY",
            "LONDON",
        ], [
            "MONTREAL",
            "SOUTHERN_QUEBEC",
            "TORONTO",
            "GOLDEN_HORSESHOE",
        ], [
            "OTTAWA",
            "CALGARY",
            "EDMONTON",
            "VANCOUVER",
        ], [
            "TROIS_RIVIERES",
            "REGINA",
            "WINNIPEG",
            "ESSEX",
            "SASKATOON",
            "VICTORIA",
        ]
    ];

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
</script>

<div>
    <div class="flex flex-col space-y-2 mb-4">
        {#each detail_view_ids.slice(0, 2) as row}
        <div class="flex flex-row space-x-2">
            {#each row as viewId}
                <Map
                    bind:selectedRiding={selectedRiding}
                    bind:hoveredRiding={hoveredRiding}
                    {electionId}
                    detail={true}
                    {viewId}
                />
            {/each}
        </div>
        {/each}
    </div>

    <Map
        bind:selectedRiding={selectedRiding}
        bind:hoveredRiding={hoveredRiding}
        {electionId}
        detail={false}
        viewId={null}
    />

    <div class="flex flex-col space-y-2">
        {#each detail_view_ids.slice(2) as row}
        <div class="flex flex-row space-x-2">
            {#each row as viewId}
                <Map
                bind:selectedRiding={selectedRiding}
                bind:hoveredRiding={hoveredRiding}
                {electionId}
                detail={true}
                {viewId}
                />
            {/each}
        </div>
        {/each}
    </div>

    {#if selectedRiding}
    <div class="py-4 sticky bottom-0">
        <div class="flex flex-col items-center bg-sol-light2 p-2 rounded-lg w-full shadow-md">
            <p class="mb-4 font-black">
                {formatString(ridings[selectedRiding].name)}, {PROVINCES[ridings[selectedRiding].province]}
            </p>
            <HorizontalBar
                primaryLabels={relevant_runs.map(run => candidates[run.candidate].first_name + ' ' + candidates[run.candidate].last_name)}
                secondaryLabels={relevant_runs.map(run => PARTIES[parties[run.party].name])}
                counts={relevant_runs.map(run => run.result == "ACCLAIMED" ? "Acclaimed" : run.votes)}
                colors={relevant_runs.map(run => parties[run.party].color)}
                showTotal={relevant_runs.length > 1}
            />
        </div>
    </div>
    {:else}
    <div class="">
        <p class="text-center text-sm italic text-sol-light1 mt-16">
            Select a riding to view regional statistics
        </p>
    </div>
    {/if}
</div>
