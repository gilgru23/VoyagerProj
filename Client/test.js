import assert from 'assert'
import { responseStatus } from './src/Config/constants.js'
import { Model } from './src/model/model.js'
const model = new Model(true)

describe('registration', async function () {
  it('registiration success scenario', async function () {
    const response = await model.registerUser(
      'Gil@gmail.com',
      '1234',
      'Gil',
      'Gruber',
      new Date()
    )
    assert.equal(response.status, responseStatus.SUCCESS)
  })
})

describe('login', async function () {
  it('login success scenario', async function () {
    const response = await model.loginUser('Gil@gmail.com', '1234')
    assert.equal(response.status, responseStatus.SUCCESS)
  })
  it('login failure scenario', async function () {
    const response = await model.loginUser('', '1234')
    assert.equal(response.status, responseStatus.FAILURE)
  })
})

describe('register dispenser', async function () {
  it('register dispenser success scenario', async function () {
    const response = await model.registerDispenser('1234', 'dispenser1')
    assert.equal(response.status, responseStatus.SUCCESS)
  })

  it('register dispenser failure scenario', async function () {
    const response = await model.registerDispenser('1234', 'dispenser1')
    assert.equal(response.status, responseStatus.FAILURE)
  })
})

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
