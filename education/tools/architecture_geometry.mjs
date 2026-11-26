/** Inspect the rendered figure, including label-to-label and label-to-node collisions. */
export async function geometryFailures(svg, diagram) {
  return svg.evaluate((root, data) => {
    const failures = [];
    const intersects = (a, b, margin = 1) =>
      a.x + margin < b.x + b.width &&
      a.x + a.width > b.x + margin &&
      a.y + margin < b.y + b.height &&
      a.y + a.height > b.y + margin;
    const box = (text) => {
      const b = text.getBBox(),
        m = root.getCTM().inverse().multiply(text.getCTM());
      const p = new DOMPoint(b.x, b.y).matrixTransform(m),
        q = new DOMPoint(b.x + b.width, b.y + b.height).matrixTransform(m);
      return { x: p.x, y: p.y, width: q.x - p.x, height: q.y - p.y };
    };
    const nodeTexts = [...root.querySelectorAll("[data-node-text]")].map((t) => ({
      text: t.textContent,
      node: t.closest("[data-panorama-node]").getAttribute("data-panorama-node"),
      box: box(t),
    }));
    const labels = [...root.querySelectorAll("[data-edge-label]")].map((t) => ({
      text: t.textContent,
      box: box(t),
    }));
    for (let i = 0; i < nodeTexts.length; i++)
      for (let j = i + 1; j < nodeTexts.length; j++)
        if (intersects(nodeTexts[i].box, nodeTexts[j].box))
          failures.push({
            kind: "text-overlap",
            a: nodeTexts[i].text,
            b: nodeTexts[j].text,
          });
    for (let i = 0; i < labels.length; i++) {
      for (const n of data.nodes.filter((n) => !["frame", "rail"].includes(n.kind)))
        if (intersects(labels[i].box, n))
          failures.push({
            kind: "label-node",
            label: labels[i].text,
            node: n.id,
          });
      for (const t of nodeTexts)
        if (intersects(labels[i].box, t.box))
          failures.push({
            kind: "label-text",
            label: labels[i].text,
            text: t.text,
          });
      for (let j = i + 1; j < labels.length; j++)
        if (intersects(labels[i].box, labels[j].box))
          failures.push({
            kind: "label-label",
            a: labels[i].text,
            b: labels[j].text,
          });
    }
    const nodes = data.nodes.filter((n) => !["frame", "rail"].includes(n.kind));
    for (const t of nodeTexts) {
      const n = data.nodes.find((n) => n.id === t.node);
      if (
        t.box.x < n.x - 1 ||
        t.box.y < n.y - 1 ||
        t.box.x + t.box.width > n.x + n.width + 1 ||
        t.box.y + t.box.height > n.y + n.height + 1
      )
        failures.push({ kind: "text-clipped", node: t.node, text: t.text });
    }
    for (const t of root.querySelectorAll("[data-node-text],[data-edge-label]")) {
      if (parseFloat(getComputedStyle(t).fontSize) * root.getScreenCTM().a < 12)
        failures.push({ kind: "small-text", text: t.textContent });
    }
    for (const e of data.edges) {
      const p = root.querySelector(`[data-panorama-edge="${e.id}"] > path:last-of-type`);
      if (!p || !p.getTotalLength()) {
        failures.push({ kind: "missing-edge", edge: e.id });
        continue;
      }
      if (e.heads !== "none" && !p.getAttribute("marker-end"))
        failures.push({ kind: "missing-arrow", edge: e.id });
      for (const n of nodes.filter((n) => ![e.source, e.target].includes(n.id))) {
        for (let at = 1; at < p.getTotalLength(); at += 3) {
          const v = p.getPointAtLength(at);
          if (
            v.x > n.x + 1 &&
            v.x < n.x + n.width - 1 &&
            v.y > n.y + 1 &&
            v.y < n.y + n.height - 1
          ) {
            failures.push({ kind: "edge-through-node", edge: e.id, node: n.id });
            break;
          }
        }
      }
    }
    for (let i = 0; i < nodes.length; i++)
      for (let j = i + 1; j < nodes.length; j++)
        if (intersects(nodes[i], nodes[j]))
          failures.push({
            kind: "node-overlap",
            a: nodes[i].id,
            b: nodes[j].id,
          });
    return failures;
  }, diagram);
}
