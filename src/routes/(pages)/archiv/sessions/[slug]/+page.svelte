<script>
	import FileItem from './FileItem.svelte';

	export let data;
</script>

<div class="card">
	<div class="card-body">
		{@html data.description}
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
