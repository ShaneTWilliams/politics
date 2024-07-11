<script>
	import { onMount } from "svelte";

    import ridings from "$lib/artifacts/riding.json"
    import runs from "$lib/artifacts/run.json"
    import parties from "$lib/artifacts/party.json"
    import elections from "$lib/artifacts/election.json"

    import { FILL_COLORS } from "$lib/constants.js"

    const RO_YEARS = [
        1867,
        1872,
        1882,
        1892,
        1903,
        1905,
        1914,
        1924,
        1933,
        1947,
        1952,
        1966,
        1976,
        1987,
        1996,
        1999,
        2003,
        2013
    ]

    export let selectedRiding, hoveredRiding, electionId, hoveredParty, view;

    let svgEl;
    let x = 0;
    let y = 0;
    let width = 0;
    let height = 0;

    function resizeSvg() {
        if (view === null) {
            const bbox = svgEl.getBBox();
            x = bbox.x;
            y = -(bbox.y + bbox.height);
            width = bbox.width;
            height = bbox.height;
        } else {
            x = view.x;
            y = -view.y;
            width = view.width;
            height = view.height;
        }
    }

    let ridingsToShow = {};
    let election = elections[electionId];

    let ro_year = RO_YEARS[0];
    for (const y of RO_YEARS) {
        if (election.date.year >= y) {
            ro_year = y;
        } else {
            break;
        }
    }
    for (const runId of election.runs) {
        let run = runs[runId];
        let riding = ridings[run.riding];
        if ((run.result === "ELECTED" || run.result === "ACCLAIMED")) {
            let color = parties[run.party].color;
            if (color === null) {
                console.log("No color for: " + parties[run.party].name)
            }
            ridingsToShow[run.riding] = {
                ...riding,
                color: color,
                victorParty: run.party,
            };
        }
    }

    onMount(() => {
        resizeSvg();

        window.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                selectedRiding = null;
            }
        });
    });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->

<svg
    xmlns='http://www.w3.org/2000/svg'
    viewBox={`${x} ${y} ${width} ${height}`}
    class="border"
>
    <g transform='scale(1,-1)' bind:this={svgEl}>
        {#each Object.entries(ridingsToShow) as [id, riding]}
        <g
            class={`
                stroke-sol-light3 ${FILL_COLORS[riding.color]}
                ${hoveredParty == riding.victorParty || hoveredRiding == id ? "opacity-70" : ""}
                ${selectedRiding == id ? "opacity-70" : ""}
            `}
            style={`stroke-width: ${Math.pow(Math.min(width, height), 2) / 2}`}
            on:click={() => {selectedRiding = id;}}
            on:mouseenter={() => {hoveredRiding = id;}}
            on:mouseleave={() => {hoveredRiding = null;}}
        >
            {@html riding.geometry[ro_year]}
        </g>
        {/each}
    </g>
</svg>
