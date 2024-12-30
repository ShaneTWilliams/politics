<script>
    import { page } from '$app/stores';

    import CharmSquareTick from '~icons/charm/square-tick'
    import CharmSquareCross from '~icons/charm/square-cross'

    import Page from '$lib/components/Page.svelte';
    import HorizontalBar from '$lib/components/HorizontalBar.svelte';
    import SmallStat from '$lib/components/SmallStat.svelte';
    import Title from '$lib/components/Title.svelte';
    import Heading from '$lib/components/Heading.svelte';
    import LargeCard from '$lib/components/LargeCard.svelte';
    import CanadaMap from '$lib/components/CanadaMap.svelte';

    import {
        getPartyLifetimeVotes,
        getPartyLifetimeRuns,
        getMostRecentGeneralElectionId,
        getPartyWinsInElection,
        getPartyPopularVoteByElection,
        getLifetimeNumberOfCandidates,
        getPartySeatsByElection,
        getTotalElectionVotes,
        getSeatsInElection,
    } from '$lib/stats.js';
    import { formatString, formatNumber } from '$lib/utils.js';
    import { PARTIES, PROVINCES, ELECTION_TYPE, FILL_COLOURS } from '$lib/constants.js';

    import candidates from '$lib/artifacts/candidate.json';
    import runs from '$lib/artifacts/run.json';
    import ridings from '$lib/artifacts/riding.json';
    import parties from '$lib/artifacts/party.json';
    import elections from '$lib/artifacts/election.json';

    $: party = parties[$page.params.partyId];

    $: mostRecentElection = getMostRecentGeneralElectionId();
    $: mostRecentElectionWins = getPartyWinsInElection($page.params.partyId, mostRecentElection);
    $: lifetimeVotes = getPartyLifetimeVotes($page.params.partyId);
    $: lifetimeRuns = getPartyLifetimeRuns($page.params.partyId);
    $: lifetimeCandidates = getLifetimeNumberOfCandidates($page.params.partyId);
    $: voteByGeneralElectionData = Object.entries(getPartyPopularVoteByElection($page.params.partyId)).map(
        ([electionId, votes]) => ({
            primaryLabel: elections[electionId].date.year,
            primaryLink: `/elections/elections/${electionId}`,
            count: votes,
            color: party.color,
        })
    );
    $: seatsByGeneralElectionData = Object.entries(getPartySeatsByElection($page.params.partyId)).map(
        ([electionId, seats]) => ({
            primaryLabel: elections[electionId].date.year,
            primaryLink: `/elections/elections/${electionId}`,
            count: seats,
            color: party.color,
        })
    );
    $: proportionOfPopularVotesData = Object.entries(getPartyPopularVoteByElection($page.params.partyId)).map(
        ([electionId, votes]) => ({
            primaryLabel: elections[electionId].date.year,
            primaryLink: `/elections/elections/${electionId}`,
            count: 100 * votes / getTotalElectionVotes(electionId),
            color: party.color,
        })
    );
    $: proportionOfSeatsData = Object.entries(getPartySeatsByElection($page.params.partyId)).map(
        ([electionId, seats]) => ({
            primaryLabel: elections[electionId].date.year,
            primaryLink: `/elections/elections/${electionId}`,
            count: 100 * seats / getSeatsInElection(electionId),
            color: party.color,
        })
    );
    $: maxNumberOfSeatsEverWon = Math.max(...Object.values(getPartySeatsByElection($page.params.partyId)));
</script>

<svelte:head>
    <title>{PARTIES[party.name]}</title>
</svelte:head>

<Page>
    <Title text={PARTIES[party.name]} />

    <Heading text="Lifetime Statistics" />
    <div class="flex flex-row space-x-6 mb-2 overflow-x-scroll py-2">
        <SmallStat name="Votes" value={ formatNumber(lifetimeVotes) } />
        <SmallStat name="Races" value={ formatNumber(lifetimeRuns) } />
        <SmallStat name="Candidates" value={ formatNumber(lifetimeCandidates) } />
    </div>

    {#if mostRecentElectionWins > 3}
    <Heading text={"2021 Election Performance"} />
    {#key $page.params.partyId}
    <CanadaMap electionId={mostRecentElection} focusParty={$page.params.partyId} />
    {/key}
    {/if}

    <Heading text="Statistics" />
    <div class="space-y-12">
    {#if voteByGeneralElectionData.length > 0}
    <LargeCard title="Popular Vote by General Election">
        <HorizontalBar data={voteByGeneralElectionData} showTotal={false} />
    </LargeCard>
    <LargeCard title="Proportion of Popular Vote by General Election">
        <HorizontalBar data={proportionOfPopularVotesData} showTotal={false} pct={true} />
    </LargeCard>
    {/if}
    {#if seatsByGeneralElectionData.length > 0}
    <LargeCard title="Seats Won by General Election">
        <HorizontalBar data={seatsByGeneralElectionData} showTotal={false} />
    </LargeCard>
    {/if}
    {#if maxNumberOfSeatsEverWon > 5}
    <LargeCard title="Proportion of Seats Won by General Election">
        <HorizontalBar data={proportionOfSeatsData} showTotal={false} pct={true} />
    </LargeCard>
    {/if}
    </div>
</Page>
