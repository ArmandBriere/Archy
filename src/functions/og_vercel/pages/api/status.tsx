export const config = {
  runtime: "experimental-edge",
};

export default function status() {
  return new Response('ok', {
    status: 200,
  });
}
