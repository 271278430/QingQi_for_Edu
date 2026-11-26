/** Same canonical result for JSON callers and the Web's SSE transport. */
export async function readTeachEvents(response) {
  return (await response.text())
    .replace(/\r\n/g, "\n")
    .split("\n\n")
    .filter((frame) => frame.startsWith("data: "))
    .map((frame) => JSON.parse(frame.slice(6)));
}
export async function readTeachResponse(response) {
  if (!response.headers()["content-type"]?.includes("text/event-stream")) return response.json();
  const events = await readTeachEvents(response);
  const last = events.at(-1);
  if (last?.kind !== "done") throw Error(last?.message || "teaching stream did not complete");
  return last.value;
}
