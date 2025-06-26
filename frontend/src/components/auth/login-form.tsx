import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "@tanstack/react-router";
import { Loader2, Send } from "lucide-react";
import type { Dispatch, SetStateAction } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";
import { loginSchema } from "@/lib/form-schemas";
import { useLoginUserUsersLoginPostMutation } from "@/store/services/apis";
import { Button } from "../ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "../ui/form";
import { Input } from "../ui/input";

interface LoginFormProps {
  setIsLogin: Dispatch<SetStateAction<boolean>>;
}

function LoginForm({ setIsLogin }: LoginFormProps) {
  const navigate = useNavigate();
  const loginForm = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
  });

  const [login, { isLoading: logging }] = useLoginUserUsersLoginPostMutation();

  const handleLogin = async (data: z.infer<typeof loginSchema>) => {
    const response = await login({
      userLogin: data,
    });

    if (response.data) {
      loginForm.reset();
      navigate({ to: "/dashboard" });
      toast.success(response.data.message);
    } else {
      toast.error("An error occurred while logging in.");
    }
  };

  return (
    <Form {...loginForm}>
      <form
        onSubmit={loginForm.handleSubmit(handleLogin)}
        className="flex w-full max-w-md flex-col items-center justify-center gap-5 rounded-xl border bg-muted/50 p-5 shadow backdrop-blur-sm"
      >
        <div className="flex w-full flex-col items-center justify-center gap-2 border-b pb-5">
          <span className="w-full text-left font-bold text-[20px] leading-[20px]">Login</span>
          <span className="w-full text-left text-[14px] text-muted-foreground leading-[14px]">
            Enter your details to get started.
          </span>
        </div>
        <FormField
          control={loginForm.control}
          name="email"
          render={({ field }) => (
            <FormItem className="w-full">
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="johnny_silverhand_roxx@arasaka.net" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={loginForm.control}
          name="password"
          render={({ field }) => (
            <FormItem className="w-full">
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" placeholder="• • • • • • • •" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button disabled={logging} type="submit" variant="default" size="lg" className="w-full">
          {logging ? (
            <Loader2 className="animate-spin" />
          ) : (
            <>
              <Send />
              Login
            </>
          )}
        </Button>
        <span
          onClick={() => setIsLogin(false)}
          className="w-full cursor-pointer text-center text-[12px] leading-[12px]"
        >
          Don&apos;t have an account?&nbsp;
          <span className="underline">Register</span>
        </span>
      </form>
    </Form>
  );
}

export default LoginForm;
