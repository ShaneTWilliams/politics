<script>
    import ArrowUp from '~icons/mdi/arrow-up'
    import ArrowDown from '~icons/mdi/arrow-down'

    import Page from '$lib/components/Page.svelte';
    import List from '$lib/components/List.svelte';
    import MiniBarGraph from '$lib/components/MiniBarGraph.svelte';
	import Title from '$lib/components/Title.svelte';

    import elections from '$lib/artifacts/election.json';

    import { MONTHS } from '$lib/constants.js';

    const ELECTION_TYPE_DISPLAY = {
        "GENERAL": "General Election",
        "BYELECTION": "By-Election",
    };

    let checked = false;
    let sortAscending = false;

    $: sortedElections = Object.entries(elections).sort((a, b) => {
        if (!sortAscending) {
            [a, b] = [b, a];
        }
        if (a[1].date.year === b[1].date.year) {
            if (a[1].date.month === b[1].date.month) {
                return a[1].date.day - b[1].date.day;
            }
            return a[1].date.month - b[1].date.month;
        }
        return a[1].date.year - b[1].date.year;
    }).filter(([electionId, election]) => {
        if (checked) {
            return true;
        }
        return election.type === "GENERAL";
    });

    $: listData = sortedElections ? sortedElections.map(([electionId, election]) => {
        return {
            link: `/elections/elections/${electionId}`,
            title: election.date.year,
            subtitle: `${MONTHS[election.date.month]} ${election.date.day}`,
            category: ELECTION_TYPE_DISPLAY[election.type],
            element: election.type === "GENERAL" ? MiniBarGraph : null,
            elementProps: { electionId }
        };
    }) : [];
</script>

<svelte:head>
    <title>Elections List</title>
</svelte:head>

<Page>
    <Title text="Federal Elections" />
    <List data={listData} emptyText="">
        <div class="flex flex-row w-full border-sol-light2 py-3">
            <button class="flex flex-row items-center hover:cursor-pointer" on:click={() => {sortAscending = !sortAscending;}}>
                <p class="font-black text-sm mr-2">Sort dates:</p>
                <p class="font-bold text-sm">
                {#if sortAscending}
                    <ArrowUp />
                {:else}
                    <ArrowDown />
                {/if}
                <p/>
            </button>
            <div class="grow" />
            <div class="flex flex-row">
                <input type="checkbox" id="check" bind:checked={checked}/>
                <label for="check" class="ml-2 font-light text-sm grow select-none">Show by-elections</label>
            </div>
        </div>
    </List>
</Page>
