<script>
	import dayjs from 'dayjs';
	import 'dayjs/locale/de';

	export let session;

	let date = dayjs(session.date).format('DD.MM.YYYY');
</script>

<li>{date} - {session.challenge.name} ({session.num_entries} Einträge)</li>
