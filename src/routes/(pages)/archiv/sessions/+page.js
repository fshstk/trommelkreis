export async function load({ fetch }) {
	async function getSessions() {
		const response = await fetch('/api/sessions/all');
		return await response.json();
	}

	return {
		title: 'Sessions',
		heading: 'Archiv',
		subHeading: 'des digitalen Trommelkreises',
		sessions: await getSessions()
	};
}
