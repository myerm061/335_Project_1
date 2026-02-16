import matplotlib.pyplot as plt

# Example data for n = 3000 (random mode)
algorithms = ['Bubble', 'Merge', 'Quick', 'Radix']
# times based on benchmark results measured on 2/13/2026. Not dynamic for cleanerpresentation 
times = [0.332445, 0.004688, 0.003184, 0.002922]



plt.figure(figsize=(8, 5))
plt.bar(algorithms, times)
plt.title("Sorting Algorithm Runtime (n = 3000, Random Input)")
plt.ylabel("Time (seconds)")
plt.xlabel("Algorithm")

plt.yscale("log")  # Makes differences clearer
plt.tight_layout()
plt.savefig("benchmark_plot.png")
plt.show()
