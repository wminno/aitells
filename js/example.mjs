// Aitells free quick score — plain fetch, no deps.
export async function analyze(text) {
  const r = await fetch("https://utils.bigfloppy.net/v1/aitells", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!r.ok) throw new Error(`aitells ${r.status}`);
  return r.json();
}

// npx example.mjs "In today's fast-paced world, robust solutions unlock value."
console.log(await analyze(process.argv[2] ?? "Hello world, this is a human sentence."));
