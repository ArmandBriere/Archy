import { Request, Response } from 'express'

/**
 * Responds to any HTTP request.
 *
 * @param req HTTP request context.
 * @param res HTTP response context.
 */
exports.js = (req: Request, res: Response) => {
  res.status(200).send("JS is slow!")
};
