import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  return <div className="flex w-full items-center justify-center p-5 font-bold text-3xl">App</div>;
}
