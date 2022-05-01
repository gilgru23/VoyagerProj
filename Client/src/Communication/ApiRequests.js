import axios from 'axios'
import { baseURL, responseStatus } from '../Config/constants.js'
import { createResponseObj } from '../utilsFunctions.js'

export const registerUser = async (email, password, firstName, lastName) => {
  try {
    const response = await axios.post(`${baseURL}/accounts/register_user`, {
      email: email,
      pwd: password,
      firstName: firstName,
      lastName: lastName
    })
    if (response) {
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
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
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}

export const loginUser = async (email, pwd) => {
  try {
    console.log('sending request')
    const response = await axios.post(`${baseURL}/accounts/login_user`, {
      email,
      pwd
    })
    if (response) {
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}

export const registerDispenser = async (address) => {
  try {
    const response = await axios.post(
      `${baseURL}/consumers/register_dispenser`,
      {
        address
      }
    )
    if (response) {
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}
