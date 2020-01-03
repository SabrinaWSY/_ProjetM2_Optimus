import numpy as np

cinema = np.array([1,3,1,1,12,15,0,10,5,3,3,3,5,7,4,1,4,2,6,2])
monument = np.array([246,115,143,253,108,195,143,111,127,55,44,34,23,55,29,68,23,31,24,16])
tournage = np.array([97,62,36,136,107,84,105,155,134,127,85,90,81,60,61,199,87,161,138,95])

corr_tournage_monument = np.corrcoef(tournage, monument)[0,1]
corr_tournage_cinema = np.corrcoef(tournage, cinema)[0,1]
corr_monument_cinema = np.corrcoef(monument, cinema)[0,1]

print(corr_tournage_monument)
print(corr_tournage_cinema)
print(corr_monument_cinema)