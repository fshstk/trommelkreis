<script>
	import moment from 'moment';

	console.log(moment.locale('de'));

	function getMonth(date) {
		return moment(date).format('MMMM');
	}

	function getYear(date) {
		return moment(date).format('YYYY');
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
				<li>{session.date} - {session.challenge.name} ({session.num_entries} Einträge)</li>
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
