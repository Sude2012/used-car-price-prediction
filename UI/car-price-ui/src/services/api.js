


import axios from "axios";

const api = axios.create({
    baseURL: "https://localhost:7188/api",
    withCredentials: false
});

export default api;

