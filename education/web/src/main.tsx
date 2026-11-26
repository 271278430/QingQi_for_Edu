import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { EducationWorkspace } from "./workspace.js";
import { createEducationService } from "@qingqi/education-client";
import "./styles.css";
const service = createEducationService();
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <EducationWorkspace service={service} />
  </StrictMode>,
);
