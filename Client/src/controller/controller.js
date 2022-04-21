import { registerUser as modelRegisterUser } from '../model/model'
import PushNotification from 'react-native-push-notification'

// const handleNotification = (data) => {
//   PushNotification.localNotification({
//     channelId: 'test-channel',
//     title: 'signIn Message',
//     message: data
//   })
// }

export const registerUser = async (email, password, role) => {
  if (email === '' && password === '') {
    Alert.alert('Enter details to signup!')
  }
  const response = await modelRegisterUser(email, password)
  // handleNotification(response)
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
