<script>
    import ridings from '$lib/artifacts/riding.json';

    export let title, subtitle, link;
</script>

<div class="flex flex-row w-full">
    <a href={link} class="border grow flex flex-col p-2 m-4 text-left space-y-1 hover:bg-sol-light2 group">
        <div class="bg-sol-light2 w-full h-48 opacity-80 mb-2 group-hover:bg-sol-light3">
            <svg
                xmlns='http://www.w3.org/2000/svg'
                viewBox="7000000, -3100000, 2000000, 2000000"
            >
                <g transform='scale(1,-1)'>
                    <g class="fill-sol-light1">
                        {@html ridings["Qlzj_gyOi3"].geometry["2013"]}
                    </g>
                </g>
            </svg>
        </div>
        <p class="text-xl font-black">
            {title}
        </p>
        <p class="text-sm text-sol-dark0">
            {subtitle}
        </p>
    </a>
</div>
