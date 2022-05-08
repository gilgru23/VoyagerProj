import assert from 'assert'
import { responseStatus } from './src/Config/constants.js'
import { Model } from './src/model/model.js'
import { toDateString } from './src/utilsFunctions.js'
const model = new Model(true)

describe('registration', async function () {
  it('registiration success scenario', async function () {
    const response = await model.registerUser(
      'Gil@gmail.com',
      'Aa1234!',
      'Gil',
      'Gruber',
      toDateString(new Date())
    )
    assert.equal(response.status, responseStatus.SUCCESS)
  })

  it('registiration failure scenario- invalid mail', async function () {
    const response = await model.registerUser(
      'Gil@gmail.com',
      'Aa1234!',
      'Gil',
      'Gruber',
      toDateString(new Date())
    )
    assert.equal(response.status, responseStatus.FAILURE)
  })

  it('registiration failure scenario- weak password', async function () {
    const response = await model.registerUser(
      'Gil@gmail.com',
      '1234',
      'Gil',
      'Gruber',
      toDateString(new Date())
    )
    assert.equal(response.status, responseStatus.FAILURE)
  })
})

describe('login', async function () {
  this.beforeEach(async () => {
    await model.registerUser(
      'Gil@gmail.com',
      'Aa1234!',
      'Gil',
      'Gruber',
      toDateString(new Date())
    )
  })

  it('login success scenario', async function () {
    const response = await model.loginUser('Gil@gmail.com', 'Aa1234!')
    assert.equal(response.status, responseStatus.SUCCESS)
  })

  it('login failure scenario- empty parameter', async function () {
    const response = await model.loginUser('', '1234')
    assert.equal(response.status, responseStatus.FAILURE)
  })

  it('login failure scenario- bad email', async function () {
    const response = await model.loginUser('Gilgmail.com', '1234')
    assert.equal(response.status, responseStatus.FAILURE)
  })
})

// describe('register dispenser', async function () {
//   it('register dispenser success scenario', async function () {
//     const response = await model.registerDispenser('1234', 'dispenser1')
//     assert.equal(response.status, responseStatus.SUCCESS)
//   })

//   it('register dispenser failure scenario', async function () {
//     const response = await model.registerDispenser('1234', 'dispenser1')
//     assert.equal(response.status, responseStatus.FAILURE)
//   })
// })

// import mockyeah from '@mockyeah/test-server-mocha'
// import supertest from 'supertest'
// const request = supertest(mockyeah)

// describe('Wondrous service', () => {
//   it('should create a mock service that returns an internal error', (done) => {
//     // create failing service mock
//     mockyeah.get('/wondrous', { status: 500 })

//     // assert service mock is working
//     request.get('/wondrous').expect(500, done)
//   })
// })
