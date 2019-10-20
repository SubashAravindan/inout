import tensorflow.compat.v1 as tf
import tensorflow as tf2
import os

class Network:
    def __init__(self, X1, X2, Y, outputClasses):

        self.x1 = tf.reshape(X1, [tf.shape(X1)[0], tf.shape(X1)[1] * tf.shape(X1)[2] * tf.shape(X1)[3]]) 
        self.x2 = tf.reshape(X2, [tf.shape(X2)[0], tf.shape(X2)[1] * tf.shape(X2)[2] * tf.shape(X2)[3]])
        self.nextDim = X1.get_shape()[1] * X1.get_shape()[2] * X1.get_shape()[3]
        self.Y = Y
        self.hiddenSize = 500
        self.margin = 5.0
        self.outputClasses = outputClasses

        # Creating the twin networks
        with tf.variable_scope("simease") as scope:
            self.o1 = self.createNetwork(self.x1)
            scope.reuse_variables()
            self.o2 = self.createNetwork(self.x2)

        # Choosing the loss function
        self.loss = self.getLoss()

        # Getting the difference
        self.diff = self.getDistance()

    def createNetwork(self, X):
        W = tf.get_variable(name = "W0", shape = [self.nextDim, self.hiddenSize])
        B = tf.get_variable(name = "B0", shape = [self.hiddenSize])
        out = tf.matmul(X, W) + B 
       
        for i in range(1, 3):
            W = tf.get_variable(name = "W" + str(i), shape = [self.hiddenSize, self.hiddenSize])
            B = tf.get_variable(name = "B" + str(i), shape = [self.hiddenSize])
            out = tf.matmul(out, W) + B
        
        wOut = tf.get_variable("wOut", shape = [self.hiddenSize, self.outputClasses])
        bOut = tf.get_variable("bOut", shape = [self.outputClasses])
        out = tf.matmul(out, wOut) + bOut
        return out
    
    def getLoss(self):
        eucl = tf.pow(tf.subtract(self.o1, self.o2), 2)
        eucl = tf.reduce_sum(eucl, axis = 1)
        eucd = tf.sqrt(eucl + 1e-6)
        margin = tf.constant(self.margin, dtype = tf.float32)
        D1 = tf.multiply(eucl, self.Y)
        D2 = tf.multiply(1 - self.Y, tf.pow(tf.math.maximum(0.0, margin - eucd), 2)) 
        outputLoss = D1 + D2
        outputLoss = tf.reduce_mean(outputLoss)
        return outputLoss

    def getDistance(self):
        dist = tf.pow(self.o1 - self.o2, 2)
        dist = tf.reduce_mean(dist, axis = 1)
        dist = tf.sqrt(dist + 1e-6)
        return dist

