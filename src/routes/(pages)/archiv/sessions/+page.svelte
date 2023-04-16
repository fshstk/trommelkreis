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
	<p>Retrieved {result} sessions</p>
{:catch error}
	<p>We had an error: {error.message}</p>
{/await}
