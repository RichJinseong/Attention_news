import Header from '@components/Header';
import React, { useCallback, useState } from 'react';
import { AppLayoutWrapper, Line } from './styles';

interface Props {
  children: React.ReactNode;
}

const AppLayout: React.FC<Props> = ({ children }) => {
  return (
    <AppLayoutWrapper>
      <Header />
      <Line />
      {children}
    </AppLayoutWrapper>
  );
};

export default AppLayout;
