import styled from 'styled-components';

export const PostPageWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
`;

export const PostPageHeader = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: end;
  border-bottom: solid 1px #707070;

  & .headerBox {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 95%;
    margin: 20px 0px;
    font-size: 28px;
    font-family: 'NanumSquareAcEB';
  }
  & .button {
    width: 32%;
    text-align: start;
    font-size: 25px;
    cursor: pointer;
  }
  & .name {
    text-align: start;
    width: 68%;
    font-size: 20px;
  }
`;

export const PostWrapper = styled.div`
  width: 95%;
  margin: 0 auto;
  display: flex;
  height: 90vh;
  overflow: auto;
  margin-top: 20px;
  /* align-items: center; */
  flex-direction: column;

  & .titleBox {
    margin-bottom: 20px;
    & .title {
      font-family: 'AppleSDGothicNeoM';
      font-size: 18px;
    }
    & .date {
      font-family: 'AppleSDGothicNeoM';
      margin-top: 5px;
      font-size: 11px;
      color: #707070;
    }
  }
  & .content {
    font-family: 'AppleSDGothicNeoL';
    font-size: 15px;
    word-spacing: 1px;
    line-height: 22px;
    padding-bottom: 100px;
  }
`;

export const PostFooter = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  bottom: 0;
  background-color: white;
  padding: 15px 0px;
  box-shadow: 3px 3px 5px 5px #dddcdc;
  border-radius: 10px 10px 0px 0px;
  cursor: pointer;

  & .footerText {
    font-family: 'AppleSDGothicNeoL';
    font-size: 25px;
    /* color: #3b3b3b; */
  }
`;
