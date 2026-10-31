export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function createVideoJob(payload: {
  prompt: string;
  style: string;
  duration: number;
  language: string;
}) {
  const res = await fetch(`${API_URL}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error('Failed to create job');
  }

  return res.json();
}

export async function getJobs() {
  const res = await fetch(`${API_URL}/api/jobs`);
  if (!res.ok) {
    throw new Error('Failed to fetch jobs');
  }
  return res.json();
}
