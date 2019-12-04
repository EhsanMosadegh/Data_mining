#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

max_depth = np.arange(1, 152)

mu = 10
sigma = 1
gaussian_size = [5000, 2]

lower_bound = 0
upper_bound = 20
noise_size = [200, 2]

gaussian_points = np.random.normal(mu, sigma, gaussian_size)
x_axis_p = gaussian_points[:,0]
y_axis_p = gaussian_points[:,1]


gaussian_noise_points = np.random.uniform(lower_bound, upper_bound, noise_size)
x_axis_p = np.append(x_axis_p, gaussian_noise_points[:,0])
y_axis_p = np.append(y_axis_p, gaussian_noise_points[:,1])
label_gauss = np.array([])
for i in range(0, 5200):
  label_gauss = np.append(label_gauss, "+")

uniform_size = [5200, 2]
uniform_points = np.random.uniform(lower_bound, upper_bound, uniform_size)
x_axis_n = uniform_points[:,0]
y_axis_n = uniform_points[:,1]

label_unif = np.array([])
for i in range(0, 5200):
  label_unif = np.append(label_unif, "o")

plt.scatter(x_axis_n, y_axis_n, s=2, facecolors='none', edgecolors='r')
plt.scatter(x_axis_p, y_axis_p, s=10, marker="+")

plt.show()

x_axis = x_axis_p
x_axis = np.append(x_axis, x_axis_n)

y_axis = y_axis_p
y_axis = np.append(y_axis, y_axis_n)

labels = label_gauss
labels = np.append(labels, label_unif)

data = {'x_col': x_axis, 'y_col': y_axis, 'class_label': labels}
dataframe = DataFrame(data)

Y = dataframe['class_label']
X = dataframe.drop(['class_label'], axis=1)

dataframe = dataframe.sample(frac=1).reset_index(drop=True)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.9)

train_acc = np.zeros(len(max_depth))
test_acc = np.zeros(len(max_depth))

for depth in max_depth:
  clf = tree.DecisionTreeClassifier(max_depth=depth)
  clf = clf.fit(X_train, Y_train)
  pred_train = clf.predict(X_train)
  pred_test = clf.predict(X_test)
  train_acc[depth-1] = accuracy_score(Y_train, pred_train)
  test_acc[depth-1] = accuracy_score(Y_test, pred_test)

plt.plot(max_depth, 1-train_acc, max_depth, 1-test_acc)
plt.legend(['Training Accuracy', 'Test Accuracy'])
plt.xlabel("Max Depth")
plt.ylabel('Accuracy')


plt.show()