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

interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export function validatePassword(password: string): ValidationResult {
  const errors: string[] = [];

  if (password.length < 8) {
    errors.push("Password must be at least 8 characters long.");
  } else if (password.length > 128) {
    errors.push("Password must be no more than 128 characters long.");
  }

  if (!/[A-Z]/.test(password)) {
    errors.push("Password must contain at least one uppercase letter (A–Z).");
  }

  if (!/[a-z]/.test(password)) {
    errors.push("Password must contain at least one lowercase letter (a–z).");
  }

  if (!/[0-9]/.test(password)) {
    errors.push("Password must contain at least one digit (0–9).");
  }

  if (!/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password)) {
    errors.push("Password must contain at least one special character (e.g. !@#$%^&*).");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
