import {
  registerUser as registerUserInServer,
  createConsumerProfile as createConsumerProfileInServer,
  login
} from '../Communication/ApiRequests'
import { Consumer } from '../model/Consumer'
import PushNotification from 'react-native-push-notification'
import { responseStatus } from '../Config/constants'

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
  if (email === '' || password === '') {
    return {
      status: responseStatus.FAILURE,
      content: 'email or password is empty'
    }
  }
  const response = await registerUserInServer(
    email,
    password,
    firstName,
    lastName
  )
  console.log(response)
  return response
  // handleNotification(response)
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
    checkTheParametersIsValid(
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
    const response = await createConsumerProfileInServer(
      residence,
      height,
      weight,
      units,
      gender,
      goal
    )
    if (response.status === responseStatus.SUCCESS) {
      return {
        status: responseStatus.SUCCESS,
        content: new Consumer(
          userCradentials.email,
          userCradentials.firstName,
          userCradentials.lastName,
          birthDate
        )
      }
    }
    return {
      status: responseStatus.FAILURE,
      content: 'Server error'
    }
  }
  return {
    status: responseStatus.FAILURE,
    content: 'one of the parameters is empty'
  }
}

export const loginUser = async (email, password) => {
  if (checkTheParametersIsValid(email, password)) {
    const response = await login(email, password)
    if (response.status === responseStatus.SUCCESS) {
      return {
        status: responseStatus.SUCCESS,
        content: new Consumer(email, 'Gil', 'Gruber', new Date())
      }
    }
  }
  return {
    status: responseStatus.FAILURE,
    content: 'one of the parameters is empty'
  }
}

export const updatePersonalInfo = (birthDate, height, weight, gender) => {
  return true
}

export const getPodsPerDispenser = (dispenserId) => {
  return ['pod1', 'pod2', ' pod3']
}
