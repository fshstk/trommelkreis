<script>
	async function getSessions() {
		const response = await fetch('/api');
		return await response.json();
	}

	let sessions = getSessions();
</script>

{#await sessions}
	<p>Retrieving sessions...</p>
{:then result}
	<ol>
		{#each result as session}
			<li>{session.date} - {session.challenge.name} ({session.num_entries} Einträge)</li>
		{/each}
	</ol>
{:catch error}
	<p>We had an error: {error.message}</p>
{/await}
