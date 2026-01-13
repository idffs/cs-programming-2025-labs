def find_all_common(start, end):
    if start > end:
        return 'Start can\'t be more than end'
    elif start < 1 or end < 1:
        return 'Start or end can\'t be less than 1'
    elif end == 1:
        return 'End can\'t be 1'
    
    def common(c):
        if c < 2:
            return False
        if c == 2:
            return True
        if c % 2 == 0:
            return False
        
        for i in range(3, int(c**0.5) + 1, 2):
            if c % i == 0:   
                return False
        return True
    
    commons = []
    for com in range(start, end + 1):
        if common(com):
            commons.append(com)
    
    if commons:
        return " ".join(map(str, commons))
    else:
        return 'Error'
try:
    a, b = map(int, input('Enter radius(3 5, 1 17, 8 90, etc.): ').split())
    print(find_all_common(a, b))
except ValueError:
    print('Start and end should be integers')