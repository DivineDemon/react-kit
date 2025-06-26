import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import LoginForm from "@/components/auth/login-form";
import RegisterForm from "@/components/auth/register-form";
import MaxWidthWrapper from "@/components/max-width-wrapper";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const [isLogin, setIsLogin] = useState<boolean>(false);

  return (
    <div className="flex h-full w-full flex-col items-start justify-start py-5">
      <MaxWidthWrapper className="flex items-center justify-center">
        {isLogin ? <LoginForm setIsLogin={setIsLogin} /> : <RegisterForm setIsLogin={setIsLogin} />}
      </MaxWidthWrapper>
    </div>
  );
}
