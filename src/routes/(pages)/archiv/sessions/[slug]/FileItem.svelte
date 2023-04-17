<script>
	export let file;
</script>

<a href="#" class="list-group-item disabled bg-secondary">
	<div class="d-flex justify-content-between">
		<h5 class="mb-1 text-truncate text-white">{file.name}</h5>
	</div>
	<div class="d-flex justify-content-between">
		<p class="mb-1 text-truncate text-white">{file.artist ? file.artist : '(Anonym)'}</p>
		<small class="text-warning">verloren</small>
	</div>
</a>
