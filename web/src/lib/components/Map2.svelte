<script>
	import { onMount } from "svelte";

    import ridings from "$lib/artifacts/debug_2003_ridings.json"

    let selectedRiding;

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

    onMount(() => {
        resizeSvg();
    });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->

<div class="flex flex-col w-full">
    <svg
        xmlns='http://www.w3.org/2000/svg'
        viewBox={`${x} ${y} ${width} ${height}`}
        >
        <g transform='scale(1,-1)' bind:this={svgEl}>
            {#each Object.entries(ridings) as [id, riding]}
            <g class={`
                stroke-white stroke-[1000]
                ${selectedRiding == id ? "fill-red-600" : ""}
                `}
                on:click={() => {
                    navigator.clipboard.writeText(id);
                    selectedRiding = id;
                }}
            >
                {@html riding.geometry}
            </g>
            {/each}
        </g>
    </svg>
    <p>
        {selectedRiding}
    </p>
</div>
