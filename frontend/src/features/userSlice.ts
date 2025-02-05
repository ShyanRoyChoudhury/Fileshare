import { RootState } from '../store';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
    email: string | null,
    mfaEnabled: boolean
}

const initialState: UserState = {
    email: null,
    mfaEnabled: false
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
    },
    setUserMFA: (state, action: PayloadAction<boolean>) => {
      state.mfaEnabled = action.payload;
    },
  }
});

// Export actions for dispatch
export const { setUserEmail, clearUserEmail, setUserMFA } = userSlice.actions;

// Export reducer for configureStore
export default userSlice.reducer;

// Selector to get email from state
export const selectUserEmail = (state: RootState) => state.user.email;