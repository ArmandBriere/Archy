import express, { json } from 'express'

const index = require('./index')

const server = express()
server.use(json())

server.post('*', index.poll)

server.listen(8888)
