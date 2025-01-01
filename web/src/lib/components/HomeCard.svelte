<script>
    import Button from '$lib/components/Button.svelte';

    export let link, title, buttonText;
</script>

<div class="w-full mt-6 p-6 bg-sol-light2 dark:bg-sol-dark2 rounded-xl flex flex-col items-left">
    <div class="w-full flex flex-row justify-center">
        <slot />
    </div>
    <div class="flex flex-col sm:ml-4">
        <div class="text-left text-lg sm:text-2xl font-bold">{title}</div>
        <div class="w-min mt-3">
            <Button {link} text={buttonText} />
        </div>
    </div>
</div>
