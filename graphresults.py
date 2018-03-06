#!/usr/bin/python

import subprocess
import sys
import re
import matplotlib.pyplot as plt

# Prints usage for script
def usage(program):
	print 'Usage: {} league'.format(program)

    
### Run main execution ###

if __name__ == "__main__":

	# Exit if usage incorrect
	if len(sys.argv) != 2:
		usage(sys.argv[0])
		sys.exit(1)

	# Capture script output
	output = subprocess.check_output(["./analyze.py", sys.argv[1]])
	output = re.split("[:\n]+", output)

	# Compile values into lists
	keys = []
	values = []
	for i in range(0,10,2):
		keys.append(output[i])
		values.append(float(output[i+1]))

	# Calculate avg
	mean = sum(values)/len(values)
	avg = []
	for i in range(0,5):
		avg.append(mean)

	# Plot values and average
	fig,ax = plt.subplots()
	ax.scatter(keys,values, label='Accuracy', marker='o', color='b')
	ax.plot(keys, avg, label='Average', linestyle='--', color='r')
	ax.set_title(sys.argv[1] + " Accuracy Statistics")
	ax.set_xlabel("Accuracies")
	ax.set_ylabel("Models")
	
	# Save the figure and close
	fig.savefig(sys.argv[1] + '_accuracies.png')
	plt.close()

