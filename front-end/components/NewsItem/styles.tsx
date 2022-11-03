import styled from 'styled-components';

export const NewsItemWrapper = styled.div`
  width: 95%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  border-bottom: solid 1px #bebebe;
  padding: 10px 0px;
  cursor: pointer;

  & .title {
    width: 80%;
    font-size: 15px;
    color: black;
    font-family: 'AppleSDGothicNeoM';
  }
  & .footer {
    width: 100%;
    margin-top: 5px;
    font-size: 12px;
    display: flex;
    justify-content: start;
    font-family: 'AppleSDGothicNeoM';

    & .about {
      font-size: 13px;
      color: #707070;
      margin-right: 5px;
    }
  }
`;
