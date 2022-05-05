import { responseStatus } from '../Config/constants.js'
import { createResponseObj } from '../utilsFunctions.js'

export class MockServer {
  users = []
  dispensers = []
  constructor(users, dispensers) {
    this.users = users
    this.dispensers = dispensers
  }
  registerUser(email, password, firstName, lastName, birthDate) {
    if (this.users.every((user) => user.email !== email)) {
      this.users.push({ email: email, pwd: password })
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'User already exists')
  }
  createConsumerProfile(residence, height, weight, units, gender, goal) {
    return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
  }

  loginUser(email, pwd) {
    if (this.users.any((user) => user.email === email && user.pwd === pwd)) {
      return createResponseObj(responseStatus.SUCCESS, 'login succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'User not found')
  }
  registerDispenser(address) {
    if (!this.dispensers.includes(address)) {
      this.dispensers.push(address)
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'User already exists')
  }
}
