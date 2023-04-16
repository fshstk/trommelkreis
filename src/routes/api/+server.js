import { json } from '@sveltejs/kit';
import moment from 'moment';
import prisma from './prismaclient';
import { groupBy, orderBy } from 'lodash';

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
		date: moment(session.date).format('YYYY-MM-DD'),
		num_entries: fileCount,
		challenge: {
			name: challenge.name,
			blurb: challenge.blurb
		}
	};
}

export async function GET() {
	let sessions = await prisma.archive_session.findMany();
	let sorted = orderBy(sessions, (session) => moment(session.date).format('YYYY-MM-DD'), ['desc']);
	let formatted = await Promise.all(sorted.map(formatSession));
	let grouped = groupBy(formatted, (session) => moment(session.date).format('YYYY-MM'));
	console.log(grouped);
	return json(grouped);
}
