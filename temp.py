max = -1.0
min = 1.0

out_min = 0
out_max = 2048

deltaIn = max - min
deltaOut = out_max - out_min

In = 0

pre = (In-min)/deltaIn

result = pre * deltaOut + out_min

print("Delta in: " + str(deltaIn))
print("Delta out: " + str(deltaOut))
print("Precent: " + str(pre))
print("Out: " + str(result))
