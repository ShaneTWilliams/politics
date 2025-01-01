<script>
	import Page from '$lib/components/Page.svelte';

	import headshot from '$lib/static/headshot.jpg';
	import Link from '$lib/components/Link.svelte';
</script>

<svelte:head>
	<title>About Shane Williams</title>
</svelte:head>

<Page>
	<div class="flex flex-col space-y-4 mt-12">
		<p class="font-bold text-3xl mb-4">About Me</p>
		<div class="flex flex-col items-center sm:items-start space-x-0 space-y-8 sm:space-y-0 sm:flex-row sm:space-x-12">
			<div class="flex flex-col grow text- space-y-4 text-sm">
				<p>I'm a firmware developer from St. John's, Newfoundland, with a keen interest in Newfoundland and Labrador provincial and Canadian federal politics.</p>
				<p>I plan to use this site to publish small political data analysis/visualization projects, starting with my <Link link="/elections">Federal Elections Visualizer</Link>. Over time, I hope to add more interactive data analysis projects and blog posts.</p>
				<p>All data and source code used in my analysis is published on this site's <Link link="https://github.com/ShaneTWilliams/site">GitHub repository</Link>.</p>
				<p>For feedback or corrections please email <Link link="mailto:shanethomaswilliams@gmail.com">shanethomaswilliams@gmail.com</Link></p>
			</div>
			<img src={headshot} alt="" class="w-72 h-72 rounded-md" />
		</div>
	</div>
</Page>
