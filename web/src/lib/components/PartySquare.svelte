<script>
    import { FILL_COLOURS } from '$lib/constants.js';
    import parties from '$lib/artifacts/party.json';

    export let partyId;
</script>

{#if partyId}
    <div class={`h-3 w-3 rounded mr-2 ${FILL_COLOURS[parties[partyId].color]}`}/>
{/if}
