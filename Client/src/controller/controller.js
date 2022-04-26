import { registerUser as RegisterUserInServer } from '../Communication/ApiRequests'
import PushNotification from 'react-native-push-notification'
import { responseStatus } from '../Config/constants'

// const handleNotification = (data) => {
//   PushNotification.localNotification({
//     channelId: 'test-channel',
//     title: 'signIn Message',
//     message: data
//   })\
// }

const checkTheParametersIsValid = (args) => args.every((arg) => arg !== '')

export const registerUser = async (email, password) => {
  if (email === '' || password === '') {
    return {
      status: responseStatus.FAILURE,
      content: 'email or password is empty'
    }
  }
  const response = await RegisterUserInServer(email, password)
  console.log(response)
  return response
  // handleNotification(response)
}

export const createConsumerProfile = (...args) => {
  if (checkTheParametersIsValid(args)) {
  }
}

export const loginUser = (email, password, role) => {
  if (email === '' && password === '') {
    Alert.alert('Enter details to signin!')
  }
}

export const updatePersonalInfo = (birthDate, height, weight, gender) => {
  return true
}

export const getPodsPerDispenser = (dispenserId) => {
  return ['pod1', 'pod2', ' pod3']
}
