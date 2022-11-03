/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  env: {
    KAKAO_REST_API: process.env.KAKAO_REST_API,
    NAVER_CLIENT_ID: process.env.NAVER_CLIENT_ID,
    GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID,
  },
};
