import { json } from '@sveltejs/kit';
import prisma from '$lib/server/prismaclient';
import { groupBy, orderBy } from 'lodash';
import dayjs from 'dayjs';

async function formatSession(session) {
	let challenge = await prisma.archive_challenge.findUnique({
		where: {
			id: session.challenge_id
		}
	});

	let fileCount = await prisma.archive_audiofile.count({
		where: {
			session_id: session.id
		}
	});

	return {
		slug: session.slug,
		date: dayjs(session.date).format('YYYY-MM-DD'),
		num_entries: fileCount,
		challenge: {
			name: challenge.name,
			blurb: challenge.blurb
		}
	};
}

export async function GET() {
	let sessions = await prisma.archive_session.findMany();
	let sorted = orderBy(sessions, 'date', ['desc']);
	let formatted = await Promise.all(sorted.map(formatSession));
	let grouped = groupBy(formatted, (session) => dayjs(session.date).format('YYYY-MM'));
	return json(grouped);
}
