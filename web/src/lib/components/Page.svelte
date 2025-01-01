<script>
	import Link from '$lib/components/Link.svelte';

	import HamburgerMenu from '~icons/mdi/hamburger-menu';
	import toast, { Toaster } from 'svelte-french-toast';

	const TAILWIND_FONT_STR = "font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;";
	const COMMON_STYLE_STRING = "border: none; font-size: 0.875rem; line-height: 1.25rem;" + TAILWIND_FONT_STR;
	const copyEmail = () => {
		let styleString = COMMON_STYLE_STRING;
		if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
			styleString += "color: #eee8d5; background-color: #073642;";
		} else {
			styleString += "color: #073642; background-color: #eee8d5;";
		}
		navigator.clipboard.writeText("shanethomaswilliams@gmail.com").then(
			() => {
				toast.success("Email copied to clipboard", {
					position: "bottom-right",
					style: styleString,
					iconTheme: {
						primary: '#859900',
						secondary: '#fdf6e3'
					}
				});
			}
		)
	};


	let hamburgerOpen = false;
</script>

<div class="w-screen flex flex-col items-center min-h-screen bg-sol-light3 dark:bg-sol-dark3 font-mono">
	<div class="bg-sol-light3/80 dark:bg-sol-dark3/80 w-full flex flex-row py-1 items-center sticky top-0 border-b dark:border-sol-dark2 z-40 backdrop-blur-sm">
		<div class="ml-4 flex flex-row items-center grow justify-center md:justify-start">
			<div class="md:hidden w-8 h-4" />
			<div class="grow md:flex-initial flex flex-row items-center justify-center">
				<a
					href="/"
					class="flex flex-row flex-initial h-8 md:h-14 hover:cursor-pointer sm:py-2 sm:px-3 hover:bg-sol-light2 dark:hover:bg-sol-dark2 rounded-lg border-transparent group items-center"
				>
					<div class="flex-row space-x-1 items-end h-full hidden md:flex">
						<div class="bg-sol-green w-4 h-8 hover:h-10" />
						<div class="bg-sol-red w-4 h-4 hover:h-6" />
						<div class="bg-sol-cyan w-4 h-6 hover:h-8" />
					</div>
					<div
						class="flex flex-row md:flex-col font-black text-sol-dark3 dark:text-sol-light3 text-lg md:space-y-1 mx-3 leading-none space-x-2 md:space-x-0"
					>
						<p>Shane</p>
						<p>Williams</p>
					</div>
				</a>
			</div>
			<div
				class="grow flex flex-row space-x-4 justify-center items-center grow font-semibold text-sol-dark3 dark:text-sol-light3 hover:pointer-cursor hidden md:flex"
			>
				<a
					href="/elections"
					class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dotted p-4"
				>
					Elections
				</a>
				<a
					href="/blog"
					class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dotted p-4"
				>
					Blog
				</a>
				<a
					href="/about"
					class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dotted p-4"
				>
					About
				</a>
			</div>
			<div class="flex-initial w-56 hidden md:flex" />
			<div
				class="md:hidden w-8 h-8 rounded hover:bg-sol-light2 dark:hover:bg-sol-dark2 text-lg mr-4"
			>
				<button
					class="flex flex-row items-center justify-center w-full h-full hover:cursor-pointer text-sol-dark2 dark:text-sol-light2"
					on:click={() => {
						hamburgerOpen = !hamburgerOpen;
					}}
					on:keydown={(e) => {
						if (e.key === 'Escape') {
							hamburgerOpen = false;
						}
					}}
				>
					<HamburgerMenu />
				</button>
			</div>
		</div>
	</div>
	<div class="w-full relative text-left hover:cursor-default grow">
		<div class="w-full flex flex-col items-center text-sol-dark3 dark:text-sol-light3 pb-24 px-6 sm:px-12 md:px-24">
			<div class="max-w-md sm:max-w-4xl w-full text-sol-dark3 dark:text-sol-light3">
				<slot />
			</div>
		</div>
		{#if hamburgerOpen}
			<button
				class="w-screen h-screen fixed top-0 left-0 hover:cursor-default"
				on:click={() => {
					hamburgerOpen = false;
				}}
			/>
			<button
				class="flex flex-col fixed border border-sol-light1 dark:border-sol-dark2 top-12 right-2 bg-sol-light3/60 dark:bg-sol-dark3/60 backdrop-blur-sm px-4 py-2 rounded-lg text-lg font-bold text-sol-dark2 dark:text-sol-light2 hover:cursor-default"
				on:click={() => {
					hamburgerOpen = false;
				}}
			>
				<a
					href="/elections"
					class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dotted p-2 hover:cursor-pointer"
				>
					Elections
				</a>
				<a
					href="/blog"
					class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dotted p-2 hover:cursor-pointer"
				>
					Blog
				</a>
				<a
					href="/about"
					class="hover:text-sol-dark1 dark:hover:text-sol-light2 hover:underline decoration-dotted p-2 hover:cursor-pointer"
				>
					About
				</a>
			</button>
		{/if}
	</div>
	<div class="w-full py-6 flex flex-row justify-center items-center text-sol-dark3 dark:text-sol-light3 text-xs">
		<div class="flex flex-row space-x-8">
			<a class="hover:underline decoration-dotted" href="https://github.com/ShaneTWilliams/site">Source</a>
			<a class="hover:underline decoration-dotted" href="/about">About</a>
			<button
				class="hover:underline hover:cursor-pointer decoration-dotted"
				on:click={copyEmail}
			>
				Contact
			</button>
		</div>
	</div>
</div>
<Toaster />
