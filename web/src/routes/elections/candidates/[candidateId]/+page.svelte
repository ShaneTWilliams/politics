<script>
    import { page } from '$app/stores';

    import CharmSquareTick from '~icons/charm/square-tick'
    import CharmSquareCross from '~icons/charm/square-cross'

    import Page from '$lib/components/Page.svelte';
    import HorizontalBar from '$lib/components/HorizontalBar.svelte';
    import SmallStat from '$lib/components/SmallStat.svelte';
    import Title from '$lib/components/Title.svelte';
    import PartySquare from '$lib/components/PartySquare.svelte';
    import Heading from '$lib/components/Heading.svelte'

    import { getRunsInRiding, isRealParty, isRealOccupation } from '$lib/stats.js';
    import { formatString, formatNumber } from '$lib/utils.js';
    import { PARTIES, PROVINCES, ELECTION_TYPE } from '$lib/constants.js';

    import candidates from '$lib/artifacts/candidate.json';
    import runs from '$lib/artifacts/run.json';
    import ridings from '$lib/artifacts/riding.json';
    import parties from '$lib/artifacts/party.json';
    import elections from '$lib/artifacts/election.json';

    $: candidate = candidates[$page.params.candidateId];

    $: candidateRuns = Object.entries(runs).filter(([runId, run]) => run.candidate === $page.params.candidateId);
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
    $: barData = candidateRuns.map(
        ([_, candidateRun]) => getRunsInRiding(candidateRun.election, candidateRun.riding)
    ).map(
        (electionRuns) => electionRuns.map(
            (run) => {
                return {
                    primaryLabel: `${candidates[run.candidate].first_name} ${candidates[run.candidate].last_name}`,
                    primaryLink: `/elections/candidates/${run.candidate}`,
                    secondaryLabel: `${PARTIES[parties[run.party].name]}`,
                    secondaryLink: isRealParty(run.party) ? `/elections/parties/${run.party}` : null,
                    count: run.votes > 0 ? run.votes : "Acclaimed",
                    color: parties[run.party].color,
                }
            }
        )
    );
</script>

<svelte:head>
    <title>{candidate.first_name} {candidate.last_name}</title>
</svelte:head>

<Page>
    <Title text={`${candidate.first_name} ${candidate.last_name}`} />

    <p class="text-lg mt-8 mb-2">Statistics</p>
    <div class="flex flex-row space-x-6 mb-2 overflow-x-scroll py-2">
        <SmallStat name="Number of Runs" value={ formatNumber(candidateRuns.length) } />
        <SmallStat name="Number of Wins" value={ formatNumber(totalWins) } />
        <SmallStat name="Total Votes" value={ formatNumber(totalVotes) } />
    </div>

    {#if candidateParties.length > 0}
    <Heading text="Affiliated Parties" />
    <div class="rounded-lg bg-sol-light2 dark:bg-sol-dark2 py-3 px-5 w-min text-sm mb-2 space-y-1">
        {#each candidateParties as partyId}
        <div class="flex flex-row items-center">
            <PartySquare {partyId}/>
            <p class="whitespace-nowrap font-bold">{PARTIES[parties[partyId].name]}</p>
        </div>
        {/each}
    </div>
    {/if}

    <Heading text="Electoral Record" />
    <div class="flex flex-col w-full">
    {#each candidateRuns as [runId, run], i}
        <div class="flex flex-col items-start rounded w-full mt-2 mb-6">
            <div class="flex flex-row items-center mb-1 text-sm w-full">
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
                <p class="text-md grow hidden sm:block">
                    &mdash; {PROVINCES[ridings[run.riding].province]}
                </p>
                <p class="text-sol-dark1 dark:text-sol-light1 mr-2 grow text-right">
                    {elections[run.election].date.year} {ELECTION_TYPE[elections[run.election].type]}
                </p>
            </div>
            <div class="flex flex-row items-center w-full">
                <div class="bg-sol-light2 dark:bg-sol-dark2 rounded-lg py-2 sm:py-4 px-4 sm:px-6 w-full">
                    <HorizontalBar data={barData[i]} showTotal={false} />
                </div>
            </div>
        </div>
    {/each}
    </div>

    {#if jobsAndYears.length > 0}
    <Heading text="Occupation History" />
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
