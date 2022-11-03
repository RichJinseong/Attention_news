import pytorch_lightning as pl
from transformers import (
    AdamW, BartTokenizer, BartForConditionalGeneration
)
import torch


class NewsSummaryModel(pl.LightningDataModule):
    def __init__(self):
        super().__init__()
        self.model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn", return_dict=True)

    def forward(self, input_ids, attention_mask, decoder_attention_mask, labels=None):

        output = self.model(
            input_ids,
            attention_mask=attention_mask,
            labels=labels,
            decoder_attention_mask=decoder_attention_mask
        )

        return output.loss, output.logits

    def training_step(self, batch, batch_idx):
        input_ids = batch['text_input_ids']
        attention_mask = batch['text_attention_mask']
        labels = batch['labels']
        labels_attention_mask = batch['labels_attention_mask']

        loss, outputs = self(
            input_ids=input_ids,
            attention_mask=attention_mask,
            decoder_attention_mask=labels_attention_mask,
            labels=labels
        )

        self.log('train_loss', loss, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        input_ids = batch['text_input_ids']
        attention_mask = batch['text_attention_mask']
        labels = batch['labels']
        labels_attention_mask = batch['labels_attention_mask']

        loss, outputs = self(
            input_ids=input_ids,
            attention_mask=attention_mask,
            decoder_attention_mask=labels_attention_mask,
            labels=labels
        )

        self.log('val_loss', loss, prog_bar=True, logger=True)
        return loss

    def test_step(self, batch, batch_idx):
        input_ids = batch['text_input_ids']
        attention_mask = batch['text_attention_mask']
        labels = batch['labels']
        labels_attention_mask = batch['labels_attention_mask']

        loss, outputs = self(
            input_ids=input_ids,
            attention_mask=attention_mask,
            decoder_attention_mask=labels_attention_mask,
            labels=labels
        )

        self.log('test_loss', loss, prog_bar=True, logger=True)
        return loss

    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=0.0001)


class Inference:
    def __init__(self):
        self.trained_model = NewsSummaryModel.load_from_checkpoint(model_path)
        # self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    def summarize(self, text):
        text_len = len(self.tokenizer.encode(text))

        if text_len >= 1200:
            inputs_no_trunc = self.tokenizer(text, max_length=None, return_tensors='pt', truncation=False)
            chunk_start = 0
            chunk_end = self.tokenizer.model_max_length  # == 1024 for Bart
            inputs_batch_lst = []
            while chunk_start <= len(inputs_no_trunc['input_ids'][0]):
                inputs_batch = inputs_no_trunc['input_ids'][0][chunk_start:chunk_end]  # get batch of n tokens
                inputs_batch = torch.unsqueeze(inputs_batch, 0)
                inputs_batch_lst.append(inputs_batch)
                chunk_start += self.tokenizer.model_max_length  # == 1024 for Bart
                chunk_end += self.tokenizer.model_max_length  # == 1024 for Bart

            # generate a summary on each batch
            summary_ids_lst = [self.trained_model.model.generate(inputs, num_beams=4, max_length=256, early_stopping=True) for inputs in inputs_batch_lst]
            # summary_ids_lst = [self.model.generate(inputs, num_beams=4, max_length=256, early_stopping=True) for inputs in inputs_batch_lst]

            # decode the output and join into one string with one paragraph per summary batch
            summary_batch_lst = []
            for summary_id in summary_ids_lst:
                summary_batch = [self.tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_id]
                summary_batch_lst.append(summary_batch[0])
            summary_all = '\n'.join(summary_batch_lst)
        if text_len < 1500:
            inputs = self.tokenizer(text, mask_token=1024, truncation=True, return_tensors='pt')
            generated_ids = self.trained_model.model.generate(inputs['input_ids'], num_beams=4, max_length=256, early_stopping=True)
            # generated_ids = self.model.generate(inputs['input_ids'], num_beams=4, max_length=256, early_stopping=True)
            preds = [self.tokenizer.decode(gen_id, skip_special_tokens=True, clean_up_tokenization_spaces=False) for gen_id in generated_ids]
            summary_all = "".join(preds)

        return summary_all

