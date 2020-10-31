import json

with open("lfpg.json", "r") as file:
  data = json.load(file)
  file.close()

for d in data:
  print(f"{d['number']} accepte les companies: {d['companies']}")