#Dict, where a key - first symbol and value - words that writing from that symbol 
a = ["apple", "pear", "banana", "qiwi", "orange", "ananas"]
print(a)
l = len(a)
res = {}
for word in a:
    f_s = word[0]
    if f_s not in res:
        res[f_s] = [word]
    else:
        res[f_s].append(word)
print(res)