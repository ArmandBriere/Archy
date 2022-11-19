import express from 'express'

const index = require('./index')

const server = express()

server.post('*', index.js)

server.listen(8888)
