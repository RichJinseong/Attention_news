import styled from 'styled-components';

export const HeaderWrapper = styled.div`
  width: 95%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
`;

export const Title = styled.div`
  width: 100%;
  margin: 20px 0px;
  font-size: 28px;
  font-family: 'NanumSquareAcEB';
`;

export const Category = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;

  & .non-active {
    font-size: 13px;
    color: #707070;
    padding-bottom: 10px;
    font-family: 'NanumSquareR';
    cursor: pointer;
  }

  & .field {
    font-size: 13px;
    padding-bottom: 10px;
    font-family: 'NanumSquareR';
    border-bottom: solid 2px #707070;
  }
`;
