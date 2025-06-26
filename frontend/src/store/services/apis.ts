import { setProfilePicture, setToken } from "../slices/global";
import { api } from "./core";
export const addTagTypes = ["items", "users"] as const;
const injectedRtkApi = api
  .enhanceEndpoints({
    addTagTypes,
  })
  .injectEndpoints({
    endpoints: (build) => ({
      healthCheckGet: build.query<HealthCheckGetApiResponse, HealthCheckGetApiArg>({
        query: () => ({ url: `/` }),
      }),
      getItemsItemsGet: build.query<GetItemsItemsGetApiResponse, GetItemsItemsGetApiArg>({
        query: () => ({ url: `/items/` }),
        providesTags: ["items", "items"],
      }),
      createItemItemsPost: build.mutation<CreateItemItemsPostApiResponse, CreateItemItemsPostApiArg>({
        query: (queryArg) => ({
          url: `/items/`,
          method: "POST",
          body: queryArg.itemBase,
        }),
        invalidatesTags: ["items", "items"],
      }),
      getItemItemsItemIdGet: build.query<GetItemItemsItemIdGetApiResponse, GetItemItemsItemIdGetApiArg>({
        query: (queryArg) => ({ url: `/items/${queryArg.itemId}` }),
        providesTags: ["items", "items"],
      }),
      updateItemItemsItemIdPut: build.mutation<UpdateItemItemsItemIdPutApiResponse, UpdateItemItemsItemIdPutApiArg>({
        query: (queryArg) => ({
          url: `/items/${queryArg.itemId}`,
          method: "PUT",
          body: queryArg.itemUpdate,
        }),
        invalidatesTags: ["items", "items"],
      }),
      deleteItemItemsItemIdDelete: build.mutation<
        DeleteItemItemsItemIdDeleteApiResponse,
        DeleteItemItemsItemIdDeleteApiArg
      >({
        query: (queryArg) => ({
          url: `/items/${queryArg.itemId}`,
          method: "DELETE",
        }),
        invalidatesTags: ["items", "items"],
      }),
      registerUserUsersRegisterPost: build.mutation<
        RegisterUserUsersRegisterPostApiResponse,
        RegisterUserUsersRegisterPostApiArg
      >({
        query: (queryArg) => ({
          url: `/users/register`,
          method: "POST",
          body: queryArg.userBase,
        }),
        invalidatesTags: ["users", "users"],
      }),
      loginUserUsersLoginPost: build.mutation<LoginUserUsersLoginPostApiResponse, LoginUserUsersLoginPostApiArg>({
        query: (queryArg) => ({
          url: `/users/login`,
          method: "POST",
          body: queryArg.userLogin,
        }),
        invalidatesTags: ["users", "users"],
        onQueryStarted: async (_, { dispatch, queryFulfilled }) => {
          const { data } = await queryFulfilled;

          if (data.status === 200) {
            dispatch(setToken(data.data?.token || ""));
            dispatch(setProfilePicture(data.data?.profile_picture || ""));
          }
        },
      }),
      getMyProfileUsersMeGet: build.query<GetMyProfileUsersMeGetApiResponse, GetMyProfileUsersMeGetApiArg>({
        query: () => ({ url: `/users/me` }),
        providesTags: ["users", "users"],
      }),
      updateUserProfileUsersMePut: build.mutation<
        UpdateUserProfileUsersMePutApiResponse,
        UpdateUserProfileUsersMePutApiArg
      >({
        query: (queryArg) => ({
          url: `/users/me`,
          method: "PUT",
          body: queryArg.userUpdate,
        }),
        invalidatesTags: ["users", "users"],
      }),
      deleteUserProfileUsersMeDelete: build.mutation<
        DeleteUserProfileUsersMeDeleteApiResponse,
        DeleteUserProfileUsersMeDeleteApiArg
      >({
        query: () => ({ url: `/users/me`, method: "DELETE" }),
        invalidatesTags: ["users", "users"],
      }),
    }),
    overrideExisting: false,
  });
