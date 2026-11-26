/** Layout ticks only; mathematical landmarks remain owned by the figure compiler. */
export function plotTicks(lo: number, hi: number): number[] {
  const raw = (hi - lo) / 4;
  const power = 10 ** Math.floor(Math.log10(raw));
  const ratio = raw / power;
  const step = power * (ratio <= 1 ? 1 : ratio <= 2 ? 2 : ratio <= 5 ? 5 : 10);
  return Array.from(
    { length: Math.max(1, Math.floor(hi / step) - Math.ceil(lo / step) + 1) },
    (_, i) => Number(((Math.ceil(lo / step) + i) * step).toPrecision(10)),
  );
}
