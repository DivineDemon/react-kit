import { createSlice } from "@reduxjs/toolkit";

const initialState: GlobalState = {
  token: null,
  profile_picture: null,
};

const globalSlice = createSlice({
  name: "global",
  initialState,
  reducers: {
    setProfilePicture: (state, action) => {
      state.profile_picture = action.payload;
    },
    setToken: (state, action) => {
      state.token = action.payload;
    },
  },
});

export const { setProfilePicture, setToken } = globalSlice.actions;
export default globalSlice.reducer;
