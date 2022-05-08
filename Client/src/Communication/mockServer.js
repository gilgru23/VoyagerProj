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
    this.dispensers = dispensers
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

    if (this.users.every((user) => user.email !== email)) {
      this.users.push({
        email: email,
        pwd: password,
        firstName: firstName,
        lastName: lastName,
        birthDate: birthDate
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

    if (this.users.some((user) => user.email === email && user.pwd === pwd)) {
      return createResponseObj(responseStatus.SUCCESS, {
        firstName: 'Gil',
        lastName: 'Gruber',
        birthDate: toDateString(new Date())
      })
    }
    return createResponseObj(responseStatus.FAILURE, 'User not found')
  }

  registerDispenser = (id, name) => {
    if (!checkTheParametersAreValid(id, name)) {
      return createResponseObj(
        responseStatus.FAILURE,
        'one of the paramter is invalid'
      )
    }
    if (!this.dispensers.includes(id)) {
      this.dispensers.push(id)
      return createResponseObj(responseStatus.SUCCESS, new Dispenser(id, name))
    }
    return createResponseObj(responseStatus.FAILURE, 'User already exists')
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
