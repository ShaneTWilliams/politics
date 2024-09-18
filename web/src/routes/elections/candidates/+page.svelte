<script>
    import Page from '$lib/components/Page.svelte';

    import candidates from '$lib/artifacts/candidate.json';
    import parties from '$lib/artifacts/party.json';
    import runs from '$lib/artifacts/run.json';

    import { PARTIES } from '$lib/constants.js';

    let searchBarContents = '';
    let partyFilterContent = '';
    $: sortedCandidates = Object.entries(candidates).filter(
        ([candidateId, candidate]) => {
            const combined = candidate.first_name + ' ' + candidate.last_name;
            return combined.toLowerCase().includes(searchBarContents.toLowerCase());
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
        if (a[1].last_name < b[1].last_name) {
            return -1;
        }
        if (a[1].last_name > b[1].last_name) {
            return 1;
        }
        return 0;
    });
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
    <p class="mt-6 mb-2 font-bold text-2xl text-sol-dark3">Federal Electoral Candidates</p>
    <div class="flex flex-col items-center">
        <div class="flex flex-row space-x-2 mb-4 items-start px-5 py-3 w-full">
            <input
                class="rounded-lg w-48 text-sm px-3 py-1 bg-sol-light2"
                type="text"
                placeholder="Candidate Name"
                bind:value={searchBarContents}
            />
            <select class="text-sm px-3 py-1 rounded-lg w-48 bg-sol-light2" bind:value={partyFilterContent}>
                <option value={""} selected>{"Any Party"}</option>
                {#each sortedParties as [partyId, party]}
                <option value={partyId}>{PARTIES[party.name]}</option>
                {/each}
            </select>
        </div>
        <div class="flex flex-col w-full">
            {#each sortedCandidates.slice(0, 20) as [candidateId, candidate]}
                <a
                    class="flex flex-row items-center px-4 py-3 hover:cursor-pointer border-sol-light1 border-t border-sol-light2 hover:bg-sol-light2"
                    href={`/elections/candidates/${candidateId}`}
                >
                    <p class="font-black text-sol-dark3 text-sm mr-6">{candidate.last_name}, {candidate.first_name}</p>
                </a>
            {/each}
        </div>
    </div>
</Page>
