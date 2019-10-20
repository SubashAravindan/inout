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
learningRate = 0.0001
optimizer = tf.compat.v1.train.AdamOptimizer(learningRate)
totalEpochs = 501
stepSize = 10
saveSize = 100

trainingClasses = os.listdir("./Training_Data")
outputClasses = len(trainingClasses)
batchSize = 50

# Helper function to resize the images
def resizeImg(img):
    return cv2.resize(img, (width, height))

# Loading all the images from the dateset
print("Loading Training Data")
X_train = []
Y_train = []
pwd = os.getcwd()
for num, direc in enumerate(trainingClasses):
    classPath = pwd + "/Training_Data/" + direc
    os.chdir(classPath)
    image_names = os.listdir(classPath)
    for image_name in image_names:
        img = cv2.imread(classPath + "/" + image_name)
        img_new = resizeImg(img)
        X_train.append(img_new)
        Y_train.append(num + 1)
print("Loaded training data")
print("Total data points are ", len(X_train))

# Changing back to the present directory
os.chdir(pwd)

# Creating the place holders
X1 = tf.compat.v1.placeholder(name = "Input1", dtype = tf.float32, shape = [None, width, height, channels])
X2 = tf.compat.v1.placeholder(name = "Input2", dtype = tf.float32, shape = [None, width, height, channels])
Y  = tf.compat.v1.placeholder(name = "Output_Class", dtype = tf.float32, shape = [None])

# Creating the network
net = Network(X1, X2, Y, outputClasses)
tripletLoss = net.loss
diff = net.diff
train = optimizer.minimize(tripletLoss, var_list=[tf.compat.v1.global_variables()])
init = tf.compat.v1.global_variables_initializer()
sess = tf.compat.v1.Session()
saver = tf.compat.v1.train.Saver()
load = True
sess.run(init)

if load:
    saver.restore(sess, "./Weights/model")

# Helper function to get the images
def getImages(bchSize):
    images = []
    vals = []
    for i in range(bchSize):
        number = random.randint(0, len(X_train) - 1)
        images.append(X_train[number])
        vals.append(Y_train[number])
    return images, vals

for step in range(totalEpochs):
    batchX1, batchY1 = getImages(batchSize)
    batchX2, batchY2 = getImages(batchSize)
    batchY = np.equal(batchY1, batchY2)
    _, loss = sess.run([train, tripletLoss], feed_dict = {
        X1 : batchX1,
        X2 : batchX2,
        Y : batchY
    })

    if np.isnan(loss):
        print("Loss diverged and model diverged")

    if step % stepSize == 0:
        print("The loss after ", step, " is ", loss)

    if step % saveSize == 0:
        saver.save(sess, "./Weights/model")
        print("Saving the model weights")
