import elections_raw from '$lib/artifacts/election.json';
import runs_raw from '$lib/artifacts/run.json';
import ridings_raw from '$lib/artifacts/riding.json';
import candidates_raw from '$lib/artifacts/candidate.json';
import parties_raw from '$lib/artifacts/party.json';
import parliaments_raw from '$lib/artifacts/parliament.json';
import detailviews_raw from '$lib/artifacts/detailview.json';
import geometries_raw from '$lib/artifacts/geometry.json';

import elections_fields from '$lib/artifacts/election_fields.json';
import runs_fields from '$lib/artifacts/run_fields.json';
import ridings_fields from '$lib/artifacts/riding_fields.json';
import candidates_fields from '$lib/artifacts/candidate_fields.json';
import parties_fields from '$lib/artifacts/party_fields.json';
import parliaments_fields from '$lib/artifacts/parliament_fields.json';
import detailviews_fields from '$lib/artifacts/detailview_fields.json';
import geometries_fields from '$lib/artifacts/geometry_fields.json';

export function load_data(data, fields) {
    let ret = {};
    for (const [key, dataArr] of Object.entries(data)) {
        let item = {};
        for (let i = 0; i < fields.length; i++) {
            item[fields[i]] = dataArr[i];
        }
        ret[key] = item;
    }
    return ret;
}

export const elections = load_data(elections_raw, elections_fields);
export const runs = load_data(runs_raw, runs_fields);
export const ridings = load_data(ridings_raw, ridings_fields);
export const candidates = load_data(candidates_raw, candidates_fields);
export const parties = load_data(parties_raw, parties_fields);
export const parliaments = load_data(parliaments_raw, parliaments_fields);
export const detailViews = load_data(detailviews_raw, detailviews_fields);
export const geometries = load_data(geometries_raw, geometries_fields);
