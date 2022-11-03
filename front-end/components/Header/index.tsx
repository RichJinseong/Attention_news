import React, { useCallback, useState } from 'react';
import { Category, HeaderWrapper, Title } from './styles';

const Header: React.FC = () => {
  const [active, setActive] = useState(0);

  const onClickCategory = useCallback(
    (data: number) => {
      setActive(data);
    },
    [active],
  );
  return (
    <HeaderWrapper>
      <Title>Attention</Title>
      <Category>
        <div className={active === 0 ? 'field' : 'non-active'} onClick={() => onClickCategory(0)}>
          카테고리
        </div>
        <div className={active === 1 ? 'field' : 'non-active'} onClick={() => onClickCategory(1)}>
          카테고리
        </div>
        <div className={active === 2 ? 'field' : 'non-active'} onClick={() => onClickCategory(2)}>
          카테고리
        </div>
        <div className={active === 3 ? 'field' : 'non-active'} onClick={() => onClickCategory(3)}>
          카테고리
        </div>
      </Category>
    </HeaderWrapper>
  );
};

export default Header;
