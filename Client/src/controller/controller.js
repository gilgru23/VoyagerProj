import {
  registerUser as registerUserInModel,
  createConsumerProfile as createConsumerProfileInModel,
  loginUser as loginUserInModel,
  registerDispenser as registerDispenserInModel
} from '../model/model.js'
import { Consumer } from '../model/Consumer.js'
import { responseStatus } from '../Config/constants.js'
import { createResponseObj } from '../utilsFunctions.js'

// const handleNotification = (data) => {
//   PushNotification.localNotification({
//     channelId: 'test-channel',
//     title: 'signIn Message',
//     message: data
//   })\
// }

const checkTheParametersIsValid = (...args) =>
  args.every((arg) => (console.log(args), arg !== ''))

export const registerUser = async (email, password, firstName, lastName) => {
  if (!checkTheParametersIsValid(email, password)) {
    return {
      status: responseStatus.FAILURE,
      content: 'email or password is empty'
    }
  }
  return registerUserInModel(email, password)
}

export const createConsumerProfile = async (
  residence,
  height,
  weight,
  units,
  gender,
  goal,
  birthDate,
  userCradentials
) => {
  if (
    !checkTheParametersIsValid(
      residence,
      height,
      weight,
      units,
      gender,
      goal,
      birthDate,
      userCradentials
    )
  ) {
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }
  return await createConsumerProfileInModel(
    residence,
    height,
    weight,
    units,
    gender,
    goal
  )
}

export const loginUser = async (email, password) => {
  if (!checkTheParametersIsValid(email, password)) {
    return createResponseObj(
      responseStatus.FAILURE,
      'one of the parameters is empty'
    )
  }
  return await loginUserInModel(email, password)
}

export const updatePersonalInfo = (birthDate, height, weight, gender) => {
  return true
}

export const getPodsPerDispenser = (dispenserId) => {
  return ['pod1', 'pod2', ' pod3']
}

export const registerDispenser = async (id, name) => {
  return await registerDispenserInModel(id, name)
}
