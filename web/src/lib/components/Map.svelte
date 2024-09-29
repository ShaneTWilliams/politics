<script>
	import { onMount } from "svelte";

    import ridings from "$lib/artifacts/riding.json"
    import runs from "$lib/artifacts/run.json"
    import parties from "$lib/artifacts/party.json"
    import elections from "$lib/artifacts/election.json"
    import geometries from "$lib/artifacts/geometry.json"
    import detailViews from "$lib/artifacts/detailview.json"

    import { FILL_COLOURS, DETAIL_VIEWS } from "$lib/constants.js"

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

    export let selectedRiding=null, hoveredRiding=null, electionId, viewId, detail, clickable;

    let view = viewId === null ? null : detailViews[viewId];

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

    const actuallyShowDetail = detail || election.type == "BYELECTION";

    for (const runId of election.runs) {
        let run = runs[runId];
        if (view !== null && !view.ridings_by_year[ro_year].includes(run.riding)) {
            continue;
        }
        let riding = ridings[run.riding];
        const geometryId = riding.geometry_by_year[ro_year];
        const geometry = geometries[geometryId];
        if ((run.result === "ELECTED" || run.result === "ACCLAIMED")) {
            if (!actuallyShowDetail && parseInt(geometry.area) < 100) {
                continue;
            }
            ridingsToShow[run.riding] = {
                ...riding,
                geometry_id: geometryId,
                color: parties[run.party].color,
                victorParty: run.party,
            };
        }
    }

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
            (id) => {
                const geometryId = ridingsToShow[id].geometry_id;
                return fetch(
                    `/src/lib/artifacts/geometry/${geometryId}/${actuallyShowDetail ? "detailed" : "simple"}.svg`
                ).then(
                    (response) => response.text()
                ).then(
                    (response) => {
                        ridingsToShow[id].geometry = response;
                    }
                )
            },
            Object.keys(ridingsToShow),
            10
        ).then(
            () => {
                resizeSvg();
            }
        );
    });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->

<div class={`flex flex-col w-full ${election.type == "BYELECTION" ? "max-h-96" : ""}`}>
    {#if view !== null}
        <p class="text-xs text-sol-dark2 dark:text-sol-light2 text-left ml-2">
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
            {#each Object.entries(ridingsToShow) as [id, riding]}
            <g
                class={`
                        stroke-sol-light3 dark:stroke-sol-dark3 ${FILL_COLOURS[riding.color]}
                        ${hoveredRiding == id && clickable ? "opacity-70" : ""}
                        ${selectedRiding == id ? "opacity-70 animate-pulse" : ""}
                    `}
                style={`stroke-width: ${Math.pow(Math.min(width, height), 0.8) / 50}`}
                on:click={() => { if (clickable) {selectedRiding = id;}}}
                on:mouseenter={() => {hoveredRiding = id;}}
                on:mouseleave={() => {hoveredRiding = null;}}
                >
                {@html riding.geometry}
            </g>
            {/each}
        </g>
    </svg>
    {:else}
    <div
        class="diagonal-lines dark:dark-diagonal-lines w-full h-full rounded-lg border border-sol-light2"
        title="No ridings to show for this date"
    />
    {/if}
</div>
