<script>
    import Page from '$lib/components/Page.svelte';
    import List from '$lib/components/List.svelte';
    import Title from '$lib/components/Title.svelte';

    import ridings from '$lib/artifacts/riding.json';

    import { PROVINCES, RO_YEARS } from '$lib/constants.js';
    import { formatString } from '$lib/utils.js';

    let searchBarContents = "";
    let provinceFilter = "";
    let yearFilter = "";

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
            return yearFilter === "" || (riding.start_date.year <= yearFilter && (!riding.end_date || riding.end_date.year >= yearFilter));
        }
    ).sort((a, b) => {
        if (a[1].name < b[1].name) {
            return -1;
        }
        if (a[1].name > b[1].name) {
            return 1;
        }
        return 0;
    });

    $: listData = sortedRidings ? sortedRidings.map(([ridingId, riding]) => {
        return {
            link: `/elections/ridings/${ridingId}`,
            title: formatString(riding.name),
            subtitle: PROVINCES[riding.province],
            category: `${riding.start_date.year} - ${riding.end_date ? riding.end_date.year + "" : "    "}`
        };
    }) : [];
</script>

<svelte:head>
    <title>Canadian Electoral Ridings</title>
</svelte:head>

<Page>
    <Title text="Federal Electoral Ridings" />
    <List data={listData} page=0 emptyText="No ridings match the specified filters" >
        <div class="flex flex-row space-x-2 items-start px-5 py-3 w-full">
            <input
                class="rounded-lg w-48 text-sm px-3 py-1 bg-sol-light2 dark:bg-sol-dark2"
                type="text"
                placeholder="Riding Name"
                bind:value={searchBarContents}
            />
            <select
                class="rounded-lg text-sm px-3 py-1 bg-sol-light2 dark:bg-sol-dark2"
                bind:value={provinceFilter}
            >
                <option value="">All regions</option>
                {#each Object.entries(PROVINCES) as [provinceId, province]}
                    <option value={provinceId}>{province}</option>
                {/each}
            </select>
            <select
                class="rounded-lg text-sm px-3 py-1 bg-sol-light2 dark:bg-sol-dark2"
                bind:value={yearFilter}
            >
                <option value="">All years</option>
                {#each RO_YEARS as year}
                    <option value={year}>{year}</option>
                {/each}
            </select>
        </div>
    </List>
</Page>
