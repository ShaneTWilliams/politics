<script>
    import Page from '$lib/components/Page.svelte';

    import { page } from '$app/stores';

    import elections from '$lib/artifacts/election.json';
    import runs from '$lib/artifacts/run.json';
    import parties from '$lib/artifacts/party.json';
    import ridings from '$lib/artifacts/riding.json';
    import candidates from '$lib/artifacts/candidate.json';

    import CanadaMap from '$lib/components/CanadaMap.svelte';
    import Map from '$lib/components/Map.svelte';
    import HorizontalBar from '$lib/components/HorizontalBar.svelte';
    import LargeCard from '$lib/components/LargeCard.svelte';
    import SmallStat from '$lib/components/SmallStat.svelte';

    import { MONTHS, PARTIES, PROVINCES } from '$lib/constants.js';
    import {
        getClosestRidingInElection,
        getRunsInRiding,
        getTotalElectionVotes,
        getVotesByParty,
        getNumberOfCandidates,
        getNumberOfRidings,
        getNumberOfCandidatesByParty,
     } from '$lib/stats.js';
    import { formatNumber } from '$lib/utils.js';

    const ELECTION_TYPE = {
        "GENERAL": "General Election",
        "BYELECTION": "By-Election",
    }

    let election = elections[$page.params.electionId];

    let party_results = {};
    let max_seats = 0;
    for (const run_id of election.runs) {
        let run = runs[run_id];
        if (run.result === "ELECTED" || run.result === "ACCLAIMED") {
            if (party_results[run.party] === undefined) {
                party_results[run.party] = {
                    count: 0,
                    color: parties[run.party].color,
                };
            }
            party_results[run.party].count += 1;
            if (party_results[run.party].count > max_seats) {
                max_seats = party_results[run.party].count;
            }
        }
    }
    let party_results_sorted = Object.entries(party_results).sort((a, b) => b[1].count - a[1].count);

    const closestRidingId = getClosestRidingInElection($page.params.electionId, true);
    const closestRidingRuns = getRunsInRiding($page.params.electionId, closestRidingId);
    const closestRiding = ridings[closestRidingId];

    const blowoutRidingId = getClosestRidingInElection($page.params.electionId, false);
    const blowoutRidingRuns = getRunsInRiding($page.params.electionId, blowoutRidingId);
    const blowoutRiding = ridings[blowoutRidingId];

    const votesByParty = getVotesByParty($page.params.electionId);

    const totalVotesCast = getTotalElectionVotes($page.params.electionId);
    const numberOfCandidates = getNumberOfCandidates($page.params.electionId);
    const numberOfRidings = getNumberOfRidings($page.params.electionId);

    const numberOfCandidatesByParty = getNumberOfCandidatesByParty($page.params.electionId);
</script>

<svelte:head>
    <title>{election.date.year} {ELECTION_TYPE[election.type]}</title>
</svelte:head>

<Page>
    <div class="my-8 ml-4">
        <p class="font-bold text-4xl text-sol-dark3">
            {election.type == "GENERAL" ? "General Election" : "By-Election"}
        </p>
        <p class="text-xl text-sol-light1 font-semibold ml-2">
            {MONTHS[election.date.month]} {election.date.day}, {election.date.year}
        </p>
    </div>
    <LargeCard title="">
        <HorizontalBar
            primaryLabels={party_results_sorted.map(([partyId, result]) => PARTIES[parties[partyId].name])}
            secondaryLabels={[]}
            counts={party_results_sorted.map(([partyId, result]) => result.count)}
            colors={party_results_sorted.map(([partyId, result]) => result.color)}
            showTotal={true}
        />
    </LargeCard>
    <div class="h-12"/>
    <CanadaMap electionId={$page.params.electionId}/>
    <p class="text-2xl font-bold mt-8 mb-4">Statistics</p>
    <div class="space-y-16">
        <LargeCard title="Popular Vote">
            <HorizontalBar
                primaryLabels={votesByParty.map(([partyId, votes]) => PARTIES[parties[partyId].name])}
                secondaryLabels={[]}
                counts={votesByParty.map(([partyId, votes]) => votesByParty.length == 1 ? "Acclaimed" : votes)}
                colors={votesByParty.map(([partyId, votes]) => parties[partyId].color)}
                showTotal={votesByParty.length > 1}
            />
        </LargeCard>
        <div class="flex flex-row justify-center space-x-6 w-full">
            <SmallStat name="Total votes cast" value={ formatNumber(totalVotesCast) } />
            <SmallStat name="Number of candidates" value={ formatNumber(numberOfCandidates) } />
            <SmallStat name="Number of ridings" value={ formatNumber(numberOfRidings) } />
        </div>
        <LargeCard title="Candidates by Party">
            <HorizontalBar
                primaryLabels={numberOfCandidatesByParty.map(([partyId, numCandidates]) => PARTIES[parties[partyId].name])}
                secondaryLabels={[]}
                counts={numberOfCandidatesByParty.map(([partyId, numCandidates]) => numCandidates)}
                colors={numberOfCandidatesByParty.map(([partyId, numCandidates]) => parties[partyId].color)}
                showTotal={false}
            />
        </LargeCard>
        {#if closestRiding && blowoutRiding}
        <LargeCard
            title="Closest Race"
            subtitle={closestRiding.name + ", " + PROVINCES[closestRiding.province]}
        >
            <HorizontalBar
                primaryLabels={closestRidingRuns.map(run => candidates[run.candidate].first_name + ' ' + candidates[run.candidate].last_name)}
                secondaryLabels={closestRidingRuns.map(run => PARTIES[parties[run.party].name])}
                counts={closestRidingRuns.map(run => run.votes)}
                colors={closestRidingRuns.map(run => parties[run.party].color)}
                showTotal={false}
            />
        </LargeCard>
        <LargeCard
            title="Biggest Blowout"
            subtitle={blowoutRiding.name + ", " + PROVINCES[blowoutRiding.province]}
        >
            <HorizontalBar
                primaryLabels={blowoutRidingRuns.map(run => candidates[run.candidate].first_name + ' ' + candidates[run.candidate].last_name)}
                secondaryLabels={blowoutRidingRuns.map(run => PARTIES[parties[run.party].name])}
                counts={blowoutRidingRuns.map(run => run.votes)}
                colors={blowoutRidingRuns.map(run => parties[run.party].color)}
                showTotal={false}
            />
        </LargeCard>
        {/if}
    </div>
</Page>
