<script>
    import PartySquare from "$lib/components/PartySquare.svelte";

    export let data;
</script>

<div class="rounded-lg bg-sol-light2 dark:bg-sol-dark2 py-3 px-5 text-sm mb-2 space-y-1 overflow-scroll sm:w-min">
    <div class="w-min">
        {#each data as row}
        <div class="flex flex-row items-center">
            <PartySquare partyId={row.partyId}/>
            <a
                class="whitespace-nowrap font-bold hover:underline decoration-dashed text-xs sm:text-sm"
                href={row.link}
            >{row.label}</a>
        </div>
        {/each}
    </div>
</div>
