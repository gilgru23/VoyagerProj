// import {
//   registerUser as registerUserInModel,
//   createConsumerProfile as createConsumerProfileInModel,
//   loginUser as loginUserInModel,
//   registerDispenser as registerDispenserInModel
// } from '../model/model.js'
import { Consumer } from '../model/Consumer.js'
import { responseStatus } from '../Config/constants.js'
import { createResponseObj } from '../utilsFunctions.js'
import { Model } from '../model/model.js'

const checkTheParametersIsValid = (...args) =>
  args.every((arg) => (console.log(args), arg !== ''))

export class Controller {
  constructor() {
    this.model = new Model(false)
  }

  registerUser = async (email, password, firstName, lastName, birthDate) => {
    if (!checkTheParametersIsValid(email, password)) {
      return {
        status: responseStatus.FAILURE,
        content: 'email or password is empty'
      }
    }
    return await this.model.registerUser(
      email,
      password,
      firstName,
      lastName,
      birthDate
    )
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
    if (
      !checkTheParametersIsValid(
        residence,
        height,
        weight,
        units,
        gender,
        goal,
        userCradentials
      )
    ) {
      return createResponseObj(responseStatus.FAILURE, 'Server error')
    }
    return await this.model.createConsumerProfile(
      residence,
      height,
      weight,
      units,
      gender,
      goal,
      userCradentials
    )
  }

  loginUser = async (email, password) => {
    if (!checkTheParametersIsValid(email, password)) {
      return createResponseObj(
        responseStatus.FAILURE,
        'one of the parameters is empty'
      )
    }
    return await this.model.loginUser(email, password)
  }

  updatePersonalInfo = (birthDate, height, weight, gender) => {
    return true
  }

  getPodsPerDispenser = (dispenserId) => {
    return ['pod1', 'pod2', ' pod3']
  }

  registerDispenser = async (id, name) => {
    return await this.model.registerDispenser(id, name)
  }
}

// export const registerUser = async (
//   email,
//   password,
//   firstName,
//   lastName,
//   birthDate
// ) => {
//   if (!checkTheParametersIsValid(email, password)) {
//     return {
//       status: responseStatus.FAILURE,
//       content: 'email or password is empty'
//     }
//   }
//   return registerUserInModel(email, password, firstName, lastName, birthDate)
// }

// export const createConsumerProfile = async (
//   residence,
//   height,
//   weight,
//   units,
//   gender,
//   goal,
//   birthDate,
//   userCradentials
// ) => {
//   if (
//     !checkTheParametersIsValid(
//       residence,
//       height,
//       weight,
//       units,
//       gender,
//       goal,
//       birthDate,
//       userCradentials
//     )
//   ) {
//     return createResponseObj(responseStatus.FAILURE, 'Server error')
//   }
//   return await createConsumerProfileInModel(
//     residence,
//     height,
//     weight,
//     units,
//     gender,
//     goal
//   )
// }

// export const loginUser = async (email, password) => {
//   if (!checkTheParametersIsValid(email, password)) {
//     return createResponseObj(
//       responseStatus.FAILURE,
//       'one of the parameters is empty'
//     )
//   }
//   return await loginUserInModel(email, password)
// }

// export const updatePersonalInfo = (birthDate, height, weight, gender) => {
//   return true
// }

// export const getPodsPerDispenser = (dispenserId) => {
//   return ['pod1', 'pod2', ' pod3']
// }

// export const registerDispenser = async (id, name) => {
//   return await registerDispenserInModel(id, name)
// }
