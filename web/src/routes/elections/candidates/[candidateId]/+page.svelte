<script>
    import { page } from '$app/stores';

    import CharmSquareTick from '~icons/charm/square-tick'
    import CharmSquareCross from '~icons/charm/square-cross'

    import Page from '$lib/components/Page.svelte';
    import HorizontalBar from '$lib/components/HorizontalBar.svelte';
    import SmallStat from '$lib/components/SmallStat.svelte';
    import Title from '$lib/components/Title.svelte';
    import PartySquare from '$lib/components/PartySquare.svelte';

    import { getRunsInRiding, isRealParty, isRealOccupation } from '$lib/stats.js';
    import { formatString, formatNumber } from '$lib/utils.js';
    import { PARTIES, PROVINCES, ELECTION_TYPE, FILL_COLOURS } from '$lib/constants.js';

    import candidates from '$lib/artifacts/candidate.json';
    import runs from '$lib/artifacts/run.json';
    import ridings from '$lib/artifacts/riding.json';
    import parties from '$lib/artifacts/party.json';
    import elections from '$lib/artifacts/election.json';

    $: candidate = candidates[$page.params.candidateId];

    $: candidateRuns = Object.entries(runs).filter(([runId, run]) => run.candidate === $page.params.candidateId).toReversed();
    $: jobsAndYears = candidateRuns.filter(
        ([runId, run]) => isRealOccupation(run.occupation)
    ).map(([runId, run]) => {
        return {
            job: run.occupation,
            year: elections[run.election].date.year,
        };
    });
    $: totalVotes = candidateRuns.reduce((acc, [runId, run]) => acc + run.votes, 0);
    $: totalWins = candidateRuns.filter(([runId, run]) => run.result === "ELECTED" || run.result === "ACCLAIMED").length;
    $: candidateParties = candidateRuns.map(
        ([runId, run]) => run.party
    ).filter(
        (value, index, self) => self.indexOf(value) === index && isRealParty(value)
    );
</script>

<svelte:head>
    <title>{candidate.first_name} {candidate.last_name}</title>
</svelte:head>

<Page>
    <Title text={`${candidate.first_name} ${candidate.last_name}`} />

    <p class="text-lg mt-8 mb-2">Statistics</p>
    <div class="flex flex-row space-x-6 mb-2">
        <SmallStat name="Number of Runs" value={ formatNumber(candidateRuns.length) } />
        <SmallStat name="Number of Wins" value={ formatNumber(totalWins) } />
        <SmallStat name="Total Votes" value={ formatNumber(totalVotes) } />
    </div>

    {#if candidateParties.length > 0}
    <p class="text-lg mt-8 mb-2">Affiliated Parties</p>
    <div class="rounded-lg bg-sol-light2 dark:bg-sol-dark2 py-3 px-5 w-min text-sm mb-2 space-y-1">
        {#each candidateParties as partyId}
        <div class="flex flex-row items-center">
            <PartySquare {partyId}/>
            <p class="whitespace-nowrap font-bold">{PARTIES[parties[partyId].name]}</p>
        </div>
        {/each}
    </div>
    {/if}

    <p class="text-lg mt-8">Electoral Record</p>
    <div class="flex flex-col w-full">
    {#each candidateRuns as [runId, run]}
        {@const allRuns = getRunsInRiding(run.election, run.riding) }
        <div class="flex flex-row items-center rounded w-full mt-2 mb-6">
            <div class="w-full">
                <div class="flex flex-row items-center mb-1 text-sm">
                    <div class="text-md ml-2 mr-3">
                        {#if run.result == "ACCLAIMED" || run.result == "ELECTED"}
                            <CharmSquareTick class="text-sol-green" />
                        {:else if run.result == "DEFEATED"}
                            <CharmSquareCross class="text-sol-red" />
                        {/if}
                    </div>
                    <p class="font-bold mr-2">
                        {formatString(ridings[run.riding].name)}
                    </p>
                    <p class="text-md grow">
                        &mdash; {PROVINCES[ridings[run.riding].province]}
                    </p>
                    <p class="text-sol-dark1 dark:text-sol-light1 mr-2">
                        {elections[run.election].date.year} {ELECTION_TYPE[elections[run.election].type]}
                    </p>
                </div>
                <div class="flex flex-row items-center w-full">
                    <div class="bg-sol-light2 dark:bg-sol-dark2 rounded-lg py-4 px-6 w-full">
                        <HorizontalBar
                            primaryLabels={allRuns.map(run => `${candidates[run.candidate].first_name} ${candidates[run.candidate].last_name}`)}
                            primaryLinks={allRuns.map(run => `/elections/candidates/${run.candidate}`)}
                            secondaryLabels={allRuns.map(run => `${PARTIES[parties[run.party].name]}`)}
                            secondaryLinks={allRuns.map(run => `/elections/parties/${run.party}`)}
                            counts={allRuns.map(run => run.votes > 0 ? run.votes : "Acclaimed")}
                            colors={allRuns.map(run => parties[run.party].color)}
                            showTotal={false}
                        />
                    </div>
                </div>
            </div>
        </div>
    {/each}
    </div>

    {#if jobsAndYears.length > 0}
    <p class="text-lg mb-2">Occupation History</p>
    <div class="rounded-lg bg-sol-light2 dark:bg-sol-dark2 p-3 w-min text-sm mb-2">
        {#each jobsAndYears as jobAndYear}
        <div class="flex flex-row">
            <p class="font-bold grow whitespace-nowrap mr-10">{jobAndYear.job == null ? "Unknown" : jobAndYear.job}</p>
            <p class="">{jobAndYear.year}</p>
        </div>
        {/each}
    </div>
    {/if}
</Page>
