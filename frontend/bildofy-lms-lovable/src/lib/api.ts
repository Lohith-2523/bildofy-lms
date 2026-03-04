import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * Centralized Axios instance for ALL authenticated API calls
 */
export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: false,
});

/**
 * Attach JWT to every request automatically
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers = config.headers ?? {};
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * Optional: global response handler (future-proofing)
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn("JWT expired or invalid");
      // future: logout / refresh token
    }
    return Promise.reject(error);
  }
);
