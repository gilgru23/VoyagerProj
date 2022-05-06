import { Alert } from 'react-native'

export const alert = (status, alertContent) =>
  Alert.alert(status, alertContent, [
    {
      text: 'Cancel',
      onPress: () => console.log('Cancel Pressed'),
      style: 'cancel'
    },
    { text: 'OK', onPress: () => console.log('OK Pressed') }
  ])
