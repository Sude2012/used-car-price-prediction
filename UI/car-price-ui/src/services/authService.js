

import api from "./api";

export const registerUser = (data) => {
    return api.post("/Auth/register", data);
};

export const loginUser = (data) => {
    return api.post("/Auth/login", data);
};



