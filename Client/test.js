import assert from 'assert'
import { registerUser, loginUser } from './src/model/model.js'
import { responseStatus } from './src/Config/constants.js'
import mockyeah from '@mockyeah/test-server-mocha'
import supertest from 'supertest'
import http from 'http'
const request = supertest(mockyeah)

describe('registration', async function () {
  it('should create a mock service that returns JSON', (done) => {
    // create service mock that returns json data
    mockyeah.get('/wondrous', { json: { foo: 'bar' } })

    // assert service mock is working
    request.get('/wondrous').expect(200, { foo: 'bar' }, done)
  })
  it('registiration success scenario', async function () {
    const response = await registerUser('Gil@gmail.com', '1234')
    assert.equal(response.status, responseStatus.SUCCESS)
  })
  // it('registiration failure scenario', async function () {
  //   const response = await registerUser('Gil', '1234')
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
  // it('registiration failure scenario', async function () {
  //   const response = await registerUser('', '1234')
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
  // it('registiration failure scenario', async function () {
  //   const response = await registerUser('Gil', '')
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
})

describe('login', async function () {
  it('login success scenario', async function () {
    const response = await loginUser('Gil@gmail.com', '1234')
    assert.equal(response.status, responseStatus.SUCCESS)
  })
  // it('registiration failure scenario', async function () {
  //   const response = await registerUser('Gil', '1234')
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
  // it('login failure scenario', async function () {
  //   const response = await loginUser('', '1234')
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
  // it('login failure scenario', async function () {
  //   const response = await loginUser('Gil@gmail.com', '')
  //   assert.equal(response.status, responseStatus.FAILURE)
  // })
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
