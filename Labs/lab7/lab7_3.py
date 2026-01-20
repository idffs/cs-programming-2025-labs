personnel = [
    {"name": "Dr. Klein", "clearance": 2},
    {"name": "Agent Brooks", "clearance": 4},
    {"name": "Technician Reed", "clearance": 1}
]

res = list(map(lambda x: {'name': x['name'], 'clearance': x['clearance'], 'category': 'Restricted' if x['clearance'] == 1 
                          else 'Confidential' if 2 <= x['clearance'] <= 3 
                          else 'Top Secret' if x['clearance'] >= 4 
                          else 'Broken Code'}, personnel))
print(res)