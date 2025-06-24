import { createRoot } from "react-dom/client";
import "./assets/css/index.css";
import { createRouter, RouterProvider } from "@tanstack/react-router";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { routeTree } from "./routeTree.gen";
import store, { persistor } from "./store";

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
    <Provider store={store}>
      <PersistGate persistor={persistor}>
        <RouterProvider router={router} />
      </PersistGate>
    </Provider>,
  );
}
