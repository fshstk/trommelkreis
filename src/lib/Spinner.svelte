<script>
	export let text = 'Bitte warten…';
</script>

<div class="text-center">
	<div class="spinner" />
	<p class="text-muted">{text}</p>
</div>

<style lang="scss">
	$spinner-color: $text-muted;
	$spinner-size: 50px;

	.spinner {
		display: inline-block;
		width: 80px;
		height: 80px;
	}

	.spinner:after {
		content: ' ';
		display: block;
		width: $spinner-size;
		height: $spinner-size;
		margin: 8px;
		border-radius: 50%;
		border: 6px solid $spinner-color;
		border-color: $spinner-color transparent $spinner-color transparent;
		animation: spinner-animation 2s linear infinite;
	}

	@keyframes spinner-animation {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
