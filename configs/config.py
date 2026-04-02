import json

cfg =  None
with open("configs/buttons_names.json","r") as f:
    buttons_names = json.load(f)
    cfg = buttons_names

