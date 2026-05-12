/**
 * Centralised API client.
 * All services talk through this module — auth, voters, elections, etc.
 */
import axios, { type AxiosRequestConfig, type AxiosResponse } from "axios";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

const client = axios.create({
  baseURL: BASE,
  headers: { "Content-Type": "application/json" },
});

/* ---------- Auth interceptors ---------- */
client.interceptors.request.use((config) => {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  config.headers["X-Correlation-ID"] = crypto.randomUUID();
  return config;
});

client.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401) {
      // Attempt silent refresh
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) throw new Error("No refresh token");
        const res = await axios.post(`${BASE}/login/refresh-token`, null, {
          params: { refresh_token: refreshToken },
        });
        localStorage.setItem("access_token", res.data.access_token);
        localStorage.setItem("refresh_token", res.data.refresh_token);
        // Retry original request
        error.config.headers.Authorization = `Bearer ${res.data.access_token}`;
        return client.request(error.config);
      } catch {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default client;
