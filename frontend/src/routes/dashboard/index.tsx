import { createFileRoute } from "@tanstack/react-router";
import { Loader2, Plus } from "lucide-react";
import { useState } from "react";
import AddItemSheet from "@/components/item/add-item-sheet";
import ItemCard from "@/components/item/item-card";
import MaxWidthWrapper from "@/components/max-width-wrapper";
import { requireAuth } from "@/lib/route-guard";
import { useGetItemsItemsGetQuery } from "@/store/services/apis";

export const Route = createFileRoute("/dashboard/")({
  component: Index,
  beforeLoad: async () => {
    await requireAuth();
  },
});

function Index() {
  const [open, setOpen] = useState<boolean>(false);
  const { data, isLoading } = useGetItemsItemsGetQuery();

  return (
    <>
      <div className="flex h-full w-full flex-col items-start justify-start py-5">
        <MaxWidthWrapper>
          {isLoading ? (
            <div className="flex h-full w-full items-center justify-center">
              <Loader2 className="size-20 animate-spin" />
            </div>
          ) : (
            <div className="grid max-h-full w-full grid-cols-4 items-start justify-start gap-4 overflow-y-auto">
              {data?.data?.map((item) => (
                <ItemCard key={item.id} item={item} />
              ))}
              <div
                onClick={() => setOpen(true)}
                className="col-span-1 flex h-full min-h-[366px] w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed bg-muted/50 backdrop-blur-sm transition-colors duration-200 ease-in-out hover:bg-muted"
              >
                <Plus className="size-20" />
              </div>
            </div>
          )}
        </MaxWidthWrapper>
      </div>
      <AddItemSheet open={open} setOpen={setOpen} />
    </>
  );
}
