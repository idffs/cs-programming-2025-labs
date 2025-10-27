user = int(input('Type what hour is(0-23): '))
if user in range(0, 6):
    print('Its night')
elif user in range(6, 12):
    print('Its morning')
elif user in range(12, 18):
    print('Its daytime')
elif user in range(18, 24):
    print('Its evening')