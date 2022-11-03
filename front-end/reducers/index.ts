import { combineReducers, AnyAction } from '@reduxjs/toolkit';

import { HYDRATE } from 'next-redux-wrapper';
import { AppState } from '../store/configureStore';
import counterSlice, { initialState as counterState } from './couter/couterSlice';
import NewsSlice from './news';

const rootReducer = combineReducers({
  counter: counterSlice.reducer,
  news: NewsSlice.reducer,
  // spotPost: PostSlice.reducer,
});

export const preloadedState = () => {
  return { counter: counterState };
};

export const reducer = (state: AppState, action: AnyAction) => {
  if (action.type === HYDRATE) {
    return {
      ...state,
      ...action.payload,
    };
  }
  return rootReducer(state, action);
};

export default rootReducer;
