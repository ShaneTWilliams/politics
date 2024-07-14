<script>
    import Page from '$lib/components/Page.svelte';
    import Card from '$lib/components/Card.svelte';

    import { getRidingByName } from '$lib/stats.js';
	import { onMount } from 'svelte';

    let svgElement;
    let x = 0;
    let y = 0;
    let width = 0;
    let height = 0;

    const labradorRidingId = getRidingByName("Labrador");

    let labradorGeometry = null;
    onMount(() => {
        fetch(
            `/src/lib/artifacts/geometry/${labradorRidingId}/2013/simple.svg`
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

<svelte:head>
    <title>Federal Elections Visualizer</title>
</svelte:head>

<Page>
    <div class="flex flex-col items-center w-full">
        <div class="flex flex-row w-full max-w-3xl">
            <Card title="Parliaments" subtitle="Canada's 44 parliaments, summarized" link={"/"} />
            <Card title="Elections" subtitle="All of Canada's general and by-elections" link={"/elections/elections"} >
                <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox={`${x} ${y} ${width} ${height}`}
                    class="h-full w-full"
                >
                    <g transform='scale(1,-1)' bind:this={svgElement}>
                        <g class="fill-sol-light1">
                            {@html labradorGeometry}
                        </g>
                    </g>
                </svg>
            </Card>
        </div>
        <div class="flex flex-row w-full max-w-3xl">
            <Card title="Ridings" subtitle="Every electoral district in our history" link={"/"} />
            <Card title="Candidates" subtitle="Every election candidate since 1867" link={"/"} />
        </div>
    </div>
</Page>
