import { registerUser as userRegistrationRequest } from '../Communication/ApiRequests.js'
export const registerUser = async (userName, password) => {
  console.log('in model')
  const response = await userRegistrationRequest(userName, password)
  console.log('response in model', response)
  return response
}
