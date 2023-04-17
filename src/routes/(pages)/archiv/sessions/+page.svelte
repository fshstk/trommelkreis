<script>
	import SessionList from './SessionList.svelte';
	import Spinner from '$lib/Spinner.svelte';

	async function getSessions() {
		const response = await fetch('/api');
		return await response.json();
	}

	let sessions = getSessions();
</script>

{#await sessions}
	<div class="text-center">
		<Spinner />
		<p class="text-muted">Sessions werden geladen…</p>
	</div>
{:then result}
	{#each Object.entries(result) as [yearAndMonth, sessions]}
		<SessionList {yearAndMonth} {sessions} />
	{/each}
{:catch error}
	<div class="text-center text-danger">
		<i class="fa-solid fa-exclamation-triangle display-4" />
		<p class="pt-3">
			Oje, da ist etwas schiefgelaufen. Bitte schicke diese Fehlernachricht an
			mitmachen@trommelkreis.club:
		</p>
		<pre><code>{error.message}</code></pre>
	</div>
{/await}
