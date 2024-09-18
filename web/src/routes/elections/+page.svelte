<script>
    import Page from '$lib/components/Page.svelte';
    import Card from '$lib/components/Card.svelte';

    import LucideInfo from '~icons/lucide/info';

    import { getRidingByName } from '$lib/stats.js';
	import { onMount } from 'svelte';

    let svgElement;
    let x = 0;
    let y = 0;
    let width = 0;
    let height = 0;

    const labradorRidingId = getRidingByName("Labrador");
    const nunavutRidingId = getRidingByName("Nunavut");

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
    <div class="flex flex-col items-center">
        <div class="flex flex-col items-center w-full mt-4 max-w-3xl space-y-4">
            <a href="/blog" class="w-full rounded-lg bg-sol-dark3 py-4 px-6 flex flex-row text-sol-light3">
                <LucideInfo class="text-lg mr-2" />
                <p class="">
                    Click here to read the accompanying blog post!
                </p>
            </a>
            <div class="flex flex-row w-full space-x-4">
                <Card title="Parties" subtitle="Registered political parties" link={"/"} />
                <Card title="Elections" subtitle="All of Canada's general and by-elections" link={"/elections/elections"} >
                </Card>
            </div>
            <div class="flex flex-row w-full space-x-4">
                <Card title="Ridings" subtitle="Every electoral district in our history" link={"/"} >
                    <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox={`${x} ${y} ${width} ${height}`}
                    class="h-full w-full"
                >
                    <g transform='scale(1,-1)' bind:this={svgElement}>
                        <g class="fill-sol-dark3">
                            {@html labradorGeometry}
                        </g>
                    </g>
                </svg>
                </Card>
                <Card title="Candidates" subtitle="Every election candidate since 1867" link={"/elections/candidates"} />
            </div>
            <div class="flex flex-row w-full">
                <Card title="Parliaments" subtitle="Canada's 44 parliaments, summarized" link={"/"} />
            </div>
        </div>
    </div>
</Page>
