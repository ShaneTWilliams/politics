<script>
    import Page from '$lib/components/Page.svelte';

    import { page } from '$app/stores';

    import elections from '$lib/artifacts/election.json';
    import runs from '$lib/artifacts/run.json';
    import parties from '$lib/artifacts/party.json';
    import ridings from '$lib/artifacts/riding.json';
    import candidates from '$lib/artifacts/candidate.json';

    import CanadaMap from '$lib/components/CanadaMap.svelte';
    import HorizontalBar from '$lib/components/HorizontalBar.svelte';
    import LargeCard from '$lib/components/LargeCard.svelte';
    import SmallStat from '$lib/components/SmallStat.svelte';
    import Title from '$lib/components/Title.svelte';
    import Subtitle from '$lib/components/Subtitle.svelte';
    import Heading from '$lib/components/Heading.svelte';

    import { MONTHS, PARTIES, PROVINCES, ELECTION_TYPE, PARTIES_THAT_ARENT_PARTIES } from '$lib/constants.js';
    import {
        getClosestRidingInElection,
        getRunsInRiding,
        getTotalElectionVotes,
        getVotesByParty,
        getNumberOfCandidates,
        getNumberOfRidings,
        getNumberOfCandidatesByParty,
        getElectionCandidatesByGender,
        getElectionWinnersByGender,
        isRealParty,
     } from '$lib/stats.js';
    import { formatNumber, formatString } from '$lib/utils.js';

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

    const candidatesByGender = getElectionCandidatesByGender($page.params.electionId);
    const winnersByGender = getElectionWinnersByGender($page.params.electionId);
</script>

<svelte:head>
    <title>{election.date.year} {ELECTION_TYPE[election.type]}</title>
</svelte:head>

