<script>
    import { page } from '$app/stores';

    import CharmSquareTick from '~icons/charm/square-tick'
    import CharmSquareCross from '~icons/charm/square-cross'

    import Page from '$lib/components/Page.svelte';
    import HorizontalBar from '$lib/components/HorizontalBar.svelte';
    import SmallStat from '$lib/components/SmallStat.svelte';
    import Title from '$lib/components/Title.svelte';
    import Subtitle from '$lib/components/Subtitle.svelte';
    import PartySquare from '$lib/components/PartySquare.svelte';

    import { getRunsInRiding } from '$lib/stats.js';
    import { formatString, formatNumber } from '$lib/utils.js';
    import { PARTIES, PROVINCES, ELECTION_TYPE, FILL_COLOURS } from '$lib/constants.js';

    import candidates from '$lib/artifacts/candidate.json';
    import runs from '$lib/artifacts/run.json';
    import ridings from '$lib/artifacts/riding.json';
    import parties from '$lib/artifacts/party.json';
    import elections from '$lib/artifacts/election.json';

    $: riding = ridings[$page.params.ridingId];

</script>

<svelte:head>
    <title>{formatString(riding.name)}</title>
</svelte:head>

<Page>
    <Title text={formatString(riding.name)} />
    <Subtitle text={PROVINCES[riding.province]} />
</Page>
