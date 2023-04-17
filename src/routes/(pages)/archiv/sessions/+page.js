async function getSessions() {
	const response = await fetch('/api');
	return await response.json();
}

export async function load() {
	return {
		title: 'Sessions',
		heading: 'Archiv',
		subHeading: 'des digitalen Trommelkreises',
		sessions: await getSessions()
	};
}
