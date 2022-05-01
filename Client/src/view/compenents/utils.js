import { Alert } from 'react-native'

export const alert = (alertContent) =>
  Alert.alert('Error', alertContent, [
    {
      text: 'Cancel',
      onPress: () => console.log('Cancel Pressed'),
      style: 'cancel'
    },
    { text: 'OK', onPress: () => console.log('OK Pressed') }
  ])
