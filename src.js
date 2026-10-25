// Serves the static site; the only logic is sending www to the bare domain.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "www.burkeruder.com") {
      url.hostname = "burkeruder.com";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
