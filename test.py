import requests
import csv
import allel

def variant_request(variant):
  try:
    response = requests.get(f"https://api.genohub.org/v1/rsids/{variant}")
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    return None


def make_CSV(dic_list):
    keys = dic_list[0].keys()  # Assuming the dictionaries have the same keys
    filename = "output.csv"  

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for i in range(len(dic_list)):
            writer.writerow(dic_list[i])


def read_variants(GeneName):
  filename = f"{GeneName}.csv"
  lst = []
  with open(filename, 'r') as csvfile:
    print('csv opened')
    reader = csv.reader(csvfile)
    count = 0
    total = 1937
    for row in reader:
      result = variant_request(row[0])
      print(str(count/total * 100) + "%")
      count+=1
      if result is not None:
        for r in result:
          lst.append(r)
      if count == 50:
        break
    print("got all info")
  
  return lst

def write_dict_to_csv(data, filename):
    # Extract column names and values
    columns = list(data.keys())
    values = list(data.values())
    num_rows = len(values[0])

    # Write data to CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(columns)
        # Write rows
        for i in range(num_rows):
            row = [values[j][i] for j in range(len(values))]
            writer.writerow(row)

def read_VCF(fileName):

  callset = allel.read_vcf(fileName)
  return callset

write_dict_to_csv(read_VCF("clinvar_20240307.vcf"), "clinvardataset")
print("done")