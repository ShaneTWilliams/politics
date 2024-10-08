<div class="w-screen flex flex-col items-center min-h-screen bg-sol-light3 dark:bg-sol-dark3">
    <div class="bg-sol-light3 dark:bg-sol-dark3 w-full flex flex-row py-1 items-center sticky top-0 shadow-md dark:shadow-2xl z-40">
        <div class="ml-4 flex flex-row items-center grow">
            <a href="/" class="flex flex-row flex-initial h-14 hover:cursor-pointer hover:animate-pulse py-2 px-3 hover:bg-sol-light2 dark:hover:bg-sol-dark2 rounded-lg border-transparent group items-center">
                <div class="flex flex-row space-x-1 items-end h-full">
                    <div class="bg-sol-green w-4 h-8"/>
                    <div class="bg-sol-red w-4 h-4"/>
                    <div class="bg-sol-cyan w-4 h-6"/>
                </div>
                <div class="flex flex-col font-black font-mono text-sol-dark3 dark:text-sol-light3 text-xl ml-3 leading-none">
                    <p>
                        Shane
                    </p>
                    <p>
                        Williams
                    </p>
                </div>
            </a>
            <div class="grow flex flex-row space-x-4 justify-center items-center grow font-semibold text-sol-dark3 dark:text-sol-light3 hover:pointer-cursor font-mono">
                <a href="/elections" class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dashed p-4">
                    Elections
                </a>
                <a href="/blog" class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dashed p-4">
                    Blog
                </a>
                <a href="/about" class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dashed p-4">
                    About
                </a>
            </div>
            <div class="flex-initial w-56"/>
        </div>
    </div>
    <div class="w-full flex flex-col items-center font-mono text-sol-dark3 dark:text-sol-light3 pb-96 px-24">
        <div class="max-w-4xl w-full text-sol-dark3 dark:text-sol-light3">
            <slot/>
        </div>
    </div>
</div>
