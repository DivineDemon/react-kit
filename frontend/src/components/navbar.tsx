import { Link, useNavigate } from "@tanstack/react-router";
import { Atom, LogOut, User2 } from "lucide-react";
import { useSelector } from "react-redux";
import type { RootState } from "@/store";
import MaxWidthWrapper from "./max-width-wrapper";
import ModeToggle from "./mode-toggle";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "./ui/dropdown-menu";

function Navbar() {
  const navigate = useNavigate();
  const { profile_picture } = useSelector((state: RootState) => state.global);

  const logout = () => {
    localStorage.clear();
    navigate({ to: "/" });
  };

  return (
    <nav className="h-16 w-full border-b py-3">
      <MaxWidthWrapper className="flex items-center justify-between">
        <Link to="/dashboard">
          <Atom className="size-9" />
        </Link>
        <div className="flex items-center justify-center gap-2.5">
          <ModeToggle />
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Avatar className="bg-muted">
                <AvatarImage alt="profile-picture" src={profile_picture ?? ""} />
                <AvatarFallback className="p-2">
                  <User2 />
                </AvatarFallback>
              </Avatar>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>
                <Link to="/dashboard/profile" className="flex items-center gap-2">
                  <User2 />
                  Profile
                </Link>
              </DropdownMenuItem>
              <DropdownMenuItem className="text-destructive" onClick={logout}>
                <LogOut />
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </MaxWidthWrapper>
    </nav>
  );
}

export default Navbar;
