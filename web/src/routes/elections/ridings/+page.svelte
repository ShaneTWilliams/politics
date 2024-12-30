<script>
    import Page from '$lib/components/Page.svelte';
    import List from '$lib/components/List.svelte';
    import Title from '$lib/components/Title.svelte';
    import TextInput from '$lib/components/TextInput.svelte';

    import ridings from '$lib/artifacts/riding.json';

    import { PROVINCES, RO_YEARS } from '$lib/constants.js';
    import { formatString } from '$lib/utils.js';

    let searchBarContents = "";
    let provinceFilter = "";
    let yearFilter = "";
    const currentYear = new Date().getFullYear();
    $: yearFilterValid = yearFilter === "" || (yearFilter >= 1867 && yearFilter <= currentYear && yearFilter % 1 === 0);

    $: sortedRidings = Object.entries(ridings).filter(
        ([ridingId, riding]) => {
            let match = true;
            for (const token of searchBarContents.split(' ')) {
                if (!riding.name.toLowerCase().includes(token.toLowerCase())) {
                    match = false;
                }
            }
            return match;
        }
    ).filter(
        ([ridingId, riding]) => {
            return provinceFilter === "" || riding.province === provinceFilter;
        }
    ).filter(
        ([ridingId, riding]) => {
            return !yearFilterValid || yearFilter === "" || ((riding.start_date.year <= yearFilter) && (!riding.end_date || riding.end_date.year >= yearFilter));
        }
    ).sort((a, b) => a[1].name.localeCompare(b[1].name));

    $: listData = sortedRidings ? sortedRidings.map(([ridingId, riding]) => {
        return {
            link: `/elections/ridings/${ridingId}`,
            title: formatString(riding.name),
            subtitle: PROVINCES[riding.province],
            category: `${riding.start_date.year}–${riding.end_date ? riding.end_date.year + "" : "    "}`
        };
    }) : [];
</script>

<svelte:head>
    <title>Canadian Electoral Ridings</title>
</svelte:head>

<Page>
    <Title text="Federal Electoral Ridings" />
    <List data={listData} emptyText="No ridings match the specified filters" hideSubtitleForSm={true} >
        <div class="flex flex-row space-x-2 items-start px-5 py-3 w-full overflow-x-scroll">
            <TextInput placeholder="Riding Name" bind:value={searchBarContents} />
            <TextInput placeholder="Year" bind:value={yearFilter} valid={yearFilterValid} />
            <select
                class="rounded-lg text-sm px-3 py-1 bg-sol-light2 dark:bg-sol-dark2"
                bind:value={provinceFilter}
            >
                <option value="">All regions</option>
                {#each Object.entries(PROVINCES) as [provinceId, province]}
                    <option value={provinceId}>{province}</option>
                {/each}
            </select>
        </div>
    </List>
</Page>
