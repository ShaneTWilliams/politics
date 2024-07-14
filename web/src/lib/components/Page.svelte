<div class="w-screen flex flex-col items-center min-h-screen bg-sol-light3">
    <div class="bg-sol-light3 w-full flex flex-row py-1 items-center sticky top-0 shadow-md">
        <div class="ml-4 flex flex-row items-center grow">
            <a href="/" class="flex flex-row flex-initial w-48 h-14 hover:cursor-pointer p-2 hover:bg-sol-light2 rounded-lg border-transparent group mr-4 items-center">
                <div class="flex flex-row space-x-1 items-end h-full">
                    <div class="bg-sol-green w-4 h-8 group-hover:h-10"/>
                    <div class="bg-sol-red w-4 h-4 group-hover:h-10"/>
                    <div class="bg-sol-cyan w-4 h-6 group-hover:h-10"/>
                </div>
                <div class="flex flex-col font-black font-mono text-sol-dark3 text-xl ml-3 leading-none">
                    <p>
                        Shane
                    </p>
                    <p>
                        Williams
                    </p>
                </div>
            </a>
            <div class="grow flex flex-row space-x-4 justify-center items-center grow font-semibold text-sol-dark2 hover:pointer-cursor font-mono">
                <a href="/elections" class="hover:text-sol-dark1 hover:underline p-4">
                    Elections
                </a>
                <a href="/" class="hover:text-sol-dark1 hover:underline p-4">
                    Blog
                </a>
                <a href="/" class="hover:text-sol-dark1 hover:underline p-4">
                    About
                </a>
            </div>
            <div class="flex-initial w-64"/>
        </div>
    </div>
    <div class="max-w-screen-lg w-full flex flex-col items-left font-mono text-sol-dark3 pb-96 px-4">
        <slot/>
    </div>
</div>
