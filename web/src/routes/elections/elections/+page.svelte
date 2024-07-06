<script>
    import Page from '$lib/components/Page.svelte';

    import ridings from '$lib/artifacts/riding.json';
    import runs from '$lib/artifacts/run.json';
    import candidates from '$lib/artifacts/candidate.json';
    import parties from '$lib/artifacts/party.json';
    import elections from '$lib/artifacts/election.json';
	import { onMount } from 'svelte';

    const ELECTION_TYPE_DISPLAY = {
        "GENERAL": "General Election",
        "BYELECTION": "By-Election",
    };

    let selectedRiding = null;

    let sortedElections;

    onMount(() => {
        sortedElections = Object.entries(elections).sort((a, b) => {
            if (a[1].date.year === b[1].date.year) {
                if (a[1].date.month === b[1].date.month) {
                    return a[1].date.day - b[1].date.day;
                }
                return a[1].date.month - b[1].date.month;
            }
            return a[1].date.year - b[1].date.year;
        });
    });
</script>

<Page>
    <p class="mt-8 font-bold text-2xl text-zinc-600">Federal Elections</p>
    {#if sortedElections !== undefined}
    {#each sortedElections as [electionId, election]}
    {#if election.type === "GENERAL"}
    <a
        class="flex flex-row border rounded mt-1 px-4 py-1 w-full hover:bg-zinc-100 hover:cursor-pointer"
        href={`/elections/elections/${electionId}`}
    >
        <p class="font-semibold mr-4 flex-grow">
            {election.date.year}-{election.date.month}-{election.date.day}
        </p>
        <p class="font-light">
            {ELECTION_TYPE_DISPLAY[election.type]}
        </p>
    </a>
    {/if}
    {/each}
    {/if}
    <div class="w-full mt-8">
    </div>
</Page>
