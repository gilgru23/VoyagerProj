import {
  registerUser as userRegistrationRequest,
  loginUser as loginUserRequest,
  createConsumerProfile as createConsumerProfileRequest,
  registerDispenser as registerDispenserRequest
} from '../Communication/ApiRequests.js'

import { Consumer } from './Consumer.js'
import { Dispenser } from './dispenser.js'
import { MockServer } from '../Communication/mockServer.js'

import { responseStatus } from '../Config/constants.js'
import { createResponseObj } from '../utilsFunctions.js'

export class Model {
  constructor(testMode) {
    console.log(testMode)
    this.mock = new MockServer([], [])
    this.registerUserReq = testMode
      ? this.mock.registerUser
      : userRegistrationRequest
    this.loginUserReq = testMode ? this.mock.loginUser : loginUserRequest
    this.createConsumerProfileReq = testMode
      ? this.mock.createConsumerProfile
      : createConsumerProfileRequest
    this.registerDispenserRreq = testMode
      ? this.mock.registerDispenser
      : registerDispenserRequest
  }

  registerUser = async (email, password, firstName, lastName, birthDate) => {
    const response = await this.registerUserReq(
      email,
      password,
      firstName,
      lastName,
      birthDate
    )
    return response
  }

  loginUser = async (email, password) => {
    const response = await this.loginUserReq(email, password)
    if (response.status === responseStatus.SUCCESS) {
      return createResponseObj(
        responseStatus.SUCCESS,
        new Consumer(email, 'Gil', 'Gruber', new Date())
      )
    }
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }

  createConsumerProfile = async (
    residence,
    height,
    weight,
    units,
    gender,
    goal
  ) => {
    const response = await this.createConsumerProfileReq(
      residence,
      height,
      weight,
      units,
      gender,
      goal
    )
    if (response.status === responseStatus.SUCCESS) {
      return createResponseObj(
        responseStatus.SUCCESS,
        new Consumer(
          userCradentials.email,
          userCradentials.firstName,
          userCradentials.lastName,
          birthDate
        )
      )
    }
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }

  registerDispenser = async (id, name) => {
    const response = await this.registerDispenserRreq(id, name)
    if (response.status === responseStatus.SUCCESS) {
      return createResponseObj(responseStatus.SUCCESS, new Dispenser(id, name))
    }
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }
}
// export const registerUser = async (
//   email,
//   password,
//   firstName,
//   lastName,
//   birthDate
// ) => {
//   const response = await userRegistrationRequest(
//     email,
//     password,
//     firstName,
//     lastName,
//     birthDate
//   )
//   return response
// }

// export const loginUser = async (email, password) => {
//   const response = await loginUserRequest(email, password)
//   if (response.status === responseStatus.SUCCESS) {
//     return createResponseObj(
//       responseStatus.SUCCESS,
//       new Consumer(email, 'Gil', 'Gruber', new Date())
//     )
//   }
//   return createResponseObj(responseStatus.FAILURE, 'Server error')
// }

// export const createConsumerProfile = async (
//   residence,
//   height,
//   weight,
//   units,
//   gender,
//   goal
// ) => {
//   const response = await createConsumerProfileRequest(
//     residence,
//     height,
//     weight,
//     units,
//     gender,
//     goal
//   )
//   if (response.status === responseStatus.SUCCESS) {
//     return createResponseObj(
//       responseStatus.SUCCESS,
//       new Consumer(
//         userCradentials.email,
//         userCradentials.firstName,
//         userCradentials.lastName,
//         birthDate
//       )
//     )
//   }
//   return createResponseObj(responseStatus.FAILURE, 'Server error')
// }

// export const registerDispenser = async (id, name) => {
//   const response = await registerDispenserRequest(id, name)
//   if (response.status === responseStatus.SUCCESS) {
//     return createResponseObj(responseStatus.SUCCESS, new Dispenser(id, name))
//   }
//   return createResponseObj(responseStatus.FAILURE, 'Server error')
// }
