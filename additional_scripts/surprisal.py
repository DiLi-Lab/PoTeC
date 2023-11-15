import torch
import numpy as np
from transformers import BertTokenizerFast, BertForMaskedLM
from transformers import GPT2LMHeadModel, GPT2TokenizerFast


class SurprisalScorer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = self.load_model(model_name)
        self.tokenizer = self.get_tokenizer()
        self.score = self.get_scorer()
        self.STRIDE = 200

    def load_model(self, model_name):
        if model_name == "bert":
            return BertForMaskedLM.from_pretrained("bert-base-german-cased")
        elif model_name == "gpt":
            return GPT2LMHeadModel.from_pretrained("benjamin/gerpt2")

    def get_scorer(self):
        self.model.eval()
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        if self.model_name == "bert":
            raise NotImplementedError
        elif self.model_name == "gpt":
            return self.score_gpt
        else:
            raise NotImplementedError

    def get_tokenizer(self):
        if self.model_name == "bert":
            return BertTokenizerFast.from_pretrained("bert-base-german-cased")
        elif self.model_name == "gpt":
            return GPT2TokenizerFast.from_pretrained("benjamin/gerpt2")
        else:
            raise NotImplementedError

    def score_gpt(self, sentence, BOS=True):
        with torch.no_grad():
            all_log_probs = torch.tensor([], device=self.model.device)
            offset_mapping = []
            start_ind = 0
            while True:
                encodings = self.tokenizer(
                    sentence[start_ind:],
                    max_length=1022,
                    truncation=True,
                    return_offsets_mapping=True,
                )
                if BOS:
                    tensor_input = torch.tensor(
                        [
                            [self.tokenizer.bos_token_id]
                            + encodings["input_ids"]
                            + [self.tokenizer.eos_token_id]
                        ],
                        device=self.model.device,
                    )
                else:
                    tensor_input = torch.tensor(
                        [encodings["input_ids"] + [self.tokenizer.eos_token_id]],
                        device=self.model.device,
                    )
                output = self.model(tensor_input, labels=tensor_input)
                shift_logits = output["logits"][..., :-1, :].contiguous()
                shift_labels = tensor_input[..., 1:].contiguous()
                log_probs = torch.nn.functional.cross_entropy(
                    shift_logits.view(-1, shift_logits.size(-1)),
                    shift_labels.view(-1),
                    reduction="none",
                )
                assert torch.isclose(
                    torch.exp(sum(log_probs) / len(log_probs)),
                    torch.exp(output["loss"]),
                )
                offset = 0 if start_ind == 0 else self.STRIDE - 1
                all_log_probs = torch.cat([all_log_probs, log_probs[offset:-1]])
                offset_mapping.extend(
                    [
                        (i + start_ind, j + start_ind)
                        for i, j in encodings["offset_mapping"][offset:]
                    ]
                )
                if encodings["offset_mapping"][-1][1] + start_ind == len(sentence):
                    break
                start_ind += encodings["offset_mapping"][-self.STRIDE][1]
            return np.asarray(all_log_probs.cpu()), offset_mapping