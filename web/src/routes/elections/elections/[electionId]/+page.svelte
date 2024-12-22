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
    let party_results_sorted = Object.entries(
        party_results
    ).sort(
        (a, b) => b[1].count - a[1].count
    ).map(([partyId, result]) => {
        return {
            primaryLabel: PARTIES[parties[partyId].name],
            primaryLink: isRealParty(partyId) ? `/elections/parties/${partyId}` : null,
            count: result.count,
            color: result.color
        };
    });

    const closestRidingId = getClosestRidingInElection($page.params.electionId, true);
    const closestRidingRuns = getRunsInRiding($page.params.electionId, closestRidingId).map(
        (run) => {
            return {
                primaryLabel: candidates[run.candidate].first_name + ' ' + candidates[run.candidate].last_name,
                primaryLink: `/elections/candidates/${run.candidate}`,
                secondaryLabel: PARTIES[parties[run.party].name],
                secondaryLink: PARTIES_THAT_ARENT_PARTIES.includes(parties[run.party].name) ? null : `/elections/parties/${run.party}`,
                count: run.votes,
                color: parties[run.party].color,
            };
        }
    );
    const closestRiding = ridings[closestRidingId];

    const blowoutRidingId = getClosestRidingInElection($page.params.electionId, false);
    const blowoutRidingRuns = getRunsInRiding($page.params.electionId, blowoutRidingId).map(
        (run) => {
            return {
                primaryLabel: candidates[run.candidate].first_name + ' ' + candidates[run.candidate].last_name,
                primaryLink: `/elections/candidates/${run.candidate}`,
                secondaryLabel: PARTIES[parties[run.party].name],
                secondaryLink: PARTIES_THAT_ARENT_PARTIES.includes(parties[run.party].name) ? null : `/elections/parties/${run.party}`,
                count: run.votes,
                color: parties[run.party].color,
            };
        }
    );
    const blowoutRiding = ridings[blowoutRidingId];

    const votesByParty = getVotesByParty($page.params.electionId).map(
        ([partyId, votes]) => {
            return {
                primaryLabel: PARTIES[parties[partyId].name],
                primaryLink: isRealParty(partyId) ? `/elections/parties/${partyId}` : null,
                count: votes == 0 ? "Acclaimed" : votes,
                color: parties[partyId].color
            };
        }
    );

    const totalVotesCast = getTotalElectionVotes($page.params.electionId);
    const numberOfCandidates = getNumberOfCandidates($page.params.electionId);
    const numberOfRidings = getNumberOfRidings($page.params.electionId);

    const numberOfCandidatesByParty = getNumberOfCandidatesByParty($page.params.electionId).map(
        ([partyId, numCandidates]) => {
            return {
                primaryLabel: PARTIES[parties[partyId].name],
                primaryLink: isRealParty(partyId) ? `/elections/parties/${partyId}` : null,
                count: numCandidates,
                color: parties[partyId].color,
            };
        }
    );

    const candidatesByGender = getElectionCandidatesByGender($page.params.electionId);
    const winnersByGender = getElectionWinnersByGender($page.params.electionId);

    const candidatesByGenderBarData = [
        {
            primaryLabel: "Male",
            count: candidatesByGender["MALE"],
            color: "BLUE"
        },
        {
            primaryLabel: "Female",
            count: candidatesByGender["FEMALE"],
            color: "PINK"
        },
        {
            primaryLabel: "Other",
            count: candidatesByGender["OTHER"],
            color: "GREEN"
        },
        {
            primaryLabel: "Unknown",
            count: candidatesByGender["UNKNOWN"],
            color: "GREY"
        }
    ]

    const winnersByGenderBarData = [
        {
            primaryLabel: "Male",
            count: winnersByGender["MALE"],
            color: "BLUE"
        },
        {
            primaryLabel: "Female",
            count: winnersByGender["FEMALE"],
            color: "PINK"
        },
        {
            primaryLabel: "Other",
            count: winnersByGender["OTHER"],
            color: "GREEN"
        },
        {
            primaryLabel: "Unknown",
            count: winnersByGender["UNKNOWN"],
            color: "GREY"
        }
    ]


    const electionRuns = election.runs.map((run) => {
        return {
            primaryLabel: candidates[runs[run].candidate].first_name + ' ' + candidates[runs[run].candidate].last_name,
            primaryLinks: `/elections/candidates/${runs[run].candidate}`,
            secondaryLabel: PARTIES[parties[runs[run].party].name],
            secondaryLink: PARTIES_THAT_ARENT_PARTIES.includes(parties[runs[run].party].name) ? null : `/elections/parties/${runs[run].party}`,
            count: runs[run].votes,
            color: parties[runs[run].party].color
        };
    });
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
        <HorizontalBar data={party_results_sorted} showTotal={true} />
    </LargeCard>
    {/if}

    {#if election.type == "GENERAL"}
    <Heading text="Maps" />
    <CanadaMap electionId={$page.params.electionId}/>
    {/if}

    <Heading text="Statistics" />
    <div class="space-y-12">
        <div class="flex flex-row space-x-6 w-full overflow-x-scroll py-2">
            <SmallStat name="Total valid ballots" value={ formatNumber(totalVotesCast) } />
            <SmallStat name="Number of candidates" value={ formatNumber(numberOfCandidates) } />
            {#if election.type == "GENERAL"}
            <SmallStat name="Number of ridings" value={ formatNumber(numberOfRidings) } />
            {/if}
        </div>

        <LargeCard title="Popular Vote">
            {#if election.type == "GENERAL"}
            <HorizontalBar data={votesByParty} showTotal={votesByParty.length > 1} />
            {:else}
            <HorizontalBar data={electionRuns} showTotal={votesByParty.length > 1} />
            {/if}
        </LargeCard>

        {#if election.type == "GENERAL"}
        <LargeCard title="Candidates by Party">
            <HorizontalBar data={numberOfCandidatesByParty} showTotal={true} />
        </LargeCard>
        {/if}

        {#if election.type == "GENERAL" && closestRiding && blowoutRiding}
        <LargeCard
            title="Closest Race"
            subtitle={closestRiding.name + ", " + PROVINCES[closestRiding.province]}
        >
            <HorizontalBar data={closestRidingRuns} showTotal={false} />
        </LargeCard>
        <LargeCard
            title="Biggest Blowout"
            subtitle={blowoutRiding.name + ", " + PROVINCES[blowoutRiding.province]}
        >
            <HorizontalBar data={blowoutRidingRuns} showTotal={false} />
        </LargeCard>
        <LargeCard title="Candidates by Gender">
            <HorizontalBar data={candidatesByGenderBarData} showTotal={false} />
        </LargeCard>
        <LargeCard title="Seats by Gender">
            <HorizontalBar data={winnersByGenderBarData} showTotal={false} />
        </LargeCard>
        {/if}
    </div>
</Page>
