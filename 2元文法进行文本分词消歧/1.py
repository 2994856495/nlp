import json
tt = {"start_row": 0, "end_row": 0, "env": 0, "now": 0}

# tt=json.dumps(tt)
f=open("1.txt","r",encoding='utf-8')
tt=json.load(f)
print(type(tt))
