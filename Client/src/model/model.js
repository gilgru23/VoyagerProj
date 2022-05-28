import {
  registerUser as userRegistrationRequest,
  loginUser as loginUserRequest,
  createConsumerProfile as createConsumerProfileRequest,
  registerDispenser as registerDispenserRequest,
  registerPod as registerPodRequest,
  dose as doseRequest,
  getDispensersOfConsumer as getDispensersOfConsumerRequest,
  getDosingHistory as getDosingHistoryRequest,
  getPods as getPodsRequest,
  logout as logoutRequest
} from '../Communication/ApiRequests.js'

import { Consumer } from './Consumer.js'
import { Dispenser } from './dispenser.js'
import { Pod } from './pod.js'
import { MockServer } from '../Communication/mockServer.js'

import { responseStatus } from '../Config/constants.js'
import { createResponseObj, toDateString } from '../utilsFunctions.js'

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

    this.registerPodRreq = testMode ? this.mock.registerPod : registerPodRequest
    this.doseReq = testMode ? this.mock.dose : doseRequest
    this.getDispensersOfConsumerReq = testMode
      ? this.mock.getDispensersOfConsumer
      : getDispensersOfConsumerRequest

    this.getDosingHistoryReq = testMode
      ? this.mock.getDosingHistory
      : getDosingHistoryRequest

    this.getPodsReq = testMode ? this.mock.getPods : getPodsRequest
    this.logoutReq = testMode ? this.mock.logout : logoutRequest
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
      const { first_name, last_name, date_of_birth } = response.content
      return createResponseObj(
        responseStatus.SUCCESS,
        new Consumer(email, first_name, last_name, date_of_birth)
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
    goal,
    userCradentials
  ) => {
    const response = await this.createConsumerProfileReq(
      residence,
      height,
      weight,
      units,
      gender,
      goal
    )
    console.log(response)
    if (response.status === responseStatus.SUCCESS) {
      console.log('In model', userCradentials)
      return createResponseObj(
        responseStatus.SUCCESS,
        new Consumer(
          userCradentials.email,
          userCradentials.firstName,
          userCradentials.lastName,
          userCradentials.birthDate
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

  getDispenserOfConsumer = async () => {
    const response = await this.getDispensersOfConsumerReq()
    if (response.status === responseStatus.SUCCESS) {
      console.log(response.content)
      return createResponseObj(
        responseStatus.SUCCESS,
        response.content.map(
          (dispenser) =>
            new Dispenser(dispenser.serial_number, dispenser.version)
        )
      )
    }
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }

  registerPod = async (id, podType) => {
    const response = await this.registerPodRreq(id, podType)
    if (response.status === responseStatus.SUCCESS) {
      return createResponseObj(responseStatus.SUCCESS, new Pod(id, podType))
    }
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }

  dose = async (pod, amount, time) => {
    const response = await this.doseReq(pod, amount, time)
    if (response.status === responseStatus.SUCCESS) {
      return createResponseObj(responseStatus.SUCCESS, 'Dosing succeeded')
    }
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }

  getDosingHistory = async () => {
    const response = await this.getDosingHistoryReq()
    if (response.status === responseStatus.SUCCESS) {
      return createResponseObj(responseStatus.SUCCESS, response.content)
    }
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }

  getPods = async () => {
    const creatPodsObjs = (podsJsns) => {
      return podsJsns.map((podJsn) => {
        const { serial_number, remainder, type_name } = podJsn
        return new Pod(serial_number, type_name, remainder)
      })
    }
    const response = await this.getPodsReq()
    if (response.status === responseStatus.SUCCESS) {
      const pods = creatPodsObjs(response.content)
      console.log('pods in model', pods)
      return createResponseObj(responseStatus.SUCCESS, pods)
    }
    return createResponseObj(responseStatus.FAILURE, 'Server error')
  }

  logout = async () => {
    const response = await this.logoutReq()
    if (response.status === responseStatus.SUCCESS) {
      console.log('logout in model')
      return createResponseObj(responseStatus.SUCCESS, response.content)
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
