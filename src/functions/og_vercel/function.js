const next = require('next')
const app = next({ dev: false })
const handle = app.getRequestHandler()
const slasher = handler => (req, res) => {
    if (req.url === '') {
        req.url = '/'
    }
    return handler(req, res)
}
module.exports.handler = slasher((req, res) => {
    return app.prepare()
        .then(() => handle(req, res))
        .catch(ex => {
            console.error(ex.stack)
            process.exit(1)
        })
})
