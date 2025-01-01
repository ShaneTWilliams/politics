<script>
    export let link, text;
</script>

<a
    href={link}
    class="sm:text-lg text-sm font-bold flex flex-row items-center justify-center border border-sol-dark2 dark:border-sol-light2 px-3 py-2 sm:px-4 sm:py-2 border-2 rounded-lg sm:rounded-xl hover:bg-sol-dark2 dark:hover:bg-sol-light2 hover:text-sol-light3 dark:hover:text-sol-dark3"
>
    <p>{text}</p>
</a>
