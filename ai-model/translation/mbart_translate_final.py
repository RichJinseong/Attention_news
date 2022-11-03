from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch

class Inference:
    def __init__(self):
        self.max_length = 1024
        self.model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
        self.tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")

    def translate(self, text):
        if len(self.tokenizer.encode(text)) >= self.max_length:
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
            translation_ids_lst = [self.model.generate(inputs, forced_bos_token_id=self.tokenizer.lang_code_to_id["ko_KR"], max_length=self.max_length) for inputs in inputs_batch_lst]
            translation_batch_lst = []
            for translated_tokens in translation_ids_lst:
                translation = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
                translation_batch_lst.append(translation)

            translation = '\n'.join(translation_batch_lst)

        if len(self.tokenizer.encode(text)) < self.max_length:
            model_inputs = self.tokenizer(text, return_tensors="pt")
            generated_tokens = self.model.generate(**model_inputs,
                                                   forced_bos_token_id=self.tokenizer.lang_code_to_id["ko_KR"],
                                                   max_length=self.max_length)
            translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

        return translation


# text1 = "PHILADELPHIA – The Houston Astros wanted to wildly celebrate Wednesday evening. They wanted to rush the mound at Citizens Bank Park, tackle closer Ryan Pressly, jump on a human dog-pile and party. It was a moment they will cherish forever, being only the second team in baseball history to pitch a no-hitter in the World Series, in their 5-0 victory over the Philadelphia Phillies. “We will celebrate,’’ Astros second baseman Jose Altuve said, “but not yet. We still have work to do. “No-hitters are cool. You don’t see no-hitters every day. But what we really wanted to do was win the game, and we did.’’ Follow every game: Live MLB Scores The Astros may have all of the momentum now, and even the favorable pitching matchups the remainder of the World Series, but with the Series tied at 2-games apiece, they want to hold off on the revelry until they win two more games for the title. “I love the no-hitter, it’s awesome,’’ Astros center fielder Chas McCormick said. “It’s really cool. But we got two more wins to go. We don’t lose sight of that. That’s when we’ll really celebrate.’’ History will have to wait, the Astros say. They helped Hall of Fame officials collect  memorabilia. They got an autographed game-used ball from starter Cristian Javier and relievers Bryan Abreu, Rafael Montero and Pressly, along with catcher Christian Vazquez. They got an Astros’ rosin bag. And a scoresheet, too, from Hall of Fame pitcher John Smoltz, the lead FOX analyst. "  * 3
# model = Inference()
# print(model.translate(text1))
