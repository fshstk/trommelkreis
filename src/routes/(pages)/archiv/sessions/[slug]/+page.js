import { error } from '@sveltejs/kit';
import dayjs from 'dayjs';
import showdown from 'showdown';

export async function load({ fetch, params }) {
	async function getSession(slug) {
		const response = await fetch(`/api/sessions/${slug}`);
		return await response.json();
	}

	let session = await getSession(params.slug);
	if (!session) {
		throw error(404, {
			message: 'Diese Session existiert nicht.'
		});
	}

	let converter = new showdown.Converter();
	let description = converter.makeHtml(session.challenge.description);
	let date = dayjs(session.date).format('DD.MM.YYYY');

	return {
		title: `Challenge vom ${date}`,
		heading: session.challenge.name,
		subHeading: dayjs(session.date).format('DD.MM.YYYY'),
		session: session,
		description: description
	};
}
