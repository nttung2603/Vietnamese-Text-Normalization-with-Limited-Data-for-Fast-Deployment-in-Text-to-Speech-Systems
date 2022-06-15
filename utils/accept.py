import unicodedata
import re

def accept_sil(token, class_name = None):
  if(len(token) != 1):
    return False
  first_char_uni = unicodedata.category(token)[0]
  if ( first_char_uni == 'P' or first_char_uni == 'S'):
    return "sil"
  else:
    return False

def accept_self(token, class_name = None):
  if (token.isalpha()):
    return "self"
  else:
    return False

def accept_spell(token, class_name = None):
  if (token.isalpha()):
    return "spell"
  else:
    return False

def accept_roman(token, class_name = None):
  if (re.search("^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$",token.upper()) != None):
    return "roman"
  else:
    return False

def accept_digit(token, class_name = None):
  if (re.search("^[0-9]+$",token) != None):
    return "digit"
  else:
    return False

def accept_cardinal(token, class_name = None):
  if (re.search("^[0-9]+$",token) != None):
    return "cardinal"
  else:
    return False

def accept_class(sentences, class_to_ix):
  list_accept_class = []

  for sentence in sentences:
    accept_sentence = []
    for token in sentence:
      temp = []
      for class_name in class_to_ix.keys():
        result = False
        if "AG" in class_name:
          key =  class_name.split("_to_")[0]
          if token == key:
            temp.append(class_to_ix[class_name])
        elif "roman" in class_name:
          result = eval("accept_roman(token)")
        elif class_name != "<PADDING>":
          result = eval("accept_"+ class_name +"(token)")
        if result != False:
            temp.append(class_to_ix[class_name])
      accept_sentence.append(temp)
    list_accept_class.append(accept_sentence)
  
  return list_accept_class