# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 16:16:00 2017

@author: root
"""

import nengo
import numpy, math
model = nengo.Network()

epsilon = 0.12
weights1 = numpy.random.uniform(-epsilon, epsilon, size = (2, 2))
weights2 = numpy.random.uniform(-epsilon, epsilon, size = (2, 2))
print weights1

def sigmoid(x):
    if x > -6:
        sig = 1/(1+math.exp(-x))
    else:
        sig = 0
    return sig

def sigmoid_grad(x):
    sig_grad = sigmoid(x)*(1-sigmoid(x))
    return sig_grad

with model:
    #input vector. Pixels to be identified
    inp =  [1, 0]
    Input = nengo.Node(inp)
    
    Input_Node_1 = nengo.Ensemble(100, dimensions = 1)
    Input_Node_2 = nengo.Ensemble(100, dimensions = 1)
    Hidden_Node_1 = nengo.Ensemble(100, dimensions = 1)
    Hidden_Node_2 = nengo.Ensemble(100, dimensions = 1)
    Output_Node_1 = nengo.Ensemble(100, dimensions = 1)
    Output_Node_2 = nengo.Ensemble(100, dimensions = 1)

    nengo.Connection(Input[0], Input_Node_1)
    nengo.Connection(Input[1], Input_Node_2)

    nengo.Connection(Input_Node_1, Hidden_Node_1, transform = weights1[0][0], function = sigmoid)
    nengo.Connection(Input_Node_2, Hidden_Node_1, transform = weights1[1][0], function = sigmoid)

    nengo.Connection(Input_Node_1, Hidden_Node_2, transform = weights1[0][1], function = sigmoid)
    nengo.Connection(Input_Node_2, Hidden_Node_2, transform = weights1[1][1], function = sigmoid)


    nengo.Connection(Hidden_Node_1, Output_Node_1, transform = weights2[0][0], function = sigmoid)
    nengo.Connection(Hidden_Node_2, Output_Node_1, transform = weights2[1][0], function = sigmoid)

    nengo.Connection(Hidden_Node_1, Output_Node_2, transform = weights2[0][1], function = sigmoid)
    nengo.Connection(Hidden_Node_2, Output_Node_2, transform = weights2[1][1], function = sigmoid)

    Ouptput_Probe_1 = nengo.Probe(Output_Node_1, synapse = 0.01)
    Ouptput_Probe_2 = nengo.Probe(Output_Node_2, synapse = 0.01)
    
with nengo.Simulator(model) as sim:
    sim.run(0.3)
Out_1 = sim.data[Output_Node_1]
Out_2 = sim.data[Output_Node_2]