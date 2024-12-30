<script>
    import Page from '$lib/components/Page.svelte';
    import List from '$lib/components/List.svelte';
    import Title from '$lib/components/Title.svelte';

    import ArrowUp from '~icons/mdi/arrow-up'
    import ArrowDown from '~icons/mdi/arrow-down'

    import parliaments from '$lib/artifacts/parliament.json';

    import { ordinalSuffix } from '$lib/utils.js';

    let sortAscending = false;

    $: listData = Object.entries(parliaments).sort(
        (a, b) => {
            return sortAscending ? a[1].number - b[1].number : b[1].number - a[1].number;
        }
    ).map(([parliamentId, parliament]) => {
        return {
            link: `/elections/parliaments/${parliamentId}`,
            title: `${ordinalSuffix(parliament.number)} parliament`,
            subtitle: "",
            category: `${parliament.start_date.year}-${parliament.end_date ? parliament.end_date.year : ''}`,
        };
    });
</script>

<svelte:head>
    <title>Canadian Parliaments</title>
</svelte:head>

<Page>
    <Title text="Parliaments" />
    <List data={listData} emptyText="You should not be seeing this text!">
        <div class="flex flex-row w-full justify-end pr-4">
            <button class="flex flex-row items-center hover:cursor-pointer mt-3" on:click={() => {sortAscending = !sortAscending;}}>
                <p class="font-black text-sm mr-2">Sort:</p>
                <p class="font-bold text-sm">
                    {#if sortAscending}
                    <ArrowUp />
                    {:else}
                    <ArrowDown />
                    {/if}
                <p/>
            </button>
        </div>
    </List>
</Page>
