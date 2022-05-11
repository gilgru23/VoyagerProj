import assert, { doesNotMatch, doesNotReject } from 'assert'
import { responseStatus } from './src/Config/constants.js'
import { Model } from './src/model/model.js'
import { toDateString } from './src/utilsFunctions.js'
import { Consumer } from './src/model/Consumer.js'
import { MockServer } from './src/Communication/mockServer.js'
import { Dispenser } from './src/model/dispenser.js'

const model = new Model(false)

const validEmail = 'gilggg3@gmail.com'
const invalidEmail = 'Gilgmail.com'
const validPassword = 'Aa12345679!'
const inValidPassword = '1234'
const firstName = 'Gil'
const lastName = 'Gruber'
const birthDateString = toDateString(new Date())
const residence = '1234'
const height = '180'
const weight = '80'
const units = 1
const gender = 1
const goal = 'N/A'
const podId = '1234'
const podType = 'regular'
const userCradentials = {
  email: validEmail,
  firstName: firstName,
  lastName: lastName,
  birthDate: birthDateString
}
const dispenserId = 'id1234'
const dispenserName = 'dispenser1'

// describe('registration', async function () {
//   this.afterEach(async () => {
//     MockServer.users = []
//     MockServer.dispensres = []
//   })

//   it('registiration success scenario', async function () {
//     const response = await model.registerUser(
//       validEmail,
//       validPassword,
//       firstName,
//       lastName,
//       birthDateString
//     )
//     assert.equal(response.status, responseStatus.SUCCESS)
//   })

// it('registiration failure scenario- invalid mail', async function () {
//   const response = await model.registerUser(
//     invalidEmail,
//     validPassword,
//     firstName,
//     lastName,
//     birthDateString
//   )
//   assert.equal(response.status, responseStatus.FAILURE)
// })

// it('registiration failure scenario- weak password', async function () {
//   const response = await model.registerUser(
//     validEmail,
//     inValidPassword,
//     firstName,
//     lastName,
//     birthDateString
//   )
//   assert.equal(response.status, responseStatus.FAILURE)
// })
// })

// describe('login', async function () {
//   this.beforeEach(async () => {
//     await model.registerUser(
//       validEmail,
//       validPassword,
//       firstName,
//       lastName,
//       birthDateString
//     )
//   })

//   this.afterEach(async () => {
//     MockServer.users = []
//     MockServer.dispensres = []
//   })

//   it('login success scenario', async function () {
//     const response = await model.loginUser(validEmail, validPassword)
//     console.log(response)
//     assert.equal(response.status, responseStatus.SUCCESS)
//     assert.deepEqual(
//       response.content,
//       new Consumer(validEmail, firstName, lastName, birthDateString)
//     )
//   })

//   it('login failure scenario- empty parameter', async function () {
//     const response = await model.loginUser('', validPassword)
//     assert.equal(response.status, responseStatus.FAILURE)
//   })

//   it('login failure scenario- bad email', async function () {
//     const response = await model.loginUser(invalidEmail, validPassword)
//     assert.equal(response.status, responseStatus.FAILURE)
//   })
// })

// describe('createConsumerProfile', async function () {
//   this.beforeEach(async () => {
//     await model.registerUser(
//       validEmail,
//       validPassword,
//       firstName,
//       lastName,
//       birthDateString
//     )
//   })

//   this.afterEach(async () => {
//     MockServer.users = []
//     MockServer.dispensres = []
//   })

//   it('createConsumerProfile success scenario', async function () {
//     assert.equal(true, true)
//   })

//   it('createConsumerProfile success scenario', async function () {
//     console.log('checking')
//     const response = await model.createConsumerProfile(
//       residence,
//       height,
//       weight,
//       units,
//       gender,
//       goal,
//       userCradentials
//     )
//     assert.equal(response.status, responseStatus.SUCCESS)
//     assert.deepEqual(
//       response.content,
//       new Consumer(validEmail, firstName, lastName, birthDateString)
//     )
//   })

//   it('createConsumerProfile failure scenario- empty parameter', async function () {
//     const response = await model.createConsumerProfile(
//       residence,
//       height,
//       weight,
//       '',
//       gender,
//       goal,
//       userCradentials
//     )
//     assert.equal(response.status, responseStatus.FAILURE)
//   })
// })

// describe('register dispenser', async function (done) {
//   this.beforeEach(async () => {
//     // await model.registerUser(
//     //   validEmail,
//     //   validPassword,
//     //   firstName,
//     //   lastName,
//     //   birthDateString
//     // )
//   })
//   it('register dispenser success scenario', async function (done) {
//     await model.loginUser(validEmail, validPassword)
//     done()
//     const response = await model.registerDispenser(dispenserId, dispenserName)
//     assert.equal(response.status, responseStatus.SUCCESS)
//     assert.deepEqual(
//       response.content,
//       new Dispenser(dispenserId, dispenserName)
//     )
//   })
//   // it('register dispenser failure scenario- duplicate dispenser', async function () {
//   //   const response = await model.registerDispenser(dispenserId, dispenserName)
//   //   assert.equal(response.status, responseStatus.FAILURE)
//   // })
//   // it('register dispenser failure scenario- one of the parameters is empty', async function () {
//   //   const response = await model.registerDispenser('', dispenserName)
//   //   assert.equal(response.status, responseStatus.FAILURE)
//   // })
//   // it('register dispenser failure scenario', async function () {
//   //   const response = await model.registerDispenser('1234', 'dispenser1')
//   //   assert.equal(response.status, responseStatus.FAILURE)
//   // })
// })

describe('register pod', async function (done) {
  this.beforeEach(async () => {
    // await model.registerUser(
    //   validEmail,
    //   validPassword,
    //   firstName,
    //   lastName,
    //   birthDateString
    // )
  })
  it('register pod success scenario', async function (done) {
    await model.loginUser(validEmail, validPassword)
    done()
    const response = await model.registerPod(podId, podType)
    assert.equal(response.status, responseStatus.SUCCESS)
    assert.deepEqual(response.content, new Pod(podId, podType))
  })
  // it('register dispenser failure scenario- duplicate dispenser', async function () {
  //   const response = await model.registerDispenser(dispenserId, dispenserName)
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
  // it('register dispenser failure scenario- one of the parameters is empty', async function () {
  //   const response = await model.registerDispenser('', dispenserName)
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
  // it('register dispenser failure scenario', async function () {
  //   const response = await model.registerDispenser('1234', 'dispenser1')
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
})
