import NewsItem from '@components/NewsItem';
import { NewsInitialStateType } from '@reducers/news';
import Link from 'next/link';
import { useRouter } from 'next/router';

import React from 'react';
import { useSelector } from 'react-redux';
import { PostFooter, PostPageHeader, PostPageWrapper, PostWrapper } from './styles';

const PostPage: React.FC = () => {
  const router = useRouter();
  const { newsData } = useSelector((state: { news: NewsInitialStateType }) => state.news);
  return (
    <PostPageWrapper>
      <PostPageHeader>
        <div className="headerBox">
          <div className="button" onClick={() => router.back()}>
            &#60;
          </div>
          <div className="name">Attention</div>
        </div>
      </PostPageHeader>
      <PostWrapper>
        <div className="titleBox">
          <div className="title">{newsData[0].title}</div>
          <div className="date">{newsData[0].date}</div>
        </div>
        <div className="content">{newsData[0].content}</div>
      </PostWrapper>
      <Link href={newsData[0].link}>
        <PostFooter>
          <div className="footerText">기사 본문으로 가기</div>
        </PostFooter>
      </Link>
    </PostPageWrapper>
  );
};

export default PostPage;
