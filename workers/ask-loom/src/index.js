/**
 * Ask Loom public intake endpoint.
 *
 * Deploy as a Cloudflare Worker and bind the route:
 *   ask-api.loomresearch.xyz/submit*
 *
 * Required Worker secrets:
 *   GITHUB_TOKEN — fine-grained PAT with Issues: Read and write on the Loom repo
 *
 * Optional Worker variables:
 *   GITHUB_OWNER=loom-research-system
 *   GITHUB_REPO=loom-research-system
 *   ALLOWED_ORIGIN=https://loomresearch.xyz
 */
const json = (body, status = 200, origin = "*") => new Response(JSON.stringify(body), {
  status,
  headers: {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin"
  }
});

export default {
  async fetch(request, env) {
    const allowedOrigin = env.ALLOWED_ORIGIN || "https://loomresearch.xyz";
    const origin = request.headers.get("Origin") || "";
    if (request.method === "OPTIONS") {
      if (origin !== allowedOrigin) return new Response(null, { status: 403 });
      return new Response(null, { status: 204, headers: {
        "Access-Control-Allow-Origin": allowedOrigin,
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "86400",
        "Vary": "Origin"
      }});
    }
    if (origin !== allowedOrigin) return json({ error: "Origin not allowed." }, 403, allowedOrigin);
    if (new URL(request.url).pathname !== "/submit" || request.method !== "POST") {
      return json({ error: "Not found." }, 404, allowedOrigin);
    }
    if (!env.GITHUB_TOKEN) return json({ error: "Intake service is not configured." }, 503, allowedOrigin);

    let payload;
    try { payload = await request.json(); }
    catch { return json({ error: "Please submit a valid request." }, 400, allowedOrigin); }

    // Honeypot: bots that fill this hidden field receive a neutral success response.
    if (typeof payload.website === "string" && payload.website.trim()) {
      return json({ received: true, reference: null }, 202, allowedOrigin);
    }
    const question = typeof payload.question === "string" ? payload.question.trim() : "";
    const context = typeof payload.context === "string" ? payload.context.trim() : "";
    if (question.length < 5) return json({ error: "Please enter a question of at least five characters." }, 400, allowedOrigin);
    if (question.length > 2000 || context.length > 3000) {
      return json({ error: "Your question or context is too long. Please shorten it and try again." }, 413, allowedOrigin);
    }

    const owner = env.GITHUB_OWNER || "loom-research-system";
    const repo = env.GITHUB_REPO || "loom-research-system";
    const title = "[Ask Loom] " + question.replace(/\s+/g, " ").slice(0, 75);
    const body = [
      "## What do you want to know?",
      question,
      "",
      "## Requested depth",
      "Quick Read",
      "",
      "## Helpful scope or identifiers",
      context || "Not provided.",
      "",
      "---",
      "Submitted through the public Ask Loom form. Intake receipt is not a finding or approval to publish."
    ].join("\n");

    let upstream;
    try {
      upstream = await fetch(`https://api.github.com/repos/${owner}/${repo}/issues`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
          "Accept": "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28",
          "Content-Type": "application/json",
          "User-Agent": "Project-Loom-Ask-Intake"
        },
        body: JSON.stringify({ title, body, labels: ["research-request"] })
      });
    } catch {
      return json({ error: "Loom could not receive the request right now. Please try again later." }, 502, allowedOrigin);
    }
    if (!upstream.ok) {
      // Do not expose GitHub response bodies or credentials to the public client.
      return json({ error: "Loom could not register the request right now. Please try again later." }, 502, allowedOrigin);
    }
    const issue = await upstream.json();
    return json({ received: true, reference: "LOOM-" + issue.number }, 201, allowedOrigin);
  }
};
