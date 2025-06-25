import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import Navbar from "@/components/navbar";

export const Route = createRootRoute({
  component: () => (
    <div className="flex h-screen w-full flex-col items-start justify-start overflow-hidden">
      <Navbar />
      <div className="h-[calc(100vh-64px)] w-full">
        <Outlet />
      </div>
      <TanStackRouterDevtools />
    </div>
  ),
});
