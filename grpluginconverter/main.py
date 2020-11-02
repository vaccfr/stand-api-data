import time, json
# from dms2dec.dms_convert import dms2dec
file_to_open = "lfpg.txt"
output_filename = "lfpg.json"

wake_turbulences = ['L', 'M', 'H', 'J']

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
  wtc = []
  notwtc = []
  priority = 1
  for d in filtered:
    if d[:5] == "STAND":
      lat = dms2decimal(d.split(':')[3])
      lon = dms2decimal(d.split(':')[4])
      dmslat = d.split(':')[3]
      dmslon = d.split(':')[4]
      stand_number = d.split(':')[2]
    if d == "SCHENGEN":
      schengen = True
    if d[:5] == "CALLS":
      companies = d.split(':')[1].split(',')
    if d[:3] == "USE":
      usage = list(d.split(':')[1])
    if d[:3] == "WTC":
      if len(wtc) == 0:
        wtc = list(d.split(':')[1])
      else:
        for c in list(d.split(':')[1]):
          if not c in wtc:
            wtc.append(c)
    if d[:5] == "NOTWT":
      notwtc = list(d.split(':')[1])
      for c in wake_turbulences:
        if not c in notwtc:
          wtc.append(c)
    if d[:5] == "PRIOR":
      if d.split(':')[1] == "+1":
        priority = 3
      elif d.split(':')[1] == "0":
        priority = 2
      elif d.split(':')[1] == "-1":
        priority = 1
  
  final = {
    "lat": lat,
    "lon": lon,
    "dmslat": dmslat,
    "dmslon": dmslon,
    "number": stand_number,
    "schengen": schengen,
    "companies": companies,
    "usage": usage,
    "wtc": wtc,
    "priority": priority
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