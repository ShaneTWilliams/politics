<script>
    import "../app.css";
    import favicon from "$static/favicon.svg";
</script>

<svelte:head>
  <link rel="icon" type="image/svg+xml" href={favicon} />
</svelte:head>

<slot />
