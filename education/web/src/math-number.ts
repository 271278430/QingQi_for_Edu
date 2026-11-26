/** Sampling without an exact tool label is a measurement, not an exact fraction. */
export function numberLabel(n: number): string {
  if (n !== 0 && Math.abs(n) < 0.01 && Number.isFinite(n)) {
    const text = n.toString();
    if (/^-?\d+\.\d{1,6}$/.test(text)) {
      const digits = text.split(".")[1].length,
        denominator = 10 ** digits;
      let numerator = Math.round(n * denominator),
        a = Math.abs(numerator),
        b = denominator;
      while (b) {
        const t = a % b;
        a = b;
        b = t;
      }
      numerator /= a;
      return `${numerator}/${denominator / a}`;
    }
    return `≈${n.toExponential(1)}`;
  }
  const rounded = Math.round(n * 100) / 100;
  return `${Math.abs(n - rounded) < 1e-10 ? "" : "≈"}${Object.is(rounded, -0) ? 0 : rounded}`;
}
export function numberTex(n: number): string {
  return numberLabel(n)
    .replace(/^(-?\d+)\/(\d+)$/, "\\frac{$1}{$2}")
    .replace("≈", "\\approx ");
}
