from num2words import num2words

spell_digit = {'0': 'không', '1': 'một', '2': 'hai', '3': 'ba', '4': 'bốn',
               '5': 'năm', '6': 'sáu', '7': 'bảy', '8': 'tám', '9': 'chín'}
               
def number_2_word(token_unnorm):
    n = int(token_unnorm)
    # If all the digits are encountered return blank string
    if(n==0):
        return ""
     
    else:
        # compute spelling for the last digit
        small_ans = spell_digit[str(int(n%10))]
 
        # keep computing for the previous digits and add the spelling for the last digit
        ans = number_2_word(int(n/10)) + small_ans + " "
     
    # Return the final answer
    return ans

def roman_to_int(s):
  rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
  int_val = 0
  for i in range(len(s)):
    if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
      int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
    else:
      int_val += rom_val[s[i]]
  return int_val

def norm_sil(token_unnorm):
  return ''

def norm_self(token_unnorm):
  return token_unnorm

def norm_spell(token_unnorm):
  return " ".join(list(token_unnorm))

def norm_digit(token_unnorm):
  ans = ''
  non_zero = token_unnorm
  while len(non_zero) > 1 and non_zero[0] == '0':
    ans += 'không '
    non_zero = non_zero[1:]
  if len(non_zero) == 1 and non_zero[0] == '0':
    return ans + 'không'
  return ans + number_2_word(non_zero)[:-1]

def norm_cardinal(token_unnorm):
  return num2words(int(token_unnorm), lang='vi')

def norm_roman(token_unnorm):
  int_form = roman_to_int(token_unnorm.upper())
  return norm_cardinal(int_form)

def norm_AG(token_class):
  return token_class[token_class.find('_to_')+4:-3]