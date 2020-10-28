import time, json
# from dms2dec.dms_convert import dms2dec
file_to_open = "sialfpg.txt"
output_filename = "lfpg.json"

def main(file_to_open):
  data = []
  with open(file_to_open, 'r') as file:
    for l in file:
      line = l.rstrip()
      if line:
        data.append(line)
    file.close()
  for d in data:
    print(d)
  return json.dumps(main_loop(data))

def main_loop(data):
  stands = []
  for d in data:
    stands.append({
      "stand": d.split(' ')[0],
      "lat": dms2decimal(d.split(' ')[1]),
      "lon": dms2decimal(d.split(' ')[2])
    })
  return stands

def dms2decimal(coord):
  multiplier = 1
  if coord[-1:] == "S" or coord[-1:] == "W":
    multiplier = -1
  degree = coord.split('°')[0]
  hour = coord.split('°')[1].split("'")[0]
  minute = coord.split('°')[1].split("'")[1].split('.')[0]
  second = coord.split('°')[1].split("'")[1].split('.')[1].split('"')[0]
  return (int(degree) + (int(hour) / 60) + (float(f"{minute}.{second}") / 3600)) * multiplier

ts = time.time()
result = main(file_to_open)
with open(output_filename, "w") as file:
  print(result, file=file)
  file.close()
te = time.time()
print(f"Lapse: {te-ts}")