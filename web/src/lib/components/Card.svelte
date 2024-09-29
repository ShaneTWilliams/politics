<script>
    import ridings from '$lib/artifacts/riding.json';

    export let title, subtitle, link;
</script>

<div class="flex flex-row w-full">
    <a href={link} class="rounded-lg bg-sol-light2 dark:bg-sol-dark2 grow flex flex-col py-4 px-6 text-left space-y-1 border border-dashed hover:border-sol-dark2 hover:dark:border-sol-light1 border-transparent">
        <div class="flex flex-row items-center justify-center rounded w-full h-48">
            <slot />
        </div>
        <p class="text-xl font-black text-sol-dark3 dark:text-sol-light3">
            {title}
        </p>
        <p class="text-sm text-sol-light1 dark:text-sol-light1">
            {subtitle}
        </p>
    </a>
</div>
