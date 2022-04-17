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

export const updatePersonalInfo = (birthDate, height, weight, gender) => {
  return true
}

export const getPodsPerDispenser = (dispenserId) => {
  return ['pod1', 'pod2', ' pod3']
}
