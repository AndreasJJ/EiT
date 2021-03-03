import argparse
import matplotlib.pyplot as plot

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
    help="name of person to make plot of")
args = vars(ap.parse_args())


colors = ["green", "red", "purple", "blue", "purple"]

def main():
  f = open("blinking.txt", "r")
  lines = f.readlines()
  plot.figure(figsize=(40,10))
  for i in range(len(lines)):
    color = "black"
    if i < len(colors):
      color = colors[i]
    list_from_line = lines[i].split(";")
    name_from_list = list_from_line[0]
    name_from_args = args["name"]
    if name_from_list == name_from_args or name_from_args == "all":
      number_list = [float(number) for number in list_from_line[1:-1]]
      if len(number_list) > 1000:
        number_list = number_list[:1000]
      plot.plot(number_list, color=color, label=name_from_list)
      if name_from_list == name_from_args: 
        plot.savefig("{}_blinking.png".format(name_from_list))
        break
  if name_from_list == "all": plot.savefig("blinking.png")
    

if __name__ == "__main__":
  main()