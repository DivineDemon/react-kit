import { Loader2, TriangleAlert } from "lucide-react";
import type { Dispatch, ReactNode, SetStateAction } from "react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogFooter } from "@/components/ui/dialog";

interface WarningModalProps {
  open: boolean;
  title: string;
  text: ReactNode;
  cta?: () => void;
  isLoading?: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
}

function WarningModal({ cta, open, text, title, setOpen, isLoading }: WarningModalProps) {
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-[425px]">
        <div className="flex flex-col items-center justify-center py-10">
          <div className="size-20 rounded-full bg-destructive/20 p-3">
            <TriangleAlert size="100%" color="#FF0000" className="size-full" />
          </div>
          <span className="mt-7 mb-2.5 w-full text-center font-semibold text-[24px] leading-[24px] tracking-tight">
            {title}
          </span>
          <span className="w-full text-center font-medium text-[14px] text-muted-foreground leading-[18px] tracking-tight">
            {text}
          </span>
        </div>
        <DialogFooter>
          <Button onClick={() => setOpen(false)} type="button" variant="secondary" className="cursor-pointer">
            Cancel
          </Button>
          <Button
            disabled={isLoading}
            onClick={() => {
              if (cta) {
                cta();
              }
            }}
            type="button"
            variant="destructive"
            className="cursor-pointer"
          >
            {isLoading ? <Loader2 className="size-5 animate-spin" /> : "Confirm"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default WarningModal;
