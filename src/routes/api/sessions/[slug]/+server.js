import { json } from '@sveltejs/kit';
import prisma from '$lib/server/prismaclient';
import dayjs from 'dayjs';

async function formatFile(file) {
	let artist = await prisma.archive_artist.findUnique({
		where: {
			id: file.artist_id
		}
	});

	return {
		name: file.name,
		url: file.data,
		artist: artist.name
	};
}

async function formatSession(session) {
	let challenge = await prisma.archive_challenge.findUnique({
		where: {
			id: session.challenge_id
		}
	});

	let files = await prisma.archive_audiofile.findMany({
		where: {
			session_id: session.id
		}
	});

	return {
		date: dayjs(session.date).format('YYYY-MM-DD'),
		slug: session.slug,
		challenge: {
			name: challenge.name,
			blurb: challenge.blurb,
			description: challenge.description
		},
		files: await Promise.all(files.map(formatFile))
	};
}

export async function GET({ params }) {
	let session = await prisma.archive_session.findUnique({
		where: {
			slug: params.slug
		}
	});

	if (!session) return json(null);

	let formatted = await formatSession(session);
	return json(formatted);
}
