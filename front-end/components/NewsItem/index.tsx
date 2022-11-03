import Link from 'next/link';
import React, { useCallback, useState } from 'react';
import { NewsItemWrapper } from './styles';

interface Props {
  data: {
    title: string;
    link: string;
    date: string;
    content: string;
    category: string;
  };
}

const NewsItem: React.FC<Props> = ({ data }) => {
  const [active, setActive] = useState(0);

  const onClickCategory = useCallback(
    (data: number) => {
      setActive(data);
    },
    [active],
  );

  const title =
    '이게 나라냐 남영희 또 폭탄발언 , 이태원 참사 신고 녹취록 공개 더이상 참을 수 없습니다 머리 속에 뭐가 들어있는지 ';

  return (
    <Link href="/post">
      <NewsItemWrapper>
        {data.title.length > 50 ? (
          <div className="title"> {data.title.substring(0, 50)}...</div>
        ) : (
          <div className="title">{data.title}</div>
        )}
        <div className="footer">
          <div className="about">{data.category}</div>
          <div className="about">{data.date}</div>
        </div>
      </NewsItemWrapper>
    </Link>
  );
};

export default NewsItem;