<Page>
    <Title text={(election.type == "BYELECTION" ? formatString(ridings[election.riding].name) + " " : "") + ELECTION_TYPE[election.type]} />
    <Subtitle text={`${MONTHS[election.date.month]} ${election.date.day}, ${election.date.year}`} />

    {#if election.type == "GENERAL"}
    <Heading text="Results" />
    <LargeCard title="Seats by party">
        <HorizontalBar
            primaryLabels={party_results_sorted.map(([partyId, result]) => PARTIES[parties[partyId].name])}
            primaryLinks={party_results_sorted.map(([partyId, result]) => isRealParty(partyId) ? `/elections/parties/${partyId}` : null)}
            secondaryLabels={[]}
            counts={party_results_sorted.map(([partyId, result]) => result.count)}
            colors={party_results_sorted.map(([partyId, result]) => result.color)}
            showTotal={true}
        />
    </LargeCard>
    {/if}

    {#if election.type == "GENERAL"}
    <Heading text="Maps" />
    <CanadaMap electionId={$page.params.electionId}/>
    {/if}

    <Heading text="Statistics" />
    <div class="space-y-12">
        <div class="flex flex-row space-x-6 w-full">
            <SmallStat name="Total valid ballots" value={ formatNumber(totalVotesCast) } />
            <SmallStat name="Number of candidates" value={ formatNumber(numberOfCandidates) } />
            {#if election.type == "GENERAL"}
            <SmallStat name="Number of ridings" value={ formatNumber(numberOfRidings) } />
            {/if}
        </div>

        <LargeCard title="Popular Vote">
            {#if election.type == "GENERAL"}
            <HorizontalBar
                primaryLabels={votesByParty.map(([partyId, votes]) => PARTIES[parties[partyId].name])}
                primaryLinks={votesByParty.map(([partyId, votes]) => isRealParty(partyId) ? `/elections/parties/${partyId}` : null)}
                secondaryLabels={[]}
                counts={votesByParty.map(([partyId, votes]) => votes == 0 ? "Acclaimed" : votes)}
                colors={votesByParty.map(([partyId, votes]) => parties[partyId].color)}
                showTotal={votesByParty.length > 1}
            />
            {:else}
            <HorizontalBar
                primaryLabels={election.runs.map(run => candidates[runs[run].candidate].first_name + ' ' + candidates[runs[run].candidate].last_name)}
                primaryLinks={election.runs.map(run => `/elections/candidates/${runs[run].candidate}`)}
                secondaryLabels={election.runs.map(run => PARTIES[parties[runs[run].party].name])}
                secondaryLinks={election.runs.map(run => PARTIES_THAT_ARENT_PARTIES.includes(parties[runs[run].party].name) ? null : `/elections/parties/${runs[run].party}`)}
                counts={election.runs.map(run => runs[run].votes)}
                colors={election.runs.map(run => parties[runs[run].party].color)}
                showTotal={votesByParty.length > 1}
            />
            {/if}
        </LargeCard>

        {#if election.type == "GENERAL"}
        <LargeCard title="Candidates by Party">
            <HorizontalBar
                primaryLabels={numberOfCandidatesByParty.map(([partyId, numCandidates]) => PARTIES[parties[partyId].name])}
                primaryLinks={numberOfCandidatesByParty.map(([partyId, numCandidates]) => isRealParty(partyId) ? `/elections/parties/${partyId}` : null)}
                secondaryLabels={[]}
                counts={numberOfCandidatesByParty.map(([partyId, numCandidates]) => numCandidates)}
                colors={numberOfCandidatesByParty.map(([partyId, numCandidates]) => parties[partyId].color)}
                showTotal={true}
            />
        </LargeCard>
        {/if}

        {#if election.type == "GENERAL" && closestRiding && blowoutRiding}
        <LargeCard
            title="Closest Race"
            subtitle={closestRiding.name + ", " + PROVINCES[closestRiding.province]}
        >
            <HorizontalBar
                primaryLabels={closestRidingRuns.map(run => candidates[run.candidate].first_name + ' ' + candidates[run.candidate].last_name)}
                primaryLinks={closestRidingRuns.map(run => `/elections/candidates/${run.candidate}`)}
                secondaryLabels={closestRidingRuns.map(run => PARTIES[parties[run.party].name])}
                secondaryLinks={closestRidingRuns.map(run => PARTIES_THAT_ARENT_PARTIES.includes(parties[run.party].name) ? null : `/elections/parties/${run.party}`)}
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
                primaryLinks={blowoutRidingRuns.map(run => `/elections/candidates/${run.candidate}`)}
                secondaryLabels={blowoutRidingRuns.map(run => PARTIES[parties[run.party].name])}
                secondaryLinks={blowoutRidingRuns.map(run => PARTIES_THAT_ARENT_PARTIES.includes(parties[run.party].name) ? null : `/elections/parties/${run.party}`)}
                counts={blowoutRidingRuns.map(run => run.votes)}
                colors={blowoutRidingRuns.map(run => parties[run.party].color)}
                showTotal={false}
            />
        </LargeCard>
        <LargeCard title="Candidates by Gender">
            <HorizontalBar
                primaryLabels={["Male", "Female", "Other", "Unknown"]}
                secondaryLabels={[]}
                counts={[candidatesByGender["MALE"], candidatesByGender["FEMALE"], candidatesByGender["OTHER"], candidatesByGender["UNKNOWN"]]}
                colors={["BLUE", "PINK", "GREEN", "GREY"]}
                showTotal={false}
            />
        </LargeCard>
        <LargeCard title="Seats by Gender">
            <HorizontalBar
                primaryLabels={["Male", "Female", "Other", "Unknown"]}
                secondaryLabels={[]}
                counts={[winnersByGender["MALE"], winnersByGender["FEMALE"], winnersByGender["OTHER"], winnersByGender["UNKNOWN"]]}
                colors={["BLUE", "PINK", "GREEN", "GREY"]}
                showTotal={false}
            />
        </LargeCard>
        {/if}
    </div>
</Page>
