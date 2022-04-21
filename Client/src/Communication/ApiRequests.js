import axios from 'axios'
import { baseURL } from '../Config/constants'
axios.defaults.withCredentials = true
export const registerUser = async (email, password) => {
  console.log('in apiRequests')
  const response = await axios.post(`${baseURL}/accounts/register_user`, {
    email: email,
    pwd: password
  })
  console.log('the response is: ', response.data)
  return response.data

  //   async delete({ id }) {
  //     return axios.delete(`${baseURL}/todos/${id}`)
  //   }

  //   async edit({ id, partialTodo }) {
  //     return axios.put(`${baseURL}/${id}`, {
  //       partialTodo: partialTodo
  //     })
  //   }

  //   async fetchAll() {
  //     return axios.get(`${baseURL}/todos`)
  //   }
}
