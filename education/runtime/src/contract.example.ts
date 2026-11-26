import { Frame } from "./contract.js";
export const example = Frame.parse({
  id: 1,
  op: "plan",
  input: { nodes: [{ id: "review", depends_on: [] }] },
});
