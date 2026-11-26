import { useState } from "react";
import { Button } from "@zcode/ui/button";
import { Input } from "@zcode/ui/input";
import { GraduationCap } from "lucide-react";
import type { Bootstrap, EducationService } from "./contract.js";
import { errorText } from "./format.js";

export function Login({
  service,
  onSuccess,
  error,
}: {
  service: EducationService;
  onSuccess: (value: Bootstrap) => void;
  error: string;
}) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState(error);
  const [busy, setBusy] = useState(false);
  return (
    <div className="grid min-h-dvh place-items-center bg-background p-6 text-ui-base text-foreground">
      <form
        className="edu-card w-full max-w-sm space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          setBusy(true);
          setMessage("");
          service
            .post<Bootstrap>("/api/login", { username, password })
            .then(onSuccess)
            .catch((e) => setMessage(errorText(e)))
            .finally(() => setBusy(false));
        }}
      >
        <GraduationCap className="size-8" />
        <h1 className="text-ui-xl font-semibold">登录清启学习工作台</h1>
        <p className="text-foreground-subtle">使用为你开通的学习账户登录。</p>
        <label className="block">
          账户
          <Input
            size="lg"
            className="edu-field text-mobile-input-safe mt-2"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label className="block">
          密码
          <Input
            size="lg"
            className="edu-field text-mobile-input-safe mt-2"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <Button className="w-full" size="lg" disabled={busy}>
          登录
        </Button>
        <p role="alert" className="text-destructive">
          {message}
        </p>
      </form>
    </div>
  );
}
