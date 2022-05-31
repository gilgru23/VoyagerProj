import { responseStatus } from '../Config/constants.js'
import { Consumer } from '../model/Consumer.js'
import { Dispenser } from '../model/dispenser.js'
import {
  createResponseObj,
  validateEmail,
  checkStrongPassword,
  checkTheParametersAreValid,
  toDateString
} from '../utilsFunctions.js'

export class MockServer {
  constructor(users, dispensers) {
    this.users = users
  }

  registerUser = (email, password, firstName, lastName, birthDate) => {
    if (
      !checkTheParametersAreValid(
        email,
        password,
        firstName,
        lastName,
        birthDate
      )
    ) {
      return createResponseObj(
        responseStatus.FAILURE,
        'one of the paramter is invalid'
      )
    }
    if (!validateEmail(email)) {
      return createResponseObj(responseStatus.FAILURE, 'email is invalid')
    }

    if (!checkStrongPassword(password)) {
      return createResponseObj(responseStatus.FAILURE, 'password is weak')
    }

    if (this.users.every((user) => user.consumer.email !== email)) {
      this.users.push({
        consumer: new Consumer(email, firstName, lastName, birthDate),
        password: password,
        dispensers: [],
        pods: []
      })
      return createResponseObj(responseStatus.SUCCESS, 'registration succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'User already exists')
  }

  loginUser = (email, pwd) => {
    if (!checkTheParametersAreValid(email, pwd)) {
      return createResponseObj(
        responseStatus.FAILURE,
        'one of the paramter is invalid'
      )
    }
    if (!validateEmail(email)) {
      return createResponseObj(responseStatus.FAILURE, 'email is invalid')
    }

    if (!checkStrongPassword(pwd)) {
      return createResponseObj(responseStatus.FAILURE, 'password is weak')
    }
    const user = this.users.find(
      (user) => user.consumer.email === email && user.password === pwd
    )
    if (user) {
      return createResponseObj(responseStatus.SUCCESS, {
        first_name: user.consumer.firstName,
        last_name: user.consumer.lastName,
        date_of_birth: user.consumer.birthDate
      })
    }
    return createResponseObj(responseStatus.FAILURE, 'User not found')
  }

  registerDispenser = (id, name, email) => {
    if (!checkTheParametersAreValid(id, name)) {
      return createResponseObj(
        responseStatus.FAILURE,
        'one of the paramter is invalid'
      )
    }
    console.log('******')
    console.log(this.users)
    console.log(email)
    console.log('******')
    const user = this.users.find((user) => user.consumer.email === email)
    if (!user.dispensers.includes(id)) {
      user.dispensers.push(id)
      return createResponseObj(
        responseStatus.SUCCESS,
        'Adding dispenser succeeded'
      )
    }
    return createResponseObj(responseStatus.FAILURE, 'Dispenser already exists')
  }

  registerPod = (id, name, email) => {
    if (!checkTheParametersAreValid(id, name)) {
      return createResponseObj(
        responseStatus.FAILURE,
        'one of the paramter is invalid'
      )
    }
    const user = this.users.find((user) => user.consumer.email === email)
    if (!user.pods.includes(id)) {
      user.pods.push(id)
      return createResponseObj(
        responseStatus.SUCCESS,
        'Adding dispenser succeeded'
      )
    }
    return createResponseObj(responseStatus.FAILURE, 'Pod already exists')
  }

  createConsumerProfile = (residence, height, weight, units, gender, goal) => {
    if (
      !checkTheParametersAreValid(
        residence,
        height,
        weight,
        units,
        gender,
        goal
      )
    ) {
      return createResponseObj(
        responseStatus.FAILURE,
        'one of the paramter is invalid'
      )
    }
    const email = this.users[0].email
    return createResponseObj(
      responseStatus.SUCCESS,
      new Consumer(
        this.users[0].email,
        this.users[0].firstName,
        this.users[0].lastName,
        this.users[0].birthDate
      )
    )
  }
}
