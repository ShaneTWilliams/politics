<script>
    import { page } from '$app/stores';

    import CharmSquareTick from '~icons/charm/square-tick'
    import CharmSquareCross from '~icons/charm/square-cross'

    import Page from '$lib/components/Page.svelte';
    import HorizontalBar from '$lib/components/HorizontalBar.svelte';
    import SmallStat from '$lib/components/SmallStat.svelte';
    import Title from '$lib/components/Title.svelte';
    import Heading from '$lib/components/Heading.svelte';
    import PartySquare from '$lib/components/PartySquare.svelte';
    import CanadaMap from '$lib/components/CanadaMap.svelte';

    import {
        getPartyLifetimeVotes,
        getPartyLifetimeRuns,
        getMostRecentGeneralElectionId,
        getPartyWinsInElection
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
</script>

<svelte:head>
    <title>{PARTIES[party.name]}</title>
</svelte:head>

<Page>
    <Title text={PARTIES[party.name]} />

    <Heading text="Statistics" />
    <div class="flex flex-row space-x-6 mb-2 overflow-x-scroll py-2">
        <SmallStat name="Lifetime Votes" value={ formatNumber(lifetimeVotes) } />
        <SmallStat name="Lifetime Runs" value={ formatNumber(lifetimeRuns) } />
        <SmallStat name="Current MPs" value={ formatNumber(mostRecentElectionWins) } />
    </div>

    {#if mostRecentElectionWins > 5}
    <Heading text={"2021 Election Performance"} />
    <CanadaMap electionId={mostRecentElection} focusParty={$page.params.partyId} />
    {/if}
</Page>
