/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */

exports.js = (req, res) => {
    res.status(200).send("JS is slow!")
};
