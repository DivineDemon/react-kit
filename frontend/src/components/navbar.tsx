import { Atom } from "lucide-react";
import MaxWidthWrapper from "./max-width-wrapper";
import ModeToggle from "./mode-toggle";

function Navbar() {
  return (
    <nav className="h-16 w-full border-b p-3">
      <MaxWidthWrapper className="flex items-center justify-between">
        <Atom className="size-9" />
        <ModeToggle />
      </MaxWidthWrapper>
    </nav>
  );
}

export default Navbar;
