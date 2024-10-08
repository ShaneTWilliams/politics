
<script>
    import { onMount } from "svelte";

    import { getRidingByName } from "$lib/stats.js";

    import ridings from "$lib/artifacts/riding.json";

    let svgElement;
    let x = 0;
    let y = 0;
    let width = 0;
    let height = 0;

    const labradorRidingId = getRidingByName("Labrador");
    const labradorGeometryId = ridings[labradorRidingId].geometry_by_year["2013"];

    let labradorGeometry = null;
    onMount(() => {
        fetch(
            `/geometry/${labradorGeometryId}/simple.svg`
        ).then(
            (response) => response.text()
        ).then(
            (response) => {
                labradorGeometry = response;
            }
        ).then(
            () => {
                const bbox = svgElement.getBBox();
                x = bbox.x;
                y = -(bbox.y + bbox.height);
                width = bbox.width;
                height = bbox.height;
            }
        );
    });
</script>

<svg viewBox={`${x} ${y} ${width} ${height}`} class="h-full w-full svg-shadow">
    <g transform='scale(1,-1)' bind:this={svgElement}>
        <g class="fill-sol-light3 dark:fill-sol-dark3">
            {@html labradorGeometry}
        </g>
    </g>
</svg>
