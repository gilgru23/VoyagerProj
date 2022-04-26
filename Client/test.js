// import assert from 'assert'
// import { registerUser } from './src/model/model.js'
// describe('Array', async function () {
//   it('should return -1 when the value is not present', async function () {
//     const response = await registerUser('Gil', '1234')
//     assert.equal(response, 'Email already registerred')
//   })
// })
import mockyeah from '@mockyeah/test-server-mocha'
import supertest from 'supertest'
const request = supertest(mockyeah)

describe('Wondrous service', () => {
  it('should create a mock service that returns an internal error', (done) => {
    // create failing service mock
    mockyeah.get('/wondrous', { status: 500 })

    // assert service mock is working
    request.get('/wondrous').expect(500, done)
  })
})
