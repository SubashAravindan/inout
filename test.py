from network import Network
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
import numpy as np
import os
import random
import cv2

# Input image sizes
width = 300
height = 300
channels = 3

# Finding the number of training classes
trainingClasses = os.listdir("./Training_Data")
outputClasses = len(trainingClasses)

# Creating the place holders
X1 = tf.compat.v1.placeholder(name = "Input1", dtype = tf.float32, shape = [None, width, height, channels])
X2 = tf.compat.v1.placeholder(name = "Input2", dtype = tf.float32, shape = [None, width, height, channels])
Y  = tf.compat.v1.placeholder(name = "Output_Class", dtype = tf.float32, shape = [None])

# Creating the network
net = Network(X1, X2, Y, outputClasses)
tripletLoss = net.loss
diff = net.diff
sess = tf.compat.v1.Session()
saver = tf.compat.v1.train.Saver()

# Restoring the model
print("Restoring the weights")
saver.restore(sess, "./Weights/model")

# Testing with sample images
pwd = os.getcwd()
img1 = np.array(cv2.imread(pwd + "/Training_Data/Watch/watch1.jpeg"))
img2 = np.array(cv2.imread(pwd + "/Training_Data/Watch/watch2.jpg"))
img3 = np.array(cv2.imread(pwd + "/Training_Data/Cars/car1.jpg"))
print(img1.shape, img2.shape, img3.shape)

img1_new = cv2.resize(img1, (width, height))
img2_new = cv2.resize(img2, (width, height))
img3_new = cv2.resize(img3, (width, height))
print(img1_new.shape, img2_new.shape, img3_new.shape)

# Helper to find output
def findDiff(x1, x2):
    x1 = np.resize(np.array(x1), (1, width, height, 3))
    x2 = np.resize(np.array(x2), (1, width, height, 3))
    print(x1.shape, x2.shape)
    output_diff = sess.run([diff], feed_dict = {X1 : x1, X2 : x2})
    return output_diff

# Testing
out1 = findDiff(img1_new, img2_new)
out2 = findDiff(img1_new, img3_new)
print(out1, out2)
