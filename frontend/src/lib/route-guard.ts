import { redirect } from "@tanstack/react-router";
import store from "@/store";

export async function requireAuth() {
  const state = store.getState();

  if (!state.global.token) {
    throw redirect({ to: "/" });
  }
}
