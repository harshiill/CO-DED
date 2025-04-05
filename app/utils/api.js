const API_BASE_URL = 'http://127.0.0.1:5000';

export async function analyzeSEO(url) {
  const res = await fetch(`${API_BASE_URL}/seo?url=${encodeURIComponent(url)}`);
  const data = await res.json();
  return data;
}

export async function scrapeWebsite(url) {
  const res = await fetch(`${API_BASE_URL}/scrape?url=${encodeURIComponent(url)}`);
  const data = await res.json();
  return data;
}

export async function updateContent(url) {
  const res = await fetch(`${API_BASE_URL}/update?url=${encodeURIComponent(url)}`);
  const data = await res.json();
  return data;
}

export async function addContent(url) {
  const res = await fetch(`${API_BASE_URL}/add?url=${encodeURIComponent(url)}`);
  const data = await res.json();
  return data;
}

export async function getErrorLinks(url) {
  const res = await fetch(`${API_BASE_URL}/errorlink?url=${encodeURIComponent(url)}`);
  const data = await res.json();
  return data;
}

export async function setupAider(workingDir) {
  const res = await fetch(`${API_BASE_URL}/setup-aider`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ workingDir })
  });
  const data = await res.json();
  return data;
}