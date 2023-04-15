<script>
	import '../app.scss';
	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>{$page.data.title} | Digitaler Trommelkreis</title>
</svelte:head>

<nav class="nav container p-1">
	<a class="nav-link text-dark" href="/" title="Home">
		<i class="fa-solid fa-house" />
	</a>
	<a class="nav-link text-dark" href="/info">Info</a>
	<a class="nav-link text-dark" href="/archiv">Archiv</a>
	<a class="nav-link text-primary" href="/upload">Mitmachen</a>
	<a class="nav-link text-dark ms-auto" href="/subscribe" title="Newsletter">
		<i class="fa-solid fa-envelope" />
	</a>
</nav>

<main class="container bg-white p-3">
	<slot />
</main>

<footer class="container text-center p-1 small text-dark">
	Impressum: &copy; 2023 Fabian Hummel |
	<a href="https://github.com/fshstk/trommelkreis">github.com/fshstk/trommelkreis</a>
</footer>
