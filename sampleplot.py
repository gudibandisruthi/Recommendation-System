import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
N = 2
errors = [3.98897594593,4.06536653397]#obtained from cross validation
xloc = np.arange(N)                
ax.bar(xloc, errors, 0.35,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))
ax.set_xlim(-0.35,len(xloc)+0.35)
ax.set_ylim(0,5)
ax.set_ylabel('Root mean square error using cross validation')
ax.set_title('Algorithms')
xLabels = ["collaborative filtering","sentimental analysis"]
ax.set_xticks(xloc+0.2)
xtickLabels = ax.set_xticklabels(xLabels)
plt.setp(xtickLabels, rotation=0, fontsize=10)
plt.show()
