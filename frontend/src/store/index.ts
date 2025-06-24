import { configureStore } from "@reduxjs/toolkit";
import { setupListeners } from "@reduxjs/toolkit/query";
import { persistReducer, persistStore } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { appApis } from "./services/apis";
import { api } from "./services/core";
import globalReducer from "./slices/global";

const persistConfig = {
  key: "root",
  storage,
};

const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
    // @ts-expect-error ype 'Reducer<GlobalState & PersistPartial, UnknownAction>' is not assignable to type 'Reducer<unknown, UnknownAction, unknown>'
    global: persistReducer(persistConfig, globalReducer),
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware({ serializableCheck: false }).concat(api.middleware),
});

setupListeners(store.dispatch);
void store.dispatch(appApis.endpoints.healthCheckGet.initiate());

export default store;
export const persistor = persistStore(store);
export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
