<script>
    export let value, valid=true, placeholder;
</script>

<input
    class={`rounded-lg w-48 text-sm px-3 py-[1px] bg-sol-light2 dark:bg-sol-dark2 border-2 border-opacity-0 border-sol-red outline-none ${valid ? "" : "border-opacity-100"}`}
    type="text"
    placeholder={placeholder}
    bind:value={value}
/>
