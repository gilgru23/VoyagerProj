import axios from 'axios'
import { baseURL, responseStatus } from '../Config/constants.js'
import Consumer from '../model/Consumer.js'
axios.defaults.withCredentials = true
export const registerUser = async (email, password) => {
  try {
    console.log('sending request')
    const response = await axios.post(`${baseURL}/accounts/register_user`, {
      email: email,
      pwd: password
    })
    if (response) {
      return responseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return responseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    console.log(e)
    return responseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}

const responseObj = (status, content) => ({
  status: status,
  content: content
})
