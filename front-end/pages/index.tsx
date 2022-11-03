import NewsItem from '@components/NewsItem';
import AppLayout from '@layouts/AppLayout';
import { NewsInitialStateType } from '@reducers/news';
import React from 'react';
import { useSelector } from 'react-redux';
import { KeywordWrapper, ListPageWrapper } from './styles';

const MainPage: React.FC = () => {
  const { keyword } = useSelector((state: { news: NewsInitialStateType }) => state.news);
  const { newsData } = useSelector((state: { news: NewsInitialStateType }) => state.news);
  return (
    <AppLayout>
      <ListPageWrapper>
        <KeywordWrapper>
          <div className="title">키워드 TOP 5</div>
          <div className="boxWrapper">
            {keyword.map((data, i) => (
              <div className="box" key={i}>
                <div className="text">{data}</div>
              </div>
            ))}
            {/* <div className="box">
              <div className="text">금리</div>
            </div>
            <div className="box">
              <div className="text">머스크</div>
            </div>
            <div className="box">
              <div className="text">김건희</div>
            </div> */}
          </div>
        </KeywordWrapper>
        {newsData.map((data, i) => (
          <NewsItem key={i} data={data} />
        ))}
        {/* <NewsItem />
        <NewsItem />
        <NewsItem />
        <NewsItem />
        <NewsItem />
        <NewsItem />
        <NewsItem />
        <NewsItem /> */}
      </ListPageWrapper>
    </AppLayout>
  );
};

export default MainPage;
