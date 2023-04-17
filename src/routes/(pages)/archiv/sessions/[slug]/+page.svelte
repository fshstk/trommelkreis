<script>
	import showdown from 'showdown';
	import FileItem from './FileItem.svelte';

	export let data;

	let converter = new showdown.Converter();
	let description = converter.makeHtml(data.session.challenge.description);
</script>

<div class="card">
	<div class="card-body">
		{@html description}
	</div>
</div>

<hr />

<div class="list-group text-left">
	{#each data.session.files as file}
		<FileItem {file} />
	{/each}
</div>

<hr />

<div class="d-flex justify-content-between">
	<span>
		<a href="/archiv">Archiv</a> / <a href="/archiv/sessions">Sessions</a> / {data.session.slug}
	</span>
</div>
