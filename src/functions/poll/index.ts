import { Request, Response } from 'express'

/**
 * Responds to any HTTP request.
 *
 * @param _ HTTP request context.
 * @param res HTTP response context.
 */
exports.js = (request: Request, res: Response) => {
  res.status(200).send("TypeScript has a good type system!")
};
