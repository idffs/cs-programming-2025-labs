incidents = [
    {"id": 101, "staff": 4},
    {"id": 102, "staff": 12},
    {"id": 103, "staff": 7},
    {"id": 104, "staff": 20}
]

sorted_i = sorted(incidents, key=lambda x: x['staff'], reverse=True)
top_3 = sorted_i[:3]
print(sorted_i)
print(top_3)