try:    
    user = int(input('Type what hour it is(0-23): '))
    if user < 0:
        print('Error: No negative values')
    if user in range(0, 6):
        print('It\'s night')
    elif user == 24:
        print("""24:** same as 0:**
It\'s night""")
    elif user in range(6, 12):
        print('It\'s morning')
    elif user in range(12, 18):
        print('It\'s daytime')
    elif user in range(18, 24):
        print('It\'s evening')
    else:
        print('Error: In day 24 hours')
except ValueError:
    print('Error: Write hour how it in example')