import matplotlib.pyplot as plt
import random


plt.suptitle("Variation of Performance Correlation \n with Quantity of Tough Questions",fontsize=16,style='italic')
plt.xlabel("Number of Tough Questions in a testing strategy",fontsize=10)
plt.ylabel("Performance Correlation of testing strategy",fontsize=10)
#~ plt.yticks([0.7,0.8,0.9,1])
plt.savefig("Variation_of_Performance_Correlation_with_Quantity_of_Tough_Questions.png")
plt.clf()
