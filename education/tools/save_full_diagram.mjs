// Export the complete SVG outside the application's scroll containers.
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
export async function saveFullDiagram(browser, locator, destination) {
  const diagram = await locator.evaluate((root) => {
    const copy = root.cloneNode(true);
    const originals = [root, ...root.querySelectorAll("*")];
    const copies = [copy, ...copy.querySelectorAll("*")];
    for (let i = 0; i < originals.length; i++) {
      const style = getComputedStyle(originals[i]);
      if (!copies[i].style) continue;
      for (const property of [
        "fill",
        "stroke",
        "stroke-width",
        "stroke-dasharray",
        "text-anchor",
        "paint-order",
        "display",
        "position",
        "overflow",
        "clip",
        "width",
        "height",
        "line-height",
        "color",
        "font-family",
        "font-size",
        "font-weight",
        "opacity",
      ]) {
        copies[i].style.setProperty(property, style.getPropertyValue(property));
      }
    }
    const width = Math.ceil(root.viewBox.baseVal.width);
    const height = Math.ceil(root.viewBox.baseVal.height);
    copy.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    copy.style.width = `${width}px`;
    copy.style.height = `${height}px`;
    copy.style.maxWidth = "none";
    copy.style.background = getComputedStyle(
      root.closest(".edu-card") ?? document.body,
    ).backgroundColor;
    return { width, height, svg: new XMLSerializer().serializeToString(copy) };
  });
  await writeFile(
    new URL(destination.href.replace(/\.png$/, ".svg")),
    diagram.svg,
  );
  const page = await browser.newPage({
    viewport: { width: diagram.width, height: diagram.height },
  });
  try {
    await page.setContent(`<body style="margin:0">${diagram.svg}</body>`);
    await page
      .locator("svg")
      .first()
      .screenshot({ path: fileURLToPath(destination) });
  } finally {
    await page.close();
  }
}
