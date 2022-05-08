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
import { checkTheParametersAreValid } from '../utilsFunctions.js'

export class Controller {
  constructor() {
    this.model = new Model(false)
  }

  registerUser = async (email, password, firstName, lastName, birthDate) => {
    console.log(checkTheParametersAreValid)
    if (!checkTheParametersAreValid(email, password)) {
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
      !checkTheParametersAreValid(
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
    if (!checkTheParametersAreValid(email, password)) {
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
