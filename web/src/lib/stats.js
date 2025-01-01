import { elections, runs, ridings, candidates, parties, parliaments, detailViews, geometries } from '$lib/data.js';

import {
	PARTIES_THAT_ARENT_PARTIES,
	OCCUPATIONS_THAT_ARENT_OCCUPATIONS,
	RO_YEARS
} from '$lib/constants';

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
		if (run.result != 'DEFEATED') {
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
		if (
			(closest && difference < closestDifference) ||
			(!closest && difference > closestDifference)
		) {
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
	return votesByParty;
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
		if (run.result != 'DEFEATED') {
			seatCounts[run.party] += 1;
		}
	}
	return Object.entries(seatCounts)
		.sort((a, b) => b[1] - a[1])
		.slice(0, n);
}

export function getElectionCandidatesByGender(electionId) {
	let candidatesByGender = {
		MALE: 0,
		FEMALE: 0,
		OTHER: 0,
		UNKNOWN: 0
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
		MALE: 0,
		FEMALE: 0,
		OTHER: 0,
		UNKNOWN: 0
	};
	for (const runId of elections[electionId].runs) {
		const run = runs[runId];
		if (run.result != 'DEFEATED') {
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
		if (run.party == partyId && run.result != 'DEFEATED') {
			count += 1;
		}
	}
	return count;
}

export function getMostRecentGeneralElectionId() {
	let mostRecentId = null;
	let mostRecentYear = 0;
	for (const [electionId, election] of Object.entries(elections)) {
		if (election.date.year > mostRecentYear && election.type == 'GENERAL') {
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
	// TODO: Fix this function.
	const electionId = getMostRecentGeneralElectionId();
	const generalElectionDate = elections[electionId].date;
	let heldRidings = new Set();
	for (const runId of elections[electionId].runs) {
		const run = runs[runId];
		if (run.party == partyId && run.result != 'DEFEATED') {
			heldRidings.add(run.riding);
		}
	}

	for (const [electionId, election] of Object.entries(elections)) {
		if (dateLaterThan(election.date, generalElectionDate) && election.type == 'BYELECTION') {
			for (const runId of election.runs) {
				const run = runs[runId];
				if (run.party != partyId) {
					continue;
				}
				if (run.result != 'DEFEATED') {
					heldRidings.add(run.riding);
				} else if (heldRidings.has(run.riding)) {
					heldRidings.delete(run.riding);
				}
			}
		}
	}

	return heldRidings.size;
}

export function getPartyPopularVoteByElection(partyId) {
	let ret = {};
	for (const [electionId, election] of Object.entries(elections)) {
		if (election.type != 'GENERAL') {
			continue;
		}
		let votes = 0;
		for (const runId of elections[electionId].runs) {
			const run = runs[runId];
			if (run.party != partyId) {
				continue;
			}
			votes += run.votes;
		}
		if (votes > 0) {
			ret[electionId] = votes;
		}
	}
	return ret;
}

export function getLifetimeNumberOfCandidates(partyId) {
	let candidates = new Set();
	for (const [runId, run] of Object.entries(runs)) {
		if (run.party == partyId) {
			candidates.add(run.candidate);
		}
	}
	return candidates.size;
}

export function getPartySeatsByElection(partyId) {
	let ret = {};
	for (const [electionId, election] of Object.entries(elections)) {
		if (election.type != 'GENERAL') {
			continue;
		}

		let seats = 0;
		for (const runId of elections[electionId].runs) {
			const run = runs[runId];
			if (run.party == partyId && run.result != 'DEFEATED') {
				seats += 1;
			}
		}
		if (seats > 0) {
			ret[electionId] = seats;
		}
	}
	return ret;
}

export function getPreviousGeneralElection(electionId) {
	let previousElectionId = null;
	let previousElectionDate = null;
	const thisElectionDate = elections[electionId].date;
	for (const [id, election] of Object.entries(elections)) {
		if (
			dateLaterThan(thisElectionDate, election.date) &&
			(previousElectionDate === null || dateLaterThan(election.date, previousElectionDate)) &&
			election.type == 'GENERAL'
		) {
			previousElectionId = id;
			previousElectionDate = election.date;
		}
	}
	return previousElectionId;
}

export function getPopularVoteSwingsFromPreviousElection(electionId, previousElectionId) {
	if (previousElectionId === null) {
		return {};
	}
	let swings = {};
	const votesByParty = getVotesByParty(electionId);
	const previousVotesByParty = getVotesByParty(previousElectionId);
	for (const [partyId, votes] of Object.entries(votesByParty)) {
		const previousVotes = previousVotesByParty[partyId];
		if (previousVotes === undefined) {
			continue;
		}
		swings[partyId] = votes - previousVotes;
	}

	return swings;
}

export function getPartyFromCandidateAndParliament(candidateId, parliamentId) {
	for (const [electionId, election] of Object.entries(elections)) {
		if (election.parliament == parliaments[parliamentId].number) {
			for (const runId of election.runs) {
				const run = runs[runId];
				if (run.candidate == candidateId) {
					return run.party;
				}
			}
		}
	}
	return null;
}

export function getByelectionsFromParliament(parliamentId) {
	let byelections = [];
	for (const [electionId, election] of Object.entries(elections)) {
		if (election.type == 'BYELECTION' && election.parliament == parliaments[parliamentId].number) {
			byelections.push(electionId);
		}
	}
	return byelections;
}

export function getGeneralElectionFromParliament(parliamentId) {
	for (const [electionId, election] of Object.entries(elections)) {
		if (election.type == 'GENERAL' && election.parliament == parliaments[parliamentId].number) {
			return electionId;
		}
	}
	return null;
}

export function getGeneralElectionVictor(electionId) {
	let results = {};
	for (const runId of elections[electionId].runs) {
		const run = runs[runId];
		if (run.result != 'DEFEATED') {
			if (run.party in results) {
				results[run.party] += 1;
			} else {
				results[run.party] = 1;
			}
		}
	}
	let winner = null;
	let winnerCount = 0;
	for (const [party, count] of Object.entries(results)) {
		if (count > winnerCount) {
			winner = party;
			winnerCount = count;
		}
	}
	return winner;
}

export function getSeatsInElection(electionId) {
	let seats = 0;
	for (const runId of elections[electionId].runs) {
		const run = runs[runId];
		if (run.result != 'DEFEATED') {
			seats += 1;
		}
	}
	return seats;
}

export function getElectionGeographyForView(electionId, viewId) {
	let ret = [];
	const election = elections[electionId];
	const view = detailViews[viewId];
	const ro_year = RO_YEARS.filter((y) => election.date.year >= y).slice(-1)[0];
	for (const runId of election.runs) {
		const run = runs[runId];
		const riding = ridings[run.riding];
		if (
			view != undefined &&
			(!(ro_year in view.ridings_by_year) || !view.ridings_by_year[ro_year].includes(run.riding))
		) {
			continue;
		}
		const geometryId = riding.geometry_by_year[ro_year];
		const geometry = geometries[geometryId];
		if (run.result != 'DEFEATED') {
			ret.push({
				...geometry,
				...run,
				runId: runId,
				geometryId: geometryId
			});
		}
	}
	return ret;
}

export function getSortedElectionRidingRuns(electionId, ridingId) {
	let ret = [];
	for (const runId of elections[electionId].runs) {
		const run = runs[runId];
		if (run.riding == ridingId) {
			ret.push(run);
		}
	}
	ret.sort((a, b) => b.votes - a.votes);
	return ret;
}
