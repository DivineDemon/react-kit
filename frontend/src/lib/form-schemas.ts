import { z } from "zod";

export const addItemSchema = z.object({
  description: z.string(),
  name: z.string().min(1, "Name is required"),
  image_url: z.string().url("Image must be a valid URL"),
});
