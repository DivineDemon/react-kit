import { z } from "zod";

export const addItemSchema = z.object({
  description: z.string(),
  name: z.string().min(1, "Name is required"),
  image_url: z.string().url("Image must be a valid URL"),
});

export const registerSchema = z.object({
  email: z.string().email({ message: "Invalid email address" }),
  last_name: z.string().min(1, { message: "Last name is required" }),
  first_name: z.string().min(1, { message: "First name is required" }),
  profile_picture: z.string().url({ message: "Must be a valid URL" }),
  password: z.string().min(8, { message: "Password must be at least 8 characters long" }),
});

export const loginSchema = z.object({
  email: z.string().email({ message: "Invalid email address" }),
  password: z.string().min(1, { message: "Password is required" }),
});

export const updateFormSchema = z.object({
  new_password: z.string().optional(),
  current_password: z.string().optional(),
  email: z.string().email({ message: "Invalid email address" }),
  last_name: z.string().min(1, { message: "Last name is required" }),
  first_name: z.string().min(1, { message: "First name is required" }),
  profile_picture: z.string().url({ message: "Invalid URL for profile picture" }),
});
