<script>
    import ridings from '$lib/artifacts/riding.json';

    export let title, subtitle, link;
    //{@html ridings["Qlzj_gyOi3"].geometry["2013"]}
</script>

<div class="flex flex-row w-full">
    <a href={link} class="rounded-lg bg-sol-light2 grow flex flex-col p-4 m-4 text-left space-y-1">
        <div class="flex flex-row items-center justify-center bg-sol-light3 rounded w-full h-48 opacity-80 mb-2 p-2">
            <slot />
        </div>
        <p class="text-xl font-black">
            {title}
        </p>
        <p class="text-sm text-sol-dark0">
            {subtitle}
        </p>
    </a>
</div>
