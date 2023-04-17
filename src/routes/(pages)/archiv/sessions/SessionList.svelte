<script>
	import dayjs from 'dayjs';
	import 'dayjs/locale/de';
	import SessionItem from './SessionItem.svelte';
	import { orderBy } from 'lodash';

	export let yearAndMonth;
	export let sessions;

	let year = dayjs(yearAndMonth).format('YYYY');
	let month = dayjs(yearAndMonth).locale('de').format('MMMM');

	let sorted = orderBy(sessions, 'date', ['asc']);

	let leftCol = sorted.slice(0, Math.ceil(sorted.length / 2));
	let rightCol = sorted.slice(Math.ceil(sorted.length / 2));
</script>

<h3>{month} <small class="text-muted">{year}</small></h3>

<div class="row">
	<div class="col-md-6">
		<div class="list-group text-left">
			{#each leftCol as session}
				<SessionItem {session} />
			{/each}
		</div>
	</div>

	<div class="col-md-6">
		<div class="list-group text-left">
			{#each rightCol as session}
				<SessionItem {session} />
			{/each}
		</div>
	</div>
</div>

<hr />
