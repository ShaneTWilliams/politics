<script>
    import Page from '$lib/components/Page.svelte';

    import candidates from '$lib/artifacts/candidate.json';

    const firstNameFrequencies = {};
    const lastNameFrequencies = {};
    for (const [candidateId, candidate] of Object.entries(candidates)) {
        if (firstNameFrequencies[candidate.first_name] === undefined) {
            firstNameFrequencies[candidate.first_name] = 0;
        }
        firstNameFrequencies[candidate.first_name] += 1;

        if (lastNameFrequencies[candidate.last_name] === undefined) {
            lastNameFrequencies[candidate.last_name] = 0;
        }
        lastNameFrequencies[candidate.last_name] += 1;
    }
</script>

<Page>
    {#each Object.entries(firstNameFrequencies).sort((a, b) => b[1] - a[1]) as [name, count]}
        {#if name !== "" && count > 50}
            <p>{name}: {count}</p>
        {/if}
    {/each}
    {#each Object.entries(lastNameFrequencies).sort((a, b) => b[1] - a[1]) as [name, count]}
        {#if name !== "" && count > 50}
            <p>{name}: {count}</p>
        {/if}
    {/each}
</Page>
