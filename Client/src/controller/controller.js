export const registerUser = (email, password, role) => {
  if (email === '' && password === '') {
    Alert.alert('Enter details to signup!')
  }
}

export const loginUser = (email, password, role) => {
  if (email === '' && password === '') {
    Alert.alert('Enter details to signin!')
  }
}
