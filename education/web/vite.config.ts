import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { fileURLToPath } from "node:url";
export default defineConfig({
  plugins: [react(), tailwindcss()],
  // 消息代码块直接使用 ZCode 现有文件图标；缺少公共资源会触发 404。
  publicDir: fileURLToPath(new URL("../../packages/web/public/", import.meta.url)),
  // ZCode 公共消息渲染器沿用 UI 包的 @ 别名；消费方指向同一份上游源码。
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("../../packages/ui/src/", import.meta.url)),
    },
  },
  server: {
    proxy: { "/api": { target: "http://127.0.0.1:18772", changeOrigin: true } },
  },
  build: { outDir: "dist", emptyOutDir: true },
});
