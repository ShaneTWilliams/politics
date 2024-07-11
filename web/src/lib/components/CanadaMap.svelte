<script>
    import Map from "./Map.svelte"

    const RO_YEARS = [
        1867,
        1872,
        1882,
        1892,
        1903,
        1905,
        1914,
        1924,
        1933,
        1947,
        1952,
        1966,
        1976,
        1987,
        1996,
        1999,
        2003,
        2013
    ]

    export let selectedRiding, electionId, hoveredParty;
    let hoveredRiding = null;
</script>

<div>
    <div>
        <Map
            bind:selectedRiding={selectedRiding} bind:hoveredRiding={hoveredRiding} {electionId} {hoveredParty}
            view={null}
        />
    </div>
    <div class="flex flex-row">
    </div>
</div>
