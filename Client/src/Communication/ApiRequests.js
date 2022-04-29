import axios from 'axios'
import { AppRegistry } from 'react-native'
import { baseURL, responseStatus } from '../Config/constants.js'
import Consumer from '../model/Consumer.js'
axios.defaults.withCredentials = true

export const registerUser = async (email, password, firstName, lastName) => {
  try {
    console.log('sending request')
    const response = await axios.post(`${baseURL}/accounts/register_user`, {
      email: email,
      pwd: password,
      firstName: firstName,
      lastName: lastName
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

export const createConsumerProfile = async (
  residence,
  height,
  weight,
  units,
  gender,
  goal
) => {
  try {
    console.log('sending request')
    const response = await axios.post(
      `${baseURL}/accounts/create_consumer_profile`,
      {
        residence,
        height,
        weight,
        units,
        gender,
        goal
      }
    )
    if (response) {
      return responseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return responseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    console.log(e)
    return responseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}

export const login = async (email, pwd) => {
  try {
    console.log('sending request')
    const response = await axios.post(`${baseURL}/accounts/login_user`, {
      email,
      pwd
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
