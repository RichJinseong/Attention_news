import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface CounterState {
  count: number;
  loading: boolean;
  error: boolean;
  errorMessage: string;
}

export const initialState: CounterState = {
  count: 0,
  loading: false,
  error: false,
  errorMessage: '',
};

export const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    incrementCounter: (state, action: PayloadAction<number>) => ({
      ...state,
      count: state.count + action.payload,
    }),
    decrementCounter: (state, action: PayloadAction<number>) => ({
      ...state,
      count: state.count - action.payload,
    }),
  },
});

export default counterSlice;
