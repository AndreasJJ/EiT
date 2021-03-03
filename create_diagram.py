import matplotlib.pyplot as plot

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
    number_list = [float(number) for number in list_from_line[1:-1]]
    if len(number_list) > 1000:
      number_list = number_list[:1000]
    plot.plot(number_list, color=color, label=list_from_line[0])
  plot.savefig("blinking.png")

if __name__ == "__main__":
  main()