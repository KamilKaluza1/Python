import random

lower_case = 'abcdefghijklmnoprstuwzy'
upper_case = lower_case.upper()
numbers = '1234567890'
symbol = "!@#$%^&*()"

sings = lower_case + upper_case + numbers + symbol

password = ''.join(random.sample(sings, 15))
print(password)