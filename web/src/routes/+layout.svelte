<script>
    import "../app.css";
    import favicon from "$lib/static/favicon.svg";
</script>

<svelte:head>
  <link rel="icon" type="image/svg" href={favicon} />
</svelte:head>

<slot />
