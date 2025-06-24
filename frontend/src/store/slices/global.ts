import { createSlice } from "@reduxjs/toolkit";

const initialState: GlobalState = {
  item: null,
  token:
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
};

const globalSlice = createSlice({
  name: "global",
  initialState,
  reducers: {
    setItem: (state, action) => {
      state.item = action.payload;
    },
    setToken: (state, action) => {
      state.token = action.payload;
    },
  },
});

export const { setItem, setToken } = globalSlice.actions;
export default globalSlice.reducer;
