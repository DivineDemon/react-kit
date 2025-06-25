import type { ReactNode } from "react";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import store, { persistor } from "@/store";
import { ThemeProvider } from "./theme-provider";
import { Toaster } from "./ui/sonner";

interface ProviderProps {
  children: ReactNode;
}

function Providers({ children }: ProviderProps) {
  return (
    <Provider store={store}>
      <PersistGate persistor={persistor}>
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
          <Toaster richColors={true} duration={1500} />
          {children}
        </ThemeProvider>
      </PersistGate>
    </Provider>
  );
}

export default Providers;
