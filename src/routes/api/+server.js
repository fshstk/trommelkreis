import { json } from '@sveltejs/kit';
import moment from 'moment';
import prisma from './prismaclient';

moment.locale('de');

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
		date: moment(session.date).format('DD.MM.YYYY'),
		month: moment(session.date).format('MMMM'),
		year: moment(session.date).format('YYYY'),
		num_entries: fileCount,
		challenge: {
			name: challenge.name,
			blurb: challenge.blurb
		}
	};
}

export async function GET() {
	let allSessions = await prisma.archive_session.findMany();
	let parsedSessions = await Promise.all(allSessions.map(formatSession));

	console.log(parsedSessions[0]);

	return json(parsedSessions);
}
