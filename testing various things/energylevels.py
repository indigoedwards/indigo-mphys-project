import matplotlib.pyplot as plt
import numpy as np

filelist = ["01","23","45","67","89"]

data = []
for i in filelist:
    with open(f"C:\Users\Indigo Edwards\indigo-mphys-project\testing various things\energylevel-output{i}.txt","r") as file:
        arr = [line.strip().split() for line in file.readlines()]
        data.append(arr)

print(data)