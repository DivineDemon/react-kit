import { Link } from "@tanstack/react-router";
import { Atom } from "lucide-react";
import MaxWidthWrapper from "./max-width-wrapper";
import ModeToggle from "./mode-toggle";

function Navbar() {
  return (
    <nav className="h-16 w-full border-b py-3">
      <MaxWidthWrapper className="flex items-center justify-between">
        <Link to="/">
          <Atom className="size-9" />
        </Link>
        <ModeToggle />
      </MaxWidthWrapper>
    </nav>
  );
}

export default Navbar;
