<script>
	import SessionList from './SessionList.svelte';
	import ErrorMessage from '$lib/ErrorMessage.svelte';
	import Spinner from '$lib/Spinner.svelte';

	async function getSessions() {
		const response = await fetch('/api');
		return await response.json();
	}

	let sessions = getSessions();
</script>

{#await sessions}
	<Spinner text="Sessions werden geladen…" />
{:then result}
	{#each Object.entries(result) as [yearAndMonth, sessions]}
		<SessionList {yearAndMonth} {sessions} />
	{/each}
{:catch error}
	<ErrorMessage text={error.message} />
{/await}
