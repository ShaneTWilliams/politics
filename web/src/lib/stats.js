import elections from '$lib/artifacts/election.json';
import runs from '$lib/artifacts/run.json';
import ridings from '$lib/artifacts/riding.json';
import candidates from '$lib/artifacts/candidate.json';
import parties from '$lib/artifacts/party.json';

import { PARTIES_THAT_ARENT_PARTIES, OCCUPATIONS_THAT_ARENT_OCCUPATIONS } from '$lib/constants';

function dateLaterThan(a, b) {
    if (a.year > b.year) {
        return true;
    } else if (a.year < b.year) {
        return false;
    }

    if (a.month > b.month) {
        return true;
    } else if (a.month < b.month) {
        return false;
    }

    if (a.day > b.day) {
        return true;
    } else if (a.day < b.day) {
        return false;
    }
    return false;
}

export function getClosestRidingInElection(electionId, closest) {
    let winners = {};
    let seconds = {};
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        if (run.result == "ACCLAIMED" || run.result == "ELECTED") {
            winners[run.riding] = runId;
        } else {
            const secondId = seconds[run.riding];
            if (secondId === undefined) {
                seconds[run.riding] = runId;
                continue;
            }
            const second = runs[secondId];
            if (run.votes > second.votes) {
                seconds[run.riding] = runId;
            }
        }
    }
    let closestRiding = null;
    let closestDifference = closest ? Infinity : 0;

    for (const riding in winners) {
        const winner = runs[winners[riding]];
        const second = runs[seconds[riding]];
        if (second === undefined) {
            continue;
        }
        const difference = Math.abs(winner.votes / second.votes);
        if ((closest && difference < closestDifference) || (!closest && difference > closestDifference)) {
            closestRiding = riding;
            closestDifference = difference;
        }
    }
    return closestRiding;
}

export function getRunsInRiding(electionId, ridingId) {
    let runsInRiding = [];
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        if (run.riding == ridingId) {
            runsInRiding.push(run);
        }
    }
    return runsInRiding;
}

export function getTotalElectionVotes(electionId) {
    let totalVotes = 0;
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        totalVotes += run.votes;
    }
    return totalVotes;
}

export function getVotesByParty(electionId) {
    let votesByParty = {};
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        if (votesByParty[run.party] === undefined) {
            votesByParty[run.party] = 0;
        }
        votesByParty[run.party] += run.votes;
    }
    return Object.entries(votesByParty).sort((a, b) => b[1] - a[1]);
}

export function getNumberOfCandidates(electionId) {
    return elections[electionId].runs.length;
}

export function getNumberOfRidings(electionId) {
    let ridings = new Set();
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        ridings.add(run.riding);
    }
    return ridings.size;
}

export function getRidingByName(name) {
    for (const [ridingId, riding] of Object.entries(ridings)) {
        if (riding.name == name) {
            return ridingId;
        }
    }
    return null;
}

export function getNumberOfCandidatesByParty(electionId) {
    let candidatesByParty = {};
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        if (candidatesByParty[run.party] === undefined) {
            candidatesByParty[run.party] = 0;
        }
        candidatesByParty[run.party] += 1;
    }
    return Object.entries(candidatesByParty).sort((a, b) => b[1] - a[1]);
}

export function getTopNSeatCounts(electionId, n) {
    let seatCounts = {};
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        if (seatCounts[run.party] === undefined) {
            seatCounts[run.party] = 0;
        }
        if (run.result == "ACCLAIMED" || run.result == "ELECTED") {
            seatCounts[run.party] += 1;
        }
    }
    return Object.entries(seatCounts).sort((a, b) => b[1] - a[1]).slice(0, n);
}

export function getElectionCandidatesByGender(electionId) {
    let candidatesByGender = {
        "MALE": 0,
        "FEMALE": 0,
        "OTHER": 0,
        "UNKNOWN": 0
    };
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        const candidate = candidates[run.candidate];
        candidatesByGender[candidate.gender] += 1;
    }
    return candidatesByGender;
}

export function getElectionWinnersByGender(electionId) {
    let winnersByGender = {
        "MALE": 0,
        "FEMALE": 0,
        "OTHER": 0,
        "UNKNOWN": 0
    };
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        if (run.result == "ACCLAIMED" || run.result == "ELECTED") {
            const candidate = candidates[run.candidate];
            winnersByGender[candidate.gender] += 1;
        }
    }
    return winnersByGender;
}

export function getSortedElectionsFromRiding(ridingId) {
    let electionsFromRiding = [];
    for (const electionId in elections) {
        for (const runId of elections[electionId].runs) {
            const run = runs[runId];
            if (run.riding == ridingId) {
                electionsFromRiding.push(electionId);
                break;
            }
        }
    }
    electionsFromRiding.sort((a, b) => elections[a].date.year - elections[b].date.year);
    return electionsFromRiding;
}

export function isRealParty(partyId) {
    return !PARTIES_THAT_ARENT_PARTIES.includes(parties[partyId].name);
}

export function isRealOccupation(occupation) {
    return !OCCUPATIONS_THAT_ARENT_OCCUPATIONS.includes(occupation);
}

export function getPartyLifetimeVotes(partyId) {
    let votes = 0;
    for (const [runId, run] of Object.entries(runs)) {
        if (run.party == partyId) {
            votes += run.votes;
        }
    }
    return votes;
}

export function getPartyLifetimeRuns(partyId) {
    let runCount = 0;
    for (const [runId, run] of Object.entries(runs)) {
        if (run.party == partyId) {
            runCount += 1;
        }
    }
    return runCount;
}

export function getPartyWinsInElection(partyId, electionId) {
    let count = 0;
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        if (run.party == partyId && (run.result == "ACCLAIMED" || run.result == "ELECTED")) {
            count += 1;
        }
    }
    return count;
}

export function getMostRecentGeneralElectionId() {
    let mostRecentId = null;
    let mostRecentYear = 0;
    for (const [electionId, election] of Object.entries(elections)) {
        if (election.date.year > mostRecentYear && election.type == "GENERAL") {
            mostRecentId = electionId;
            mostRecentYear = election.date.year;
        }
    }
    return mostRecentId;
}

export function getCandidateVoteProportion(runId) {
    const run = runs[runId];
    let totalVotes = 0;
    for (const otherRunId of elections[run.election].runs) {
        const otherRun = runs[otherRunId];
        if (run.riding == otherRun.riding) {
            totalVotes += otherRun.votes;
        }
    }
    return run.votes / totalVotes;
}

export function getPartyNumberOfMPsCurrently(partyId) {
    const electionId = getMostRecentGeneralElectionId();
    const generalElectionDate = elections[electionId].date;
    let heldRidings = Set()
    for (const runId of elections[electionId].runs) {
        const run = runs[runId];
        if (run.party == partyId && (run.result == "ACCLAIMED" || run.result == "ELECTED")) {
            count += 1;
            heldRidings.add(run.riding);
        }
    }

    for (const [electionId, election] of Object.entries(elections)) {
        if (dateLaterThan(election.date > generalElectionDate) && election.type == "BYELECTION") {
            for (const runId of election.runs) {
                const run = runs[runId];
                if (run.party == partyId && (run.result == "ACCLAIMED" || run.result == "ELECTED")) {
                    heldRidings.add(run.riding);
                }
            }
        }
    }
}
