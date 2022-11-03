import styled from 'styled-components';

export const ListPageWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: auto;
`;

export const KeywordWrapper = styled.div`
  width: 95%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  padding: 20px 0px;

  & .boxWrapper {
    width: 100%;
    display: flex;
    margin-top: 10px;
    justify-content: space-between;

    & .box {
      width: 22%;
      height: 27px;
      border-radius: 25px;
      border: solid 1px #fcb0b0;
      display: flex;
      align-items: center;
      justify-content: center;

      & .text {
        font-family: 'NanumSquareR';
        font-size: 12px;
        color: #fd5a5a;
      }
    }
  }
  & .title {
    font-family: 'NanumSquareR';
    font-size: 13px;
  }
`;
