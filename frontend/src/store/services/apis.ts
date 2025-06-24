import { api } from "./core";
export const addTagTypes = ["items"] as const;
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
    }),
    overrideExisting: false,
  });
export { injectedRtkApi as appApis };
export type HealthCheckGetApiResponse = /** status 200 Successful Response */ ResponseModelHealthBase;
export type HealthCheckGetApiArg = void;
export type GetItemsItemsGetApiResponse = /** status 200 Successful Response */ ResponseModelListItemRead;
export type GetItemsItemsGetApiArg = void;
export type CreateItemItemsPostApiResponse = /** status 200 Successful Response */ ResponseModelItemRead;
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
export const {
  useHealthCheckGetQuery,
  useGetItemsItemsGetQuery,
  useCreateItemItemsPostMutation,
  useGetItemItemsItemIdGetQuery,
  useUpdateItemItemsItemIdPutMutation,
  useDeleteItemItemsItemIdDeleteMutation,
} = injectedRtkApi;
