<script>
	import dayjs from 'dayjs';
	import 'dayjs/locale/de';

	function getMonth(date) {
		return dayjs(date).locale('de').format('MMMM');
	}

	function getYear(date) {
		return dayjs(date).format('YYYY');
	}

	function getDate(date) {
		return dayjs(date).format('DD.MM.YYYY');
	}

	async function getSessions() {
		const response = await fetch('/api');
		return await response.json();
	}

	let sessions = getSessions();
</script>

{#await sessions}
	<div class="text-center">
		<div class="spinner" />
		<p class="text-muted">Sessions werden geladen…</p>
	</div>
{:then result}
	<ol>
		{#each Object.entries(result) as [yearAndMonth, sessions]}
			<li>{getYear(yearAndMonth)} - {getMonth(yearAndMonth)}</li>
			{#each sessions as session}
				<li>{getDate(session.date)} - {session.challenge.name} ({session.num_entries} Einträge)</li>
			{/each}
		{/each}
	</ol>
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