export { injectedRtkApi as appApis };
export type HealthCheckGetApiResponse = /** status 200 Successful Response */ ResponseModelHealthBase;
export type HealthCheckGetApiArg = void;
export type GetItemsItemsGetApiResponse = /** status 200 Successful Response */ ResponseModelListItemRead;
export type GetItemsItemsGetApiArg = void;
export type CreateItemItemsPostApiResponse = /** status 201 Successful Response */ ResponseModelItemRead;
export type CreateItemItemsPostApiArg = {
  itemBase: ItemBase;
};
export type GetItemItemsItemIdGetApiResponse = /** status 200 Successful Response */ ResponseModelItemRead;
export type GetItemItemsItemIdGetApiArg = {
  itemId: number;
};
export type UpdateItemItemsItemIdPutApiResponse = /** status 200 Successful Response */ ResponseModelItemRead;
export type UpdateItemItemsItemIdPutApiArg = {
  itemId: number;
  itemUpdate: ItemUpdate;
};
export type DeleteItemItemsItemIdDeleteApiResponse = /** status 200 Successful Response */ ResponseModelItemDelete;
export type DeleteItemItemsItemIdDeleteApiArg = {
  itemId: number;
};
export type RegisterUserUsersRegisterPostApiResponse = /** status 200 Successful Response */ ResponseModelUserRead;
export type RegisterUserUsersRegisterPostApiArg = {
  userBase: UserBase;
};
export type LoginUserUsersLoginPostApiResponse = /** status 200 Successful Response */ ResponseModelUserRead;
export type LoginUserUsersLoginPostApiArg = {
  userLogin: UserLogin;
};
export type GetMyProfileUsersMeGetApiResponse = /** status 200 Successful Response */ ResponseModelUserRead;
export type GetMyProfileUsersMeGetApiArg = void;
export type UpdateUserProfileUsersMePutApiResponse = /** status 200 Successful Response */ ResponseModelUserRead;
export type UpdateUserProfileUsersMePutApiArg = {
  userUpdate: UserUpdate;
};
export type DeleteUserProfileUsersMeDeleteApiResponse = /** status 200 Successful Response */ ResponseModelUserDelete;
export type DeleteUserProfileUsersMeDeleteApiArg = void;
export type HealthBase = {
  status: string;
  message: string;
};
export type ResponseModelHealthBase = {
  status?: number;
  data?: HealthBase | null;
  message?: string;
};
export type ItemRead = {
  name: string;
  description: string;
  image_url: string;
  id: number;
};
export type ResponseModelListItemRead = {
  status?: number;
  data?: ItemRead[] | null;
  message?: string;
};
export type ResponseModelItemRead = {
  status?: number;
  data?: ItemRead | null;
  message?: string;
};
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
};
export type ItemBase = {
  name: string;
  description: string;
  image_url: string;
};
export type ItemUpdate = {
  name?: string | null;
  description?: string | null;
  image_url?: string | null;
};
export type ItemDelete = {
  id: number;
};
export type ResponseModelItemDelete = {
  status?: number;
  data?: ItemDelete | null;
  message?: string;
};
export type UserRead = {
  email: string;
  password: string;
  last_name: string;
  first_name: string;
  profile_picture?: string | null;
  id: number;
  token?: string | null;
};
export type ResponseModelUserRead = {
  status?: number;
  data?: UserRead | null;
  message?: string;
};
export type UserBase = {
  email: string;
  password: string;
  last_name: string;
  first_name: string;
  profile_picture?: string | null;
};
export type UserLogin = {
  email: string;
  password: string;
};
export type UserUpdate = {
  email?: string | null;
  last_name?: string | null;
  first_name?: string | null;
  new_password?: string | null;
  current_password?: string | null;
  profile_picture?: string | null;
};
export type UserDelete = {
  id: number;
};
export type ResponseModelUserDelete = {
  status?: number;
  data?: UserDelete | null;
  message?: string;
};
export const {
  useHealthCheckGetQuery,
  useGetItemsItemsGetQuery,
  useCreateItemItemsPostMutation,
  useGetItemItemsItemIdGetQuery,
  useUpdateItemItemsItemIdPutMutation,
  useDeleteItemItemsItemIdDeleteMutation,
  useRegisterUserUsersRegisterPostMutation,
  useLoginUserUsersLoginPostMutation,
  useGetMyProfileUsersMeGetQuery,
  useUpdateUserProfileUsersMePutMutation,
  useDeleteUserProfileUsersMeDeleteMutation,
} = injectedRtkApi;
