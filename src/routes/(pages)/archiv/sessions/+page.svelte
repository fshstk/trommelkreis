<script>
	import SessionList from './SessionList.svelte';

	export let data;
</script>

{#each Object.entries(data.sessions) as [yearAndMonth, sessions]}
	<SessionList {yearAndMonth} {sessions} />
{/each}
