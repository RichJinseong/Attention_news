from predict import Inference
from datasets import load_dataset
from rouge_score import rouge_scorer

score_list = []
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
# 데이터
raw_datasets = load_dataset('cnn_dailymail', '3.0.0')
test_dataset = raw_datasets['test'][:10]

import time
start = time.time()
model = Inference(model_path='./model/bart-large-cnn-512length.ckpt')
mid = time.time()
for i in range(10):
    model_summary = model.summarize(test_dataset['article'][i])
    print('정답 : ')
    print(test_dataset['highlights'][i])
    print(' ')
    print('추론 : ')
    print(model_summary)
    print(' ')
    print('----------------------------')
    score_list.append(scorer.score(test_dataset['highlights'][i], model_summary))
end = time.time()
print('mid : ', mid - start)
print('end : ', end - mid)
print('total : ', end - start)

print(score_list)
print(score_list[0]['rouge1']['precision'])
# print(sum(score_list[0]['rouge1']['precision']) / len(score_list))

