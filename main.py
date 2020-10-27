
file_to_open = "lfpg.txt"

def main(file_to_open):
  data = []
  with open(file_to_open, 'r') as file:
    for l in file:
      line = l.rstrip()
      if line:
        data.append(line)
    file.close()
  main_loop(data)

def main_loop(data):
  # This function takes the raw stripped lines of the file and parses them
  stands = []
  filtered = []
  starting_index = 0
  for idx, val in enumerate(data):
    if val[:5] == "STAND":
      if not len(filtered) == 0:
        print(f"NEW DATA!")
        print(filtered)
        print(f"\n")
        parser(filtered)
        filtered = []
      starting_index = idx
      filtered.append(val)
    elif not val[:2] == "//":
      filtered.append(val)
  
def parser(filtered):
  pass

main(file_to_open)
