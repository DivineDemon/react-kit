import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { type Dispatch, type SetStateAction, useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";
import { addItemSchema } from "@/lib/form-schemas";
import {
  useCreateItemItemsPostMutation,
  useGetItemItemsItemIdGetQuery,
  useUpdateItemItemsItemIdPutMutation,
} from "@/store/services/apis";
import { Button } from "../ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "../ui/form";
import ImageUploader from "../ui/image-uploader";
import { Input } from "../ui/input";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "../ui/sheet";
import { Textarea } from "../ui/textarea";

interface AddItemSheetProps {
  id?: number;
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
}

function AddItemSheet({ id, open, setOpen }: AddItemSheetProps) {
  const form = useForm<z.infer<typeof addItemSchema>>({
    resolver: zodResolver(addItemSchema),
  });

  const { data } = useGetItemItemsItemIdGetQuery(
    {
      itemId: id || 0,
    },
    {
      skip: !open || !id,
      refetchOnMountOrArgChange: true,
    },
  );
  const [addItem, { isLoading: adding }] = useCreateItemItemsPostMutation();
  const [updateItem, { isLoading: updating }] = useUpdateItemItemsItemIdPutMutation();

  const onSubmit = async (data: z.infer<typeof addItemSchema>) => {
    let response = null;

    if (id) {
      response = await updateItem({
        itemId: id,
        itemUpdate: data,
      });
    } else {
      response = await addItem({
        itemBase: data,
      });
    }

    if (response.data) {
      setOpen(false);
      form.reset();
      toast.success(response.data.message);
    } else {
      toast.error(`Failed to ${id ? "update" : "add"} item.`);
    }
  };

  useEffect(() => {
    if (data) {
      form.setValue("name", `${data.data?.name}`);
      form.setValue("image_url", `${data.data?.image_url}`);
      form.setValue("description", `${data.data?.description}`);
    }
  }, [data, form.setValue]);

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetContent className="gap-0">
        <SheetHeader>
          <SheetTitle>Add an Item</SheetTitle>
          <SheetDescription>Add your favorite items here.</SheetDescription>
        </SheetHeader>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="flex h-full w-full flex-col items-start justify-start gap-5 border-t p-5"
          >
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem className="w-full">
                  <FormLabel>Item Name</FormLabel>
                  <FormControl>
                    <Input placeholder="A drop of virgin blood" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem className="w-full">
                  <FormLabel>Item Description</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="A drop of virgin blood is a rare and powerful item that can be used in various magical rituals."
                      className="h-44 resize-none"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="image_url"
              render={({ field, fieldState }) => (
                <ImageUploader field={field} error={fieldState.error} label="Item Image" />
              )}
            />
            <div className="mt-auto flex w-full items-center justify-end gap-2.5">
              <Button onClick={() => setOpen(false)} type="button" variant="secondary" size="sm">
                Cancel
              </Button>
              <Button disabled={adding || updating} type="submit" variant="default" size="sm">
                {adding || updating ? <Loader2 className="animate-spin" /> : "Submit"}
              </Button>
            </div>
          </form>
        </Form>
      </SheetContent>
    </Sheet>
  );
}

export default AddItemSheet;
