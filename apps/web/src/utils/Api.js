import axios from 'axios'

export const API_URL = process.env.REACT_APP_API_URL

const API = axios.create({
  withCredentials: false,
  baseURL: API_URL,
})
// API.interceptors.request.use((config) => {
//   config.headers.Authorization = `Bearer ${localStorage.getItem('accessToken')}`
//   return config
// })
// API.interceptors.response.use(
//   (config) => {
//     return config
//   },
//   async (error) => {
//     const originalRequest = error.config
//     if (error.response.status === 401 && error.config && !error.config._isRetry) {
//       originalRequest._isRetry = true
//       try {
//         console.log('refresh token get')
//         const refresh = localStorage.getItem('refreshToken')
//         const response = await axios.post(`${API_URL}auth/update_token/`, { refresh })
//         localStorage.setItem('accessToken', response.data.access)
//         return API.request(originalRequest)
//       } catch (e) {
//         console.log('Not Auth')
//       }
//     }
//     throw error
//   },
// )

export default API
