import time, json
# from dms2dec.dms_convert import dms2dec
file_to_open = "lfmn.txt"
output_filename = "lfmn.json"

def main(file_to_open):
  data = []
  with open(file_to_open, 'r') as file:
    for l in file:
      line = l.rstrip()
      if line:
        data.append(line)
    file.close()
  return json.dumps(main_loop(data))

def main_loop(data):
  # This function takes the raw stripped lines of the file and parses them
  stands = []
  filtered = []
  starting_index = 0
  for idx, val in enumerate(data):
    if val[:5] == "STAND":
      if not len(filtered) == 0:
        final_Data = parser(filtered)

        stands.append(final_Data)
        filtered = []
      starting_index = idx
      filtered.append(val)
    elif not val[:2] == "//":
      filtered.append(val)
  
  return stands
  
def parser(filtered):
  schengen = False
  companies = []
  usage = []
  for d in filtered:
    if d[:5] == "STAND":
      lat = dms2decimal(d.split(':')[3])
      lon = dms2decimal(d.split(':')[4])
      stand_number = d.split(':')[2]
    if d == "SCHENGEN":
      schengen = True
    if d[:5] == "CALLS":
      companies = d.split(':')[1].split(',')
    if d[:3] == "USE":
      usage = list(d.split(':')[1])
  
  final = {
    "lat": lat,
    "lon": lon,
    "number": stand_number,
    "schengen": schengen,
    "companies": companies,
    "usage": usage
  }
  return final

def dms2decimal(coord):
  card = coord[:1]
  coord = coord[1:]
  wip = coord.split('.')
  wip.append(card)
  multiplier = 1
  if card == "S" or card == "W":
    multiplier = -1
  return (int(wip[0]) + (int(wip[1]) / 60) + (float(f"{wip[2]}.{wip[3]}") / 3600)) * multiplier
  

ts = time.time()
result = main(file_to_open)
with open(output_filename, "w") as file:
  print(result, file=file)
  file.close()
te = time.time()
print(f"Lapse: {te-ts}")