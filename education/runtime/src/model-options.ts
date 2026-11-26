/** Pure configuration adapter to ZCode's original restricted CEL compiler. */
import { compileModelOptionMap } from "@zcode/shared/model-config";

let source = "";
for await (const chunk of process.stdin) {
  source += String(chunk);
  if (source.length > 64000) throw new Error("model option map input is too large");
}
try {
  const input = JSON.parse(source) as { map: string; levels: string[] };
  if (!Array.isArray(input.levels) || input.levels.length > 16)
    throw new Error("invalid model reasoning levels");
  const program = compileModelOptionMap(input.map, "reasoningLevel");
  process.stdout.write(
    JSON.stringify({
      patches: Object.fromEntries(input.levels.map((level) => [level, program.evaluate(level)])),
    }),
  );
} catch (error) {
  process.stdout.write(
    JSON.stringify({ error: error instanceof Error ? error.message : "invalid model option map" }),
  );
  process.exitCode = 1;
}
