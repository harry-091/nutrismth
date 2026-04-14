const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

export function fetchSections() {
  return request("/content/sections");
}

export function fetchModelMetrics() {
  return request("/model/metrics");
}

export function submitAssessment(payload) {
  return request("/assessment", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchRecommendations(payload) {
  return request("/recommendations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function optimizePlate(payload) {
  return request("/plate/optimize", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
