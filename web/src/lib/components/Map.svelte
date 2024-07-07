<script>
	import { onMount } from "svelte";

    import ridings from "$lib/artifacts/riding.json"
    import runs from "$lib/artifacts/run.json"
    import parties from "$lib/artifacts/party.json"
    import elections from "$lib/artifacts/election.json"

    const COLOR_TO_FILL = {
        "RED":      "fill-red-700",
        "ORANGE":   "fill-amber-600",
        "YELLOW":   "fill-yellow-700",
        "GREEN":    "fill-green-700",
        "BLUE":     "fill-blue-700",
        "PURPLE":   "fill-purple-700",
        "GREY":     "fill-grey-700",
        "BLACK":    "fill-black-700",
        "WHITE":    "fill-white-700",
        "BROWN":    "fill-brown-700",
        "PINK":     "fill-pink-700",
    };
    const COLOR_TO_HOVER_FILL = {
        "RED":      "hover:fill-red-500",
        "ORANGE":   "hover:fill-amber-500",
        "YELLOW":   "hover:fill-yellow-500",
        "GREEN":    "hover:fill-green-500",
        "BLUE":     "hover:fill-blue-500",
        "PURPLE":   "hover:fill-purple-500",
        "GREY":     "hover:fill-grey-500",
        "BLACK":    "hover:fill-black-500",
        "WHITE":    "hover:fill-white-500",
        "BROWN":    "hover:fill-brown-500",
        "PINK":     "hover:fill-pink-500",
    };

    export let selectedRiding, electionId;

    let svgEl;
    let x = 0;
    let y = 0;
    let width = 0;
    let height = 0;

    function resizeSvg() {
        const bbox = svgEl.getBBox();
        x = bbox.x;
        y = -(bbox.y + bbox.height);
        width = bbox.width;
        height = bbox.height;
    }

    let ridingsToShow = {};
    let election = elections[electionId];
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
                color: color
            };
        }
    }

    onMount(() => {
        resizeSvg();
    });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->

<svg
    xmlns='http://www.w3.org/2000/svg'
    viewBox={`${x} ${y} ${width} ${height}`}
>
    <g transform='scale(1,-1)' bind:this={svgEl}>
        {#each Object.entries(ridingsToShow) as [id, riding]}
        <g class={`
            stroke-white stroke-[1000]
            ${selectedRiding == id ? "" : COLOR_TO_HOVER_FILL[riding.color]}
            ${selectedRiding == id ? "fill-black" : COLOR_TO_FILL[riding.color]}
        `}
            on:click={() => {selectedRiding = id}
        }>
            {@html riding.geometry}
        </g>
        {/each}
    </g>
</svg>
