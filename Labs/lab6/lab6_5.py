def check_for_palindrom(a):
    clear = ''.join(char.lower() for char in a if char.isalnum())
    if clear == clear[::-1]:  
        return 'Yes, it\'s palindrom'
    else:
        return 'No, it\'s not palindrom'
user = str(input('Enter your sentence: '))
print(check_for_palindrom(user))