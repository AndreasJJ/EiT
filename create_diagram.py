import argparse
import matplotlib.pyplot as plot
import os

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
    help="name of person to make plot of. If all, everyones blinking is plotted into same graph.")
args = vars(ap.parse_args())

test_cases = ["blinking", "damped_ear", "thresh", "is_blinking"]
colors = ["green", "red", "purple", "blue", "purple"]

def summary_of_everyone():
  all_names = [x[0] for x in os.walk("tests/")][1:]
  print(all_names)
  # lines = f.readlines()
  plot.figure(figsize=(40,10))
  for i in range(len(all_names)):
    name = all_names[i]
    f = open("{}/blinking.txt".format(name), "r")
    line = f.readline()
    color = "black"
    if i < len(colors):
      color = colors[i]    
    list_from_line = line.split(";")
    # name_from_list = list_from_line[0]
    number_list = [float(number) for number in list_from_line[1:-1]]
    if len(number_list) > 1000:
      number_list = number_list[:1000]
    plot.plot(number_list, color=color, label=name)
  plot.savefig("tests/blinking_all.png")
    
def only_one():
  plot.figure(figsize=(40,10))
  name_from_args = args["name"]
  for i in range(len(test_cases)):
    f = open("tests/{}/{}.txt".format(name_from_args, test_cases[i]), "r")
    line = f.readline()
    color = "black"
    if i < len(colors):
      color = colors[i]
    list_from_line = line.split(";")
    name_from_list = list_from_line[0]
    if name_from_list == name_from_args:
      number_list = [float(number) for number in list_from_line[1:-1]]
      if len(number_list) > 1000:
        number_list = number_list[:1000]
      plot.plot(number_list, color=color)
      plot.savefig("tests/{0}/{1}.png".format(name_from_list, test_cases[i]))
    f.close()
  plot.savefig("tests/{0}/summary.png".format(name_from_list))

if __name__ == "__main__":
  if args["name"] == "all": 
    summary_of_everyone()
  else:
    only_one()


    