<div class="bg-sol-light3 dark:bg-sol-dark3 py-4 pr-2 pl-4 space-y-2 rounded svg-shadow">
    {#each {length: 7} as _, i}
        <div class="flex flex-row space-x-1">
            <div class="bg-sol-light2 dark:bg-sol-dark2 w-16 h-3 rounded-sm flex flex-col">
                <div class="grow"/>
                <div class="grow flex flex-row border-b border-dotted border-sol-light3 dark:border-sol-dark3">
                    <div class="w-4 border-t border-dotted border-sol-light3 dark:border-sol-dark3"/>
                    <div class="grow border-t-4 border-dashed border-sol-light3 dark:border-sol-dark3"/>
                    <div class="w-4 border-t border-dotted border-sol-light3 dark:border-sol-dark3"/>
                </div>
                <div class="grow"/>
            </div>
            <div class="flex flex-row items-center justify-center bg-sol-light2 dark:bg-sol-dark2 rounded-full w-3 h-3 text-sm text-sol-red font-bold italic">
                {#if i === 2}
                    X
                {/if}
            </div>
        </div>
    {/each}
</div>
