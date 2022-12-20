import axios from 'axios'

const instance = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
    withCredentials: true
})

export const authAPI = {
    login(email: string, password: string) {
        return instance.post('auth/login/', {email, password});
    }
}