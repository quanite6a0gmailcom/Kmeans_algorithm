import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy


img = plt.imread("kevin.jpg")


width = img.shape[0]
height = img.shape[1]

img = img.reshape(width*height, 3)
print(img.shape)

kmeans = KMeans(n_clusters=100).fit(img)

labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_

print(clusters)

# img2 = numpy.zeros_like(img)
img2 = numpy.zeros((width, height, 3),dtype=numpy.uint8)

index = 0
for i in range(width):
    for j in range(height):
        label_of_pixel = labels[index]
        img2[i][j] = clusters[label_of_pixel]
        index += 1
# for i in range(len(img2)):
#     img2[i] = clusters[labels[i]]

# img2 = img2.reshape(width, height, 3)
plt.imshow(img2)
plt.show()
