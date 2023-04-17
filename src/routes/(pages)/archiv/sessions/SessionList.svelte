<script>
	import dayjs from 'dayjs';
	import 'dayjs/locale/de';
	import SessionItem from './SessionItem.svelte';

	export let yearAndMonth;
	export let sessions;

	let year = dayjs(yearAndMonth).format('YYYY');
	let month = dayjs(yearAndMonth).locale('de').format('MMMM');
</script>

<h3>{month} <small class="text-muted">{year}</small></h3>
<ol>
	{#each sessions as session}
		<SessionItem {session} />
	{/each}
</ol>
