<script>
    import Page from '$lib/components/Page.svelte';
    import List from '$lib/components/List.svelte';
    import Title from '$lib/components/Title.svelte';

    import candidates from '$lib/artifacts/candidate.json';
    import parties from '$lib/artifacts/party.json';
    import runs from '$lib/artifacts/run.json';

    import { PARTIES } from '$lib/constants.js';

    let searchBarContents = "";
    let partyFilterContent = '';

    $: sortedCandidates = Object.entries(candidates).filter(
        ([candidateId, candidate]) => {
            const combined = candidate.first_name + ' ' + candidate.last_name;
            let match = true;
            for (const token of searchBarContents.split(' ')) {
                if (!combined.toLowerCase().includes(token.toLowerCase())) {
                    match = false;
                }
            }
            return match;
        }
    ).filter(
        ([candidateId, candidate]) => {
            for (const runId of candidate.runs) {
                const run = runs[runId];
                if (partyFilterContent === '' || run.party === partyFilterContent) {
                    return true;
                }
            }
            return false;
        }
    ).sort((a, b) => {
        if (a[1].last_name == b[1].last_name) {
            return a[1].first_name.localeCompare(b[1].first_name);
        }
        return a[1].last_name.localeCompare(b[1].last_name);
    });

    $: listData = sortedCandidates ? sortedCandidates.map(([candidateId, candidate]) => {
        return {
            link: `/elections/candidates/${candidateId}`,
            title: `${candidate.last_name}, ${candidate.first_name}`,
            subtitle: "",
            category: ""
        };
    }) : [];

    const sortedParties = Object.entries(parties).sort((a, b) => {
        if (a[1].name < b[1].name) {
            return -1;
        }
        if (a[1].name > b[1].name) {
            return 1;
        }
        return 0;
    });
</script>

<svelte:head>
    <title>Canadian Electoral Candidates</title>
</svelte:head>

<Page>
    <Title text="Federal Election Candidates" />
    <List data={listData} emptyText="No matching candidates found">
        <div class="flex flex-row space-x-2 items-start px-5 py-3 w-full overflow-x-scroll">
            <input
                class="rounded-lg w-48 text-sm px-3 py-1 bg-sol-light2 dark:bg-sol-dark2"
                type="text"
                placeholder="Candidate Name"
                bind:value={searchBarContents}
            />
            <select class="text-sm px-3 py-1 rounded-lg w-48 bg-sol-light2 dark:bg-sol-dark2" bind:value={partyFilterContent}>
                <option value={""} selected>{"Any Party"}</option>
                {#each sortedParties as [partyId, party]}
                <option value={partyId}>{PARTIES[party.name]}</option>
                {/each}
            </select>
        </div>
    </List>
</Page>
