'use strict'

const fp = require('fastify-plugin')
const mongoose = require('mongoose')
const fastify = require('fastify')({
  logger: true
})
const routes = require('./routes')
const swagger = require('./config/swagger')
// const fp = require('fastify-plugin')

const schema = {
  type: 'object',
  required: [ 'MONGODB_URL'],
  properties: {
    MONGODB_URL: { type: 'string' },
  },
  additionalProperties: false
}
// Register Swagger
fastify
.register(require('fastify-swagger'), swagger.options)
.register(require('fastify-env'), { schema } )
.register(fp(connectToDatabases))

async function connectToDatabases(fastify) {
  mongoose.connect(fastify.config.MONGODB_URL + '/mycargarage', { useNewUrlParser: true })
}

// Loop over each route
routes.forEach((route, index) => {
  fastify.route(route)
})

// Run the server!
const start = async () => {
  try {
    await fastify.listen(3000, '0.0.0.0')
    fastify.swagger()
    fastify.log.info(`server listening on ${fastify.server.address().port}`)
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}

start()