from crawler.crawling import crawling_bot
from summarization.predict import Inference as SummarizationInfer
from keyword.keyBERT_mmr_keyword import KeyWordTop5
from translation.mbart_translate_final import Inference as TranslationInfer


class Server:
    def __init__(self):
        self.summary_model = SummarizationInfer()
        self.trans_model = TranslationInfer()

    def summarize_to_translate(self, text):
        """
        요약 후 번역
        :param text: Raw news article
        :return:
        """
        en_summary = self.summary_model.summarize(text)
        ko_summary = self.trans_model.translate(en_summary)

        return ko_summary

    def translate_all(self, text):
        """
        전체 기사 번역, 제목 기사 번역, 키워드 번역
        :param text: Raw news article
        :return:
        """
        ko_text = self.trans_model.translate(text)

        return ko_text


if '__main__' == __name__:
    server = Server()
    data = crawling_bot()
    ko_doc = server.translate_all(data)
    print(ko_doc)
