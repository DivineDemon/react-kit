import { type ClassValue, clsx } from "clsx";
import { toast } from "sonner";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export async function uploadToImgbb(image: File): Promise<string> {
  const endpoint = new URL("https://api.imgbb.com/1/upload");
  endpoint.searchParams.set("key", import.meta.env.VITE_IMGBB_API_KEY);

  const formData = new FormData();
  formData.append("image", image);

  const response = await fetch(endpoint.toString(), {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    toast.error(`imgbb upload failed (${response.status}): ${errorBody}`);
  }

  const imageData = await response.json();

  return imageData.data.url;
}
