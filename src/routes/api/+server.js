import { json } from '@sveltejs/kit';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function GET() {
	let numSessions = await prisma.archive_session.count();
	return json(numSessions);
}
