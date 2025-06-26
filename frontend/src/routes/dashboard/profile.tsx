import { zodResolver } from "@hookform/resolvers/zod";
import { createFileRoute } from "@tanstack/react-router";
import { Loader2, Save } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";
import MaxWidthWrapper from "@/components/max-width-wrapper";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import ImageUploader from "@/components/ui/image-uploader";
import { Input } from "@/components/ui/input";
import { updateFormSchema } from "@/lib/form-schemas";
import { validatePassword } from "@/lib/utils";
import { useGetMyProfileUsersMeGetQuery, useUpdateUserProfileUsersMePutMutation } from "@/store/services/apis";

export const Route = createFileRoute("/dashboard/profile")({
  component: UserProfile,
});

function UserProfile() {
  const form = useForm<z.infer<typeof updateFormSchema>>({
    resolver: zodResolver(updateFormSchema),
  });

  const { data } = useGetMyProfileUsersMeGetQuery();
  const [updateProfile, { isLoading }] = useUpdateUserProfileUsersMePutMutation();

  const onSubmit = async (data: z.infer<typeof updateFormSchema>) => {
    if (data.current_password) {
      const validated = validatePassword(data?.current_password);
      if (!validated.valid) {
        toast.error(`Current password validation failed: ${validated.errors.join(", ")}`);
        return;
      }
    }

    if (data.new_password) {
      const validated = validatePassword(data?.new_password);
      if (!validated.valid) {
        toast.error(`New password validation failed: ${validated.errors.join(", ")}`);
        return;
      }
    }

    const response = await updateProfile({
      userUpdate: data,
    });

    if (response.data) {
      form.reset();
      toast.success("Profile updated successfully!");
    } else {
      toast.error("Failed to update profile. Please try again.");
    }
  };

  useEffect(() => {
    if (data) {
      form.setValue("email", `${data.data?.email}`);
      form.setValue("last_name", `${data.data?.last_name}`);
      form.setValue("first_name", `${data.data?.first_name}`);
      form.setValue("profile_picture", `${data.data?.profile_picture}`);
    }
  }, [data, form.setValue]);

  return (
    <div className="flex h-full w-full flex-col items-start justify-start py-5">
      <MaxWidthWrapper className="overflow-y-auto">
        <Card className="w-full">
          <CardHeader>
            <CardTitle>Edit Profile</CardTitle>
            <CardDescription>View and edit your profile information here.</CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="grid w-full grid-cols-2 gap-5">
                <FormField
                  control={form.control}
                  name="first_name"
                  render={({ field }) => (
                    <FormItem className="w-full">
                      <FormLabel>First Name</FormLabel>
                      <FormControl>
                        <Input placeholder="Johnny" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="last_name"
                  render={({ field }) => (
                    <FormItem className="w-full">
                      <FormLabel>Last Name</FormLabel>
                      <FormControl>
                        <Input placeholder="Silverhand" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem className="w-full">
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input type="email" placeholder="johnny_silverhand_roxx@arasaka.net" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="current_password"
                  render={({ field }) => (
                    <FormItem className="w-full">
                      <FormLabel>Current Password</FormLabel>
                      <FormControl>
                        <Input type="password" placeholder="• • • • • • • •" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="new_password"
                  render={({ field }) => (
                    <FormItem className="w-full">
                      <FormLabel>New Password</FormLabel>
                      <FormControl>
                        <Input type="password" placeholder="• • • • • • • •" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <div className="col-span-2 w-full">
                  <FormField
                    control={form.control}
                    name="profile_picture"
                    render={({ field, fieldState }) => (
                      <ImageUploader field={field} error={fieldState.error} label="Item Image" />
                    )}
                  />
                </div>
                <div className="col-span-2 flex w-full items-center justify-end">
                  <Button disabled={isLoading} type="submit" variant="default" size="sm">
                    {isLoading ? (
                      <Loader2 className="animate-spin" />
                    ) : (
                      <>
                        <Save />
                        Save Changes
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </Form>
          </CardContent>
        </Card>
      </MaxWidthWrapper>
    </div>
  );
}
