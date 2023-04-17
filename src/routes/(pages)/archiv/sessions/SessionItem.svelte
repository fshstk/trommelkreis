<script>
	import dayjs from 'dayjs';
	import 'dayjs/locale/de';

	export let session;

	let date = dayjs(session.date).format('DD.MM.YYYY');
	let showItem = session.num_entries > 0;

	function numFiles(session) {
		if (session.num_entries === 0) return 'Keine Einträge';
		if (session.num_entries === 1) return '1 Eintrag';
		return `${session.num_entries} Einträge`;
	}
</script>

{#if showItem}
	<a href="/archiv/sessions/{session.slug}" class="list-group-item list-group-item-action">
		<div class="d-flex justify-content-between">
			<h5 class="mb-1 text-truncate">{session.challenge.name}</h5>
			<small class="text-muted">{date}</small>
		</div>
		<p style="height: 20px;" class="mb-1 text-truncate">{session.challenge.blurb}</p>
		<div class="d-flex justify-content-between">
			<small class="text-muted">{numFiles(session)}</small>
			<!-- 
    {#if session.copyright_issues}
			<small><i class="fa-solid fa-lock" /></small>
		{/if}
    -->
		</div>
	</a>
{/if}
