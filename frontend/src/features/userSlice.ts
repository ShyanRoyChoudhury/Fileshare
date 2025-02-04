import { RootState } from '../store';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
    email: string | null
}

const initialState: UserState = {
    email: null
  };
  

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUserEmail: (state, action: PayloadAction<string | null>) => {
        state.email = action.payload || null;
      },
    clearUserEmail: (state) => {
      state.email = null;
    }
  }
});

// Export actions for dispatch
export const { setUserEmail, clearUserEmail } = userSlice.actions;

// Export reducer for configureStore
export default userSlice.reducer;

// Selector to get email from state
export const selectUserEmail = (state: RootState) => state.user.email;