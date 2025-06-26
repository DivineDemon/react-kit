import { createFileRoute } from "@tanstack/react-router";
import { Loader2 } from "lucide-react";
import MaxWidthWrapper from "@/components/max-width-wrapper";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { requireAuth } from "@/lib/route-guard";
import { cn } from "@/lib/utils";
import { useGetItemItemsItemIdGetQuery } from "@/store/services/apis";

export const Route = createFileRoute("/items/$itemId/")({
  component: ItemDetails,
  beforeLoad: async () => {
    await requireAuth();
  },
});

function ItemDetails() {
  const { itemId } = Route.useParams();

  const { data, isLoading } = useGetItemItemsItemIdGetQuery({
    itemId: Number(itemId),
  });

  return (
    <div className="flex h-full w-full flex-col items-start justify-start py-5">
      <MaxWidthWrapper>
        {isLoading ? (
          <div className="flex h-full w-full items-center justify-center">
            <Loader2 className="size-20 animate-spin" />
          </div>
        ) : (
          <Card className="w-full">
            <CardHeader>
              <div className="flex w-full items-center justify-start gap-2.5">
                <img
                  src={data?.data?.image_url}
                  alt="item-image"
                  className={cn("size-10 rounded-md", {
                    grayscale: data?.data?.name.includes("Mono"),
                  })}
                />
                <div className="flex w-full flex-col items-center justify-center gap-1.5">
                  <CardTitle className="w-full text-left">Item Details</CardTitle>
                  <CardDescription className="w-full text-left">
                    Details for Item: {itemId} - {data?.data?.name}
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <span className="w-full text-left text-muted-foreground text-sm">{data?.data?.description}</span>
            </CardContent>
          </Card>
        )}
      </MaxWidthWrapper>
    </div>
  );
}
