import { createFileRoute } from "@tanstack/react-router";
import { useGetItemsItemsGetQuery } from "@/store/services/apis";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const { data, isLoading } = useGetItemsItemsGetQuery();

  return (
    <div className="flex w-full items-center justify-center p-5 font-bold text-3xl">
      {isLoading ? "Loading..." : data?.data?.length ? "Items Loaded" : "No Items Found"}
      <div className="mt-2 text-gray-500 text-sm">
        {data?.data?.length ? `Total items: ${data.data.length}` : "Try adding some items!"}
      </div>
    </div>
  );
}
