<script>
	import { page } from '$app/stores';
</script>

<main>
	<div class="row">
		<div class="col-6 my-auto text-right">
			<img src="/logo.png" width="300px" class="img-fluid float-end p-3" alt="logo" />
		</div>
		<div class="col-6 my-auto text-left">
			<h1 class="text-truncate">{$page.status} <i class="fas fa-face-frown-open" /></h1>
			<h6 class="text-muted">{$page.error.message}</h6>
		</div>
	</div>
</main>
