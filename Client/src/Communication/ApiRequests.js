import axios from 'axios'
import { baseURL, responseStatus } from '../Config/constants.js'
import { createResponseObj } from '../utilsFunctions.js'

export const registerUser = async (
  email,
  password,
  firstName,
  lastName,
  birthDate
) => {
  try {
    const response = await axios.post(`${baseURL}/accounts/register_user`, {
      email: email,
      pwd: password,
      f_name: firstName,
      l_name: lastName,
      dob: birthDate,
      phone: '0527484595'
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
      console.log('response from server:', response.data)
      return createResponseObj(responseStatus.SUCCESS, response.data)
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}

export const registerDispenser = async (id, name) => {
  try {
    console.log('sending to server: ', id, name)
    const response = await axios.post(
      `${baseURL}/consumers/register_dispenser`,
      {
        serial_num: id,
        version: name
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

export const registerPod = async (id, podType) => {
  try {
    const response = await axios.post(`${baseURL}/consumers/register_pod`, {
      serial_num: id,
      pod_type: podType
    })
    if (response) {
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}

export const dose = async (pod, amount, time) => {
  try {
    const response = await axios.post(`${baseURL}/consumers/dose`, {
      pod_serial_num: pod,
      amount: amount,
      time: time
    })
    if (response) {
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}

export const getDispensersOfConsumer = async () => {
  try {
    const response = await axios.post(
      `${baseURL}/consumers/get_dispensers_of_consumer`
    )
    if (response) {
      return createResponseObj(responseStatus.SUCCESS, response.data)
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}

export const getDosingHistory = async () => {
  try {
    const response = await axios.post(`${baseURL}/consumers/get_dosing_history`)
    if (response) {
      return createResponseObj(responseStatus.SUCCESS, response.data)
    }
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  } catch (e) {
    return createResponseObj(responseStatus.FAILURE, 'Registeration failed')
  }
}
