import elections from '$lib/artifacts/election.json';
import runs from '$lib/artifacts/run.json';
import ridings from '$lib/artifacts/riding.json';

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
        const difference = Math.abs(winner.votes - second.votes);
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
