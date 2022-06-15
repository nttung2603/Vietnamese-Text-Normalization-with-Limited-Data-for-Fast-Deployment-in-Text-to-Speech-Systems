import unicodedata

def tokenizer(unnorm_sentences):
  unnorm_tokens = []

  for i in range(len(unnorm_sentences)):
    raw_sentence = unnorm_sentences[i]
    chars = list(raw_sentence)
    chars2 = []
    j = 0
    while j < len(chars):
      if (j + 1 < len(chars)):
        if 'P' in unicodedata.category(chars[j]):
          chars2.extend([chars[j], ' '])
        elif unicodedata.category(chars[j]) not in ('Ll', 'Lu', 'Mn'):
          if unicodedata.category(chars[j]) != unicodedata.category(chars[j+1]):
            chars2.extend([chars[j], ' '])
          else:
            chars2.append(chars[j])
        else:
          if unicodedata.category(chars[j+1]) not in ('Ll', 'Lu', 'Mn'):
            chars2.extend([chars[j].lower(), ' '])
          else:
            chars2.append(chars[j].lower())
      else:
        chars2.append(chars[j].lower())

      j += 1
    new_sentence = "".join(chars2)
    unnorm_tokens.append(new_sentence.split())
  return unnorm_tokens