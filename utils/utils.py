import torch
from tokenizer import tokenizer
from normalize import *
from accept import *
import torch.nn as nn

def encoding(sentences, word_to_ix, max_len):
  x_ids = []

  for sentence in sentences:
    encode_sentence = []
    for token in sentence:
      if re.search("^[0-9]+$",token) == None:
        encode_sentence.append(word_to_ix.get(token,word_to_ix['<UNKNOWN_WORD>']))
      else:
        encode_sentence.append(word_to_ix.get(token,word_to_ix['<NUMBER>']))
    for i in range(max_len-len(sentence)):
      encode_sentence.append(word_to_ix['<PADDING>'])
    x_ids.append(encode_sentence)

  return x_ids

def token_classification(list_accept_class, prob_softmax, class_to_ix):
  ix_to_class = list(class_to_ix.keys())
  list_class_pred = []

  for j in range(len(list_accept_class)):
    sentence = list_accept_class[j]
    classes = []
    for i in range(len(sentence)):
      temp = torch.zeros(len(class_to_ix)).to("cuda")
      temp[sentence[i]] = 1
      res = prob_softmax[j][i]*temp
      classes.append(ix_to_class[res.argmax(dim=0)])
    list_class_pred.append(classes)

  return list_class_pred

def token_normalization(sentences, list_class_pred):
  norm_pred = []

  for i in range(len(sentences)):
    norm_token_pred = []
    for j in range(len(sentences[i])):
      token = sentences[i][j]
      if 'AG' in list_class_pred[i][j]:
        norm_token_pred.append(norm_AG(list_class_pred[i][j]))
      elif list_class_pred[i][j] != 'sil' and list_class_pred[i][j] != '<PADDING>':
        norm_token_pred.append(eval("norm_"+ list_class_pred[i][j] +"(token)"))
    norm_pred.append(norm_token_pred)

  return norm_pred

def normalization(model, unnorm_sentences):
  sentences = tokenizer(unnorm_sentences)

  x_ids = encoding(sentences)

  list_accept_class = accept_class(sentences)

  func_softmax = nn.Softmax(dim=-1)
  xb = torch.tensor(x_ids).to("cuda")
  prob = model.forward(xb)
  prob_softmax =  func_softmax(prob)

  list_class_pred = token_classification(list_accept_class, prob_softmax)

  norm_pred = token_normalization(sentences, list_class_pred)
  
  return norm_pred

def predict_class(model, unnorm_token):
  x_ids = encoding(unnorm_token)

  list_accept_class = accept_class(unnorm_token)

  func_softmax = nn.Softmax(dim=-1)
  xb = torch.tensor(x_ids).to("cuda")
  prob = model.forward(xb)
  prob_softmax =  func_softmax(prob)

  list_class_pred = token_classification(list_accept_class, prob_softmax)
  
  return list_class_pred

def batch_normalization(model, unnorm_token):
  class_pred = []

  i = 0
  max_idx = len(unnorm_token) - 1
  while i < max_idx//100:
    left = 100*i
    right = 100*i + 100 
    pred = predict_class(model, unnorm_token[left:right])
    for sentence in pred:
      temp = []
      for c in sentence:
        temp.append(c)
      class_pred.append(temp)
    gc.collect()
    torch.cuda.empty_cache()
    i += 1

  pred = predict_class(model, unnorm_token[100*i:])
  for sentence in pred:
    temp = []
    for c in sentence:
      temp.append(c)
    class_pred.append(temp)
  gc.collect()
  torch.cuda.empty_cache()
  
  return class_pred

def wer_calculation(model, unnorm_token, norm_token):
  # unnorm_data: List[List[token]]
  # class_actl: List[List[class]]

  class_pred = batch_normalization(model, unnorm_token)

  #norm_actl = token_normalization(unnorm_data, class_actl)
  norm_pred_data = token_normalization(unnorm_token, class_pred)
  norm_pred = [" ".join(x) for x in norm_pred_data]
  norm_actual = [" ".join(x) for x in norm_token]
  return word_error_rate(preds=norm_pred, target=norm_actual)