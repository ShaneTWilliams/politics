<script>
	import { onMount } from "svelte";

    import ridings from "$lib/artifacts/riding.json"
    import runs from "$lib/artifacts/run.json"
    import parties from "$lib/artifacts/party.json"
    import elections from "$lib/artifacts/election.json"
    import geometries from "$lib/artifacts/geometry.json"
    import detailViews from "$lib/artifacts/detailview.json"

    import { FILL_COLOURS, DETAIL_VIEWS } from "$lib/constants.js"
    import {
        getCandidateVoteProportion,
        getElectionGeographyForView,
     } from "$lib/stats.js"

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

    export let selectedRiding=null, hoveredRiding=null, electionId, viewId, detail, clickable, focusParty, doneLoading, lightStroke=false;

    let svgElement;
    let x = 0;
    let y = 0;
    let width = 0;
    let height = 0;

    function resizeSvg() {
        if (view === null) {
            const bbox = svgElement.getBBox();
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

    $: view = viewId === null ? null : detailViews[viewId];
    $: election = elections[electionId];
    $: actuallyShowDetail = detail || election.type == "BYELECTION";

    $: ridingsToShow = getElectionGeographyForView(electionId, viewId).filter(
        (riding) => (actuallyShowDetail || parseInt(riding.area) > 100)
    ).map(
        (riding) => {
            let opacity = 100;

            let color = parties[riding.party].color;
            if (focusParty) {
                if (riding.party != focusParty) {
                    color = "BASE2";
                } else {
                    opacity = Math.min(100, 400 * Math.pow(getCandidateVoteProportion(riding.runId), 2));
                }
            }
            return {
                ...riding,
                color: color,
                opacity: 100,
                victorParty: riding.party,
            };
        }
    );

    onMount(() => {
        window.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                selectedRiding = null;
            }
        });

        async function promiseAllInBatches(task, items, batchSize) {
            let position = 0;
            let results = [];
            while (position < items.length) {
                const itemsForBatch = items.slice(position, position + batchSize);
                results = [...results, ...await Promise.all(itemsForBatch.map(item => task(item)))];
                position += batchSize;
            }
            return results;
        }

        promiseAllInBatches(
            ([i, riding]) => {
                return fetch(
                    `/geometry/${riding.geometryId}/${actuallyShowDetail ? "detailed" : "simple"}.svg`
                ).then(
                    (response) => response.text()
                ).then(
                    (response) => {
                        ridingsToShow[i].geometry = response;
                    }
                )
            },
            Object.entries(ridingsToShow),
            10
        ).then(
            () => {
                resizeSvg();
                doneLoading = true;
            }
        );
    });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->

<div class={`flex flex-col w-full truncate ${election.type == "BYELECTION" ? "max-h-96" : ""}`}>
    {#if view}
        <p class="text-xs text-sol-dark2 dark:text-sol-light2 text-left sm:ml-2 truncate">
            {DETAIL_VIEWS[view.name]}
        </p>
    {/if}
    {#if Object.keys(ridingsToShow).length > 1 || viewId === null}
    <svg
        xmlns='http://www.w3.org/2000/svg'
        viewBox={`${x} ${y} ${width} ${height}`}
        class="rounded-lg"
    >
        <g transform='scale(1,-1)' bind:this={svgElement}>
            {#each ridingsToShow as riding}
            <g
                class={`
                    ${FILL_COLOURS[riding.color]}
                    ${selectedRiding == riding.riding ? "animate-pulse" : ""}
                    ${lightStroke ? "stroke-sol-light2 dark:stroke-sol-dark2" : "stroke-sol-light3 dark:stroke-sol-dark3"}
                `}
                style={`
                    stroke-width: ${Math.pow(Math.min(width, height), 0.8) / 50};
                    opacity: ${clickable && (hoveredRiding == riding.riding || selectedRiding == riding.riding) ? Math.max(0, riding.opacity - 20) : riding.opacity}%
                `}
                on:click={() => { if (clickable) {selectedRiding = riding.riding;}}}
                on:mouseenter={() => {hoveredRiding = riding.riding;}}
                on:mouseleave={() => {hoveredRiding = null;}}
                >
                {@html riding.geometry}
            </g>
            {/each}
        </g>
    </svg>
    {:else}
    <div
        class="diagonal-lines dark:dark-diagonal-lines w-full h-full rounded-lg border border-sol-light2 dark:border-sol-dark2 aspect-square"
        title="No ridings to show for this date"
    />
    {/if}
</div>
