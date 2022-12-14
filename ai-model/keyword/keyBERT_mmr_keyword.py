# -*- coding: utf-8 -*-
"""mBART_nmt_word.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M1OlZ8qshisLVSSmV6mrqlDT6ED50iPe

## keyBERT 키워드 추출

https://wikidocs.net/159467

## install*
"""

!pip install sentence_transformers

"""## Max Sum Similarity

10개의 키워드를 선택하고, 이 10개 중에서 서로 가장 유사성이 낮은 5개를 선택합니다. 낮은 nr_candidates를 설정하면 결과는 출력된 키워드 5개는 
기존의 코사인 유사도만 사용한 것과 매우 유사한 것으로 보입니다.
"""

def max_sum_sim(doc_embedding, candidate_embeddings, words, top_n, nr_candidates):
    # 문서와 각 키워드들 간의 유사도
    distances = cosine_similarity(doc_embedding, candidate_embeddings)

    # 각 키워드들 간의 유사도
    distances_candidates = cosine_similarity(candidate_embeddings, 
                                            candidate_embeddings)

    # 코사인 유사도에 기반하여 키워드들 중 상위 top_n개의 단어를 pick.
    words_idx = list(distances.argsort()[0][-nr_candidates:])
    words_vals = [candidates[index] for index in words_idx]
    distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

    # 각 키워드들 중에서 가장 덜 유사한 키워드들간의 조합을 계산
    min_sim = np.inf
    candidate = None
    for combination in itertools.combinations(range(len(words_idx)), top_n):
        sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
        if sim < min_sim:
            candidate = combination
            min_sim = sim

    return [words_vals[idx] for idx in candidate]

# 상대적으로 높은 nr_candidates는 더 다양한 키워드 5개를 만듭니다.
# max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n=5, nr_candidates=20)

# max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n=5, nr_candidates=10)

"""## Maximal Marginal Relevance

MMR은 텍스트 요약 작업에서 중복을 최소화하고 결과의 다양성을 극대화하기 위해 노력합니다. 
참고 자료 : EmbedRank(https://arxiv.org/pdf/1801.04470.pdf) 라는 키워드 추출 알고리즘은 키워드/키프레이즈를 다양화하는 데 사용할 수 있는 MMR을 구현. 

먼저 문서와 가장 유사한 키워드/키프레이즈를 선택합니다. 
그런 다음 문서와 유사하고 이미 선택된 키워드/키프레이즈와 유사하지 않은 새로운 후보를 반복적으로 선택합니다.
"""

def mmr(doc_embedding, candidate_embeddings, words, top_n, diversity):

    # 문서와 각 키워드들 간의 유사도가 적혀있는 리스트
    word_doc_similarity = cosine_similarity(candidate_embeddings, doc_embedding)

    # 각 키워드들 간의 유사도
    word_similarity = cosine_similarity(candidate_embeddings)

    # 문서와 가장 높은 유사도를 가진 키워드의 인덱스를 추출.
    # 만약, 2번 문서가 가장 유사도가 높았다면
    # keywords_idx = [2]
    keywords_idx = [np.argmax(word_doc_similarity)]

    # 가장 높은 유사도를 가진 키워드의 인덱스를 제외한 문서의 인덱스들
    # 만약, 2번 문서가 가장 유사도가 높았다면
    # ==> candidates_idx = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10 ... 중략 ...]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    # 최고의 키워드는 이미 추출했으므로 top_n-1번만큼 아래를 반복.
    # ex) top_n = 5라면, 아래의 loop는 4번 반복됨.
    for _ in range(top_n - 1):
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # MMR을 계산
        mmr = (1-diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # keywords & candidates를 업데이트
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [words[idx] for idx in keywords_idx]

# mmr(doc_embedding, candidate_embeddings, candidates, top_n=5, diversity=0.7)

"""## DOC Word : CountVectorizer"""

import numpy as np
import itertools

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

import os
# google drive mount
from google.colab import drive
drive.mount('/content/drive')


nmt_dir = '/content/drive/MyDrive/goorm'
os.listdir(nmt_dir)

import json

with open("/content/drive/MyDrive/goorm/news_data.json", "r", encoding="utf8") as f:
    json_data = json.load(f)

# print(json_data[0]["category"]) # category 정보를 조회
# print(json_data[0]["headline"]) # category 정보를 조회
# print(json_data[0]["content"]) # category 정보를 조회
# print(json_data[0]["date"]) # category 정보를 조회

doc = json_data[0]["content"]

# doc.split()

# def listToWord(str_list):
#     doc = "" 
#     str_list= str_list.split()
#     for s in str_list:
#         doc += s + " "
#     return doc.strip()

pattern = "(?u)\\b[\\w-]+\\b"

# 2개의 단어 묶음인 단어구 추출
n_gram_range = (2, 2)
stop_words = "english"

count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words, token_pattern=pattern).fit([doc])
candidates = count.get_feature_names_out()

model = SentenceTransformer('distilbert-base-nli-mean-tokens')
doc_embedding = model.encode([doc])
candidate_embeddings = model.encode(candidates)

def KeyWordTop5(text):   
    
    KeyWord_Top5 = mmr(doc_embedding, candidate_embeddings, candidates, top_n=5, diversity=0.7)
    
    return KeyWord_Top5

# print('trigram 개수 :',len(candidates))
# print('trigram 다섯개만 출력 :',candidates[:5])

"""## 일반 문서와 가장 유사한 키워드 추출 : Top 5

이 프로젝트에서는 가장 유사한 키워드와 Maximal Marginal Relevance 중 선택 필요!
"""

# 문서와 가장 유사한 키워드들 추출.  상위 5개의 키워드를 출력합니다.
# 문서와 가장 유사한 키워드들은 문서를 대표하기 위한 좋은 키워드라고 가정합니다.
top_n = 5
distances = cosine_similarity(doc_embedding, candidate_embeddings)
keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
# print(keywords)

"""## 배포"""

print(KeyWordTop5(doc))