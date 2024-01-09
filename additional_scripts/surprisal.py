import os
os.environ['CUDA_VISIBLE_DEVICES'] = "1,2,3"
import torch
import numpy as np
from transformers import BertTokenizerFast, BertForMaskedLM, GPT2LMHeadModel, GPT2TokenizerFast, AutoModelForCausalLM, AutoTokenizer
from typing import List, Tuple
device = "cuda" if torch.cuda.is_available() else "cpu"

class LMScorerBase:
    def __init__(self):
        self.model = self.load_model()
        self.tokenizer = self.get_tokenizer()
        self.score = self.get_scorer()
        self.STRIDE = 200

    def load_model(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_tokenizer(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_scorer(self):
        raise NotImplementedError("Subclasses must implement this method")

    def score_generative_lm(self, sentence, BOS=True):
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
        
    def score_maskedlm(self, sentence):
        # TODO CHECK MASK
        mask_id = self.tokenizer.convert_tokens_to_ids('[MASK]')
        with torch.no_grad():
            all_log_probs = []
            offset_mapping = []
            start_ind = 0
            while True:
                encodings = self.tokenizer(sentence[start_ind:], max_length=500, truncation=True, return_offsets_mapping=True)
                tensor_input = torch.tensor([encodings['input_ids']], device=self.model.device)
                mask_input = tensor_input.clone()
                offset = 1 if start_ind == 0 else self.STRIDE
                while offset_mapping and encodings['offset_mapping'][offset][0] + start_ind > offset_mapping[-1][1] + 1:
                    offset -= 1
                for i, word in enumerate(encodings['input_ids'][:-1]):
                    if i < offset:
                        continue
                    mask_input[:,i]=mask_id
                    output = self.model(mask_input, labels=tensor_input)
                    log_probs = torch.nn.functional.log_softmax(output['logits'][:,i], dim=-1).squeeze(0)
                    all_log_probs.append(-log_probs[tensor_input[0,i]].item())
                    mask_input[:,i] = word
                offset_mapping.extend([(i+start_ind, j+start_ind) for i,j in encodings['offset_mapping'][offset:-1]])
                if encodings['offset_mapping'][-2][1] + start_ind >= (len(sentence)-1):
                    break
                start_ind += encodings['offset_mapping'][-self.STRIDE-1][1]
                
            return np.asarray(all_log_probs), offset_mapping


class GPTBScorer(LMScorerBase):
    def __init__(self):
        super().__init__()
        self.name = "gpt2-base"

    def load_model(self):
        model = GPT2LMHeadModel.from_pretrained("benjamin/gerpt2")
        model.to(device)
        model.eval()
        return model

    def get_tokenizer(self):
        return GPT2TokenizerFast.from_pretrained("benjamin/gerpt2")
    
    def get_scorer(self):
        return self.score_generative_lm
    

class GPTLScorer(LMScorerBase):
    def __init__(self):
        super().__init__()
        self.name = "gpt2-large"

    def load_model(self):
        model = GPT2LMHeadModel.from_pretrained("benjamin/gerpt2-large")
        model.to(device)
        model.eval()
        return model

    def get_tokenizer(self):
        return GPT2TokenizerFast.from_pretrained("benjamin/gerpt2-large")
    
    def get_scorer(self):
        return self.score_generative_lm


class Llama7Scorer(LMScorerBase):
    def __init__(self):
        super().__init__()
        self.name = "llama-7b"

    def load_model(self):
        # to device not necessary for llama
        model = AutoModelForCausalLM.from_pretrained(
            "LeoLM/leo-hessianai-7b",
            device_map="auto",
            torch_dtype=torch.float16,
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16)
        model.eval()
        return model
    
    def get_tokenizer(self):
        return AutoTokenizer.from_pretrained("LeoLM/leo-hessianai-7b")
    
    def get_scorer(self):
        return super().score_generative_lm
    
class Llama13Scorer(LMScorerBase):
    def __init__(self):
        super().__init__()
        self.name = "llama-13b"

    def load_model(self):
        # to device not necessary for llama
        model = AutoModelForCausalLM.from_pretrained(
            "LeoLM/leo-hessianai-13b",
            device_map="auto",
            torch_dtype=torch.float16,
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16)
        model.eval()
        return model

    def get_scorer(self):
        return super().score_generative_lm
    
    def get_tokenizer(self):
        return AutoTokenizer.from_pretrained("LeoLM/leo-hessianai-13b")


class BERTScorer(LMScorerBase):
    # TODO for BERT use cased text
    def __init__(self):
        super().__init__()
        self.name = "bert-base"

    def load_model(self):
        model = BertForMaskedLM.from_pretrained("bert-base-german-cased")
        model.to(device)
        model.eval()
        return model

    def get_tokenizer(self):
        return BertTokenizerFast.from_pretrained("bert-base-german-cased")
    
    def get_scorer(self):
        return super().score_maskedlm


class MultiLMScorer:
    def __init__(self):
        self.model_classes = [GPTBScorer, GPTLScorer, Llama7Scorer, Llama13Scorer, BERTScorer]
        # self.model_classes = [BERTScorer]

    def load_models(self):
        for model in self.model_classes:
            yield model()

    def __len__(self):
        return len(self.model_classes)