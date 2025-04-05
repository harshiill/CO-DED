const API_BASE_URL = 'http://127.0.0.1:5000';

const handleResponse = async (res) => {
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || 'API error');
    }
    return res.json();
  };

// export const createUser = async (userData) => {
//     const res = await fetch(`${BASE_URL}/users/`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(userData),
//     });
//     return handleResponse(res);
//   };
  
// export const getUserById = async (id) => {
//     const res = await fetch(`${BASE_URL}/users/${id}`);
//     return handleResponse(res);
// };

export const getLLMCompletion = async (prompt) => {
    const res = await fetch(`${BASE_URL}/v1/completions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
    });
    return handleResponse(res);
};

export const scrapeWebsite = async (url) => {
    const res = await fetch(`${BASE_URL}/scraped-data?url=${encodeURIComponent(url)}`);
    return handleResponse(res);
};

export const updateWebsiteContent = async (url) => {
    const res = await fetch(`${BASE_URL}/update-content?url=${encodeURIComponent(url)}`);
    return handleResponse(res);
};

export const checkBrokenLinks = async (url) => {
    const res = await fetch(`${BASE_URL}/errorlink?url=${encodeURIComponent(url)}`);
    return handleResponse(res);
};

export const analyzeSEO = async (url) => {
    const res = await fetch(`${BASE_URL}/seo?url=${encodeURIComponent(url)}`);
    return handleResponse(res);
};

export const clearCache = async () => {
    const res = await fetch(`${BASE_URL}/clear-cache`, { method: 'DELETE' });
    return handleResponse(res);
};

export const runAiderUpdate = async (workingDir) => {
    const res = await fetch(`${BASE_URL}/setup-aider`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workingDir }),
    });
    return handleResponse(res);
};

export const connectToServer = async () => {
    const res = await fetch(`${BASE_URL}/v1/connect`);
    return handleResponse(res);
};