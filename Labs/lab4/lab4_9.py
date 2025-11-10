try:    
    user = int(input('Type what hour it is(0-23): '))
    if user in range(0, 6):
        print('Its night')
    elif user == 24:
        print('24:** same as 0:**, so its night')
    elif user in range(6, 12):
        print('Its morning')
    elif user in range(12, 18):
        print('Its daytime')
    elif user in range(18, 24):
        print('Its evening')
    else:
        print('Error: In day 24 hours')
except ValueError:
    print('Error: Write hour how it in example')