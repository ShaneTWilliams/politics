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
    import { browser } from '$app/environment';

    export let electionId, focusParty=null;
    $: election = elections[electionId];

    $: hoveredRiding = null;
    $: selectedRiding = null;
    let BIG_DETAIL_VIEW_IDS = [
        [
            "MONTREAL",
            "SOUTHERN_QUEBEC",
            "TORONTO",
            "GOLDEN_HORSESHOE",
        ], [
            "OTTAWA",
            "CALGARY",
            "EDMONTON",
            "VANCOUVER",
        ]
    ];
    let SMALL_DETAIL_VIEW_IDS = [
        [
            "ST_JOHNS",
            "PEI",
            "MONCTON",
            "HALIFAX",
            "QUEBEC_CITY",
            "LONDON",
        ], [
            "TROIS_RIVIERES",
            "REGINA",
            "WINNIPEG",
            "ESSEX",
            "SASKATOON",
            "VICTORIA",
        ]
    ];

    $: relevant_runs = [];
    $: max_votes = 0;
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
    $: relevantRunsBarData = relevant_runs.map(
        (run) => {
            return {
                primaryLabel: candidates[run.candidate].first_name + ' ' + candidates[run.candidate].last_name,
                primaryLink: `/elections/candidates/${run.candidate}`,
                secondaryLabel: PARTIES[parties[run.party].name],
                secondaryLink: `/elections/parties/${run.party}`,
                count: run.result == "ACCLAIMED" ? "Acclaimed" : run.votes,
                color: parties[run.party].color,
            };
        }
    );

    // Determine if we're stuck to the bottom of the screen.
    let stickyElement, stuck;
    $: if (browser && stickyElement) {
        const observer = new IntersectionObserver(
            ([e]) => stuck = e.intersectionRatio < 1,
            {threshold: [1]}
        );
        observer.observe(stickyElement)
    }
</script>

<div class="w-full">
    <Map
        bind:selectedRiding={selectedRiding}
        bind:hoveredRiding={hoveredRiding}
        {electionId}
        detail={false}
        viewId={null}
        clickable={true}
        {focusParty}
    />

    {#if election.type == "GENERAL"}
    <div class="flex flex-col space-y-2 mb-4 px-2 overflow-none">
        {#each BIG_DETAIL_VIEW_IDS as row}
        <div class="flex flex-row space-x-2">
            {#each row as viewId}
                <Map
                    bind:selectedRiding={selectedRiding}
                    bind:hoveredRiding={hoveredRiding}
                    {electionId}
                    detail={true}
                    {viewId}
                    clickable={true}
                    {focusParty}
                />
            {/each}
        </div>
        {/each}
    </div>
    <div class="flex flex-col space-y-2 px-2">
        {#each SMALL_DETAIL_VIEW_IDS as row}
        <div class="flex flex-row space-x-2 w-full">
            {#each row as viewId}
                <Map
                    bind:selectedRiding={selectedRiding}
                    bind:hoveredRiding={hoveredRiding}
                    {electionId}
                    detail={true}
                    {viewId}
                    clickable={true}
                    {focusParty}
                />
            {/each}
        </div>
        {/each}
    </div>
    {/if}

    {#if selectedRiding}
    <div class="pb-4 mt-8 sticky -bottom-[1px]" bind:this={stickyElement}>
        <div class={`flex flex-col items-center bg-sol-light2 dark:bg-sol-dark2 p-2 rounded-lg w-full ${stuck ? "shadow-[rgba(0,0,0,0.1)_0px_0px_25px_5px]" : ""}`}>
            <a class="mb-4 font-black hover:underline decoration-dashed" href={`/elections/ridings/${selectedRiding}`}>
                {formatString(ridings[selectedRiding].name)}, {PROVINCES[ridings[selectedRiding].province]}
            </a>
            <HorizontalBar data={relevantRunsBarData} showTotal={relevant_runs.length > 1} />
        </div>
    </div>
    {:else}
    <div class="">
        <p class="text-center text-sm italic text-sol-light1 dark:text-sol-dark1 mt-16">
            Select a riding to view regional statistics
        </p>
    </div>
    {/if}
</div>
