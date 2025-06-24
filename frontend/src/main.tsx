import { createRoot } from "react-dom/client";
import "./assets/css/index.css";
import { createRouter, RouterProvider } from "@tanstack/react-router";
import Providers from "./components/providers";
import { routeTree } from "./routeTree.gen";

const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const rootElement = document.getElementById("root")!;
if (!rootElement.innerHTML) {
  const root = createRoot(rootElement);
  root.render(
    <Providers>
      <RouterProvider router={router} />
    </Providers>,
  );
}
