import axios from 'axios'

const instance = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
    withCredentials: true
})

instance.interceptors.response.use(undefined, (error) => {
    if (error.response) return error.response
});

export const authAPI = {
    login(email: string, password: string) {
        return instance.post('auth/login/', {email, password});
    },
    register(email: string, username: string, password: string) {
        return instance.post('auth/register/', {email, username, password});
    }
}