import { Link } from "@tanstack/react-router";
import { Edit, EllipsisVertical, Eye, Trash } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { type ItemRead, useDeleteItemItemsItemIdDeleteMutation } from "@/store/services/apis";
import { Button } from "../ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "../ui/dropdown-menu";
import WarningModal from "../warning-modal";
import AddItemSheet from "./add-item-sheet";

interface ItemCardProps {
  item: ItemRead;
}

function ItemCard({ item }: ItemCardProps) {
  const [open, setOpen] = useState<boolean>(false);
  const [update, setUpdate] = useState<boolean>(false);
  const [deleteItem, { isLoading }] = useDeleteItemItemsItemIdDeleteMutation();

  const handleDelete = async () => {
    const response = await deleteItem({
      itemId: item.id,
    });

    if (response.data) {
      toast.success(response.data.message);
    } else {
      toast.error("Failed to delete item");
    }
  };

  return (
    <>
      <div
        key={item.id}
        className="relative col-span-1 flex h-full w-full flex-col items-center justify-between rounded-lg border bg-muted shadow"
      >
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="default" size="icon" className="absolute top-2.5 right-2.5 z-[1]">
              <EllipsisVertical />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <Link
                to="/items/$itemId"
                params={{ itemId: String(item.id) }}
                className="flex w-full items-center justify-start gap-2"
              >
                <Eye />
                View Item
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setUpdate(true)}>
              <Edit />
              Edit Item
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setOpen(true)} className="text-destructive">
              <Trash />
              Delete Item
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <img
          src={item.image_url}
          alt="item-image"
          className={cn("aspect-square w-full rounded-t-lg object-cover", {
            grayscale: item.name.includes("Mono"),
          })}
        />
        <div className="flex w-full flex-col items-start justify-start gap-1.5 p-3.5">
          <span className="w-full text-left font-bold text-[18px] leading-[18px]">{item.name}</span>
          <span className="line-clamp-2 w-full text-left text-[14px] text-muted-foreground leading-[16px]">
            {item.description}
          </span>
        </div>
      </div>
      <WarningModal
        open={open}
        setOpen={setOpen}
        title="Are you Sure?"
        text={
          <span>
            This action is irreversible, please
            <br />
            make sure before confirming.
          </span>
        }
        cta={handleDelete}
        isLoading={isLoading}
      />
      <AddItemSheet id={item.id} open={update} setOpen={setUpdate} />
    </>
  );
}

export default ItemCard;
