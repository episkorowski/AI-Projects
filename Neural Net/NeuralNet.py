import copy
import sys
from datetime import datetime
from math import exp
from random import random, randint, choice


class Perceptron:
    """
    Class to represent a single Perceptron in the net.
    """

    def __init__(self, in_size=1, weights=None):
        self.inSize = in_size + 1  # number of perceptrons feeding into this one; add one for bias
        if weights is None:
            # weights of previous layers into this one, random if passed in as None
            self.weights = [1.0] * self.inSize
            self.set_random_weights()
        else:
            self.weights = weights

    def get_weighted_sum(self, in_acts):
        """
        Returns the sum of the input weighted by the weights.
        
        Inputs:
            in_acts (list<float/int>): input values, same as length as inSize
        Returns:
            float
            The weighted sum
        """
        return sum([inAct * inWt for inAct, inWt in zip(in_acts, self.weights)])

    def sigmoid(self, value):
        """
        Return the value of a sigmoid function.
        
        Args:
            value (float): the value to get sigmoid for
        Returns:
            float
            The output of the sigmoid function parametrized by 
            the value.
        """
        """YOUR CODE"""
        return 1 / (1 + exp(-value))

    def sigmoid_activation(self, in_acts):
        """
        Returns the activation value of this Perceptron with the given input.
        Same as g(z) in book.
        Remember to add 1 to the start of inActs for the bias input.
        
        Inputs:
            in_acts (list<float/int>): input values, not including bias
        Returns:
            float
            The value of the sigmoid of the weighted input
        """
        """YOUR CODE"""
        new_in_acts = in_acts[:]
        new_in_acts.insert(0,1)
        # print(new_in_acts)
        return self.sigmoid(self.get_weighted_sum(new_in_acts))


    def sigmoid_deriv(self, value):
        """
        Return the value of the derivative of a sigmoid function.
        
        Args:
            value (float): the value to get sigmoid for
        Returns:
            float
            The output of the derivative of a sigmoid function
            parametrized by the value.
        """
        value = self.sigmoid(value)
        return value * (1 - value)

    def sigmoid_activation_deriv(self, in_acts):
        """
        Returns the derivative of the activation of this Perceptron with the
        given input. Same as g'(z) in book (note that this is not rounded.
        Remember to add 1 to the start of inActs for the bias input.
        
        Inputs:
            in_acts (list<float/int>): input values, not including bias
        Returns:
            int
            The derivative of the sigmoid of the weighted input
        """
        new_in_acts = in_acts[:]
        new_in_acts.insert(0,1)
        return self.sigmoid_deriv(self.get_weighted_sum(new_in_acts))

    def update_weights(self, in_acts, alpha, delta):
        """
        Updates the weights for this Perceptron given the input delta.
        Remember to add 1 to the start of inActs for the bias input.
        
        Inputs:
            in_acts (list<float/int>): input values, not including bias
            alpha (float): The learning rate
            delta (float): If this is an output, then g'(z)*error
                           If this is a hidden unit, then the as defined-
                           g'(z)*sum over weight*delta for the next layer
        Returns:
            float
            Return the total modification of all the weights (sum of each abs(modification))
        """
        total_modification = 0
        new_in_acts = [1] + in_acts

        for i in range(len(new_in_acts)):
            new_weight = self.weights[i] + alpha * new_in_acts[i] * delta
            total_modification += abs(new_weight - self.weights[i])
            self.weights[i] = new_weight
        return total_modification

    def set_random_weights(self):
        """
        Generates random input weights that vary from -1.0 to 1.0
        """
        for i in range(self.inSize):
            self.weights[i] = (random() + .0001) * (choice([-1, 1]))

    def __str__(self):
        outStr = ''
        outStr += 'Perceptron with %d inputs\n' % self.inSize
        outStr += 'Node input weights %s\n' % str(self.weights)
        return outStr


class NeuralNet:
    """
    Class to hold the net of perceptrons and implement functions for it.
    """

    def __init__(self, layer_size):  # default 3 layer, 1 percep per layer
        """
        Initiates the NN with the given sizes.
        
        Args:
            layer_size (list<int>): the number of perceptrons in each layer
        """
        self.layer_size = layer_size  # Holds number of inputs and percepetrons in each layer
        self.output_layer = []
        self.num_hidden_layers = len(layer_size) - 2
        self.hidden_layers = [[] for x in range(self.num_hidden_layers)]
        self.num_layers = self.num_hidden_layers + 1

        # build hidden layer(s)
        for h in range(self.num_hidden_layers):
            for p in range(layer_size[h + 1]):
                percep = Perceptron(layer_size[h])  # num of perceps feeding into this one
                self.hidden_layers[h].append(percep)

        # build output layer
        for i in range(layer_size[-1]):
            percep = Perceptron(layer_size[-2])  # num of perceps feeding into this one
            self.output_layer.append(percep)

        # build layers list that holds all layers in order - use this structure
        # to implement back propagation
        self.layers = [self.hidden_layers[h] for h in range(self.num_hidden_layers)] + [self.output_layer]

    def __str__(self):
        out_str = ''
        out_str += '\n'
        for hidden_index in range(self.num_hidden_layers):
            out_str += '\nHidden Layer #%d' % hidden_index
            for index in range(len(self.hidden_layers[hidden_index])):
                out_str += 'Percep #%d: %s' % (index, str(self.hidden_layers[hidden_index][index]))
            out_str += '\n'
        for i in range(len(self.output_layer)):
            out_str += 'Output Percep #%d:%s' % (i, str(self.output_layer[i]))
        return out_str

    def feed_forward(self, in_acts):
        """
        Propagate input vector forward to calculate outputs.
        
        Args:
            in_acts (list<float>): the input to the NN (an example)
        Returns:
            list<list<float/int>>
            A list of lists. The first list is the input list, and the others are
            lists of the output values of all perceptrons in each layer.
        """
        result = [in_acts]

        for i in range(self.num_layers):
            prev_layer = result[i]
            curr_layer = []
            for percep in self.layers[i]:
                activation = percep.sigmoid_activation(prev_layer) #-1?
                curr_layer.append(activation)
            result.append(curr_layer)
        return result


    def backprop_learning(self, examples, alpha):
        """
        Run a single iteration of backward propagation learning algorithm.
        See the text and slides for pseudo code.
        
        Args: 
            examples (list<tuple<list<float>,list<float>>>):
              for each tuple first element is input(feature)"vector" (list)
              second element is output "vector" (list)
            alpha (float): the alpha to training with
        Returns
           tuple<float,float>
           
           A tuple of average_error and average_weight_change, to be used as stopping conditions.
           average_error is the summed error^2/2 of all examples, divided by numExamples*numOutputs.
           average_weight_change is the summed absolute weight change of all perceptrons,
           divided by the sum of their input sizes (the average weight change for a single perceptron).
        """
        # keep track of output
        average_error = 0
        average_weight_change = 0
        num_weights = 0

        for example in examples:  # for each example
            # keep track of deltas to use in weight change
            deltas = []
            # Neural net output list
            all_layer_output = self.feed_forward(example[0])
            last_layer_output = all_layer_output[-1]
            # Empty output layer delta list
            out_delta = []
            # iterate through all output layer neurons
            for output_num in range(len(example[1])):
                g_prime = self.output_layer[output_num].sigmoid_activation_deriv(all_layer_output[-2]) # example[0]?
                error = (example[1][output_num] - last_layer_output[output_num])   #"""FILL IN - error for this neuron"""
                delta = error * g_prime   #"""FILL IN - delta for this neuron"""
                average_error += error * error / 2
                out_delta.append(delta)
            deltas.append(out_delta)

            """
            Backpropagate through all hidden layers, calculating and storing
            the deltas for each perceptron layer.
            """
            for layer_num in range(self.num_hidden_layers - 1, -1, -1):
                layer = self.layers[layer_num]
                next_layer = self.layers[layer_num + 1]
                hidden_delta = []
                # Iterate through all neurons in this layer
                for neuronNum in range(len(layer)):
                    g_prime = layer[neuronNum].sigmoid_activation_deriv(all_layer_output[layer_num]) # FILL IN

                    w = sum([next_layer[i].weights[neuronNum+1] * deltas[0][i] for i in range(len(next_layer))])


                    delta = g_prime * w                   
                            #"""FILL IN - delta for this neuron
                               #Carefully look at the equation here,
                               # it is easy to do this by intuition incorrectly"""
                    hidden_delta.append(delta)
                deltas = [hidden_delta] + deltas
            """Get output of all layers"""

            """
            Having aggregated all deltas, update the weights of the 
            hidden and output layers accordingly.
            """
            for num_layer in range(0, self.num_layers):
                layer = self.layers[num_layer]
                for numNeuron in range(len(layer)):
                    weight_mod = layer[numNeuron].update_weights(all_layer_output[num_layer], alpha, deltas[num_layer][numNeuron])
                    average_weight_change += weight_mod
                    num_weights += layer[numNeuron].inSize
                    # end for each example
        # calculate final output
        average_error /= (len(examples) * len(examples[0][1]))  # number of examples x length of output vector
        average_weight_change /= (num_weights)
        return average_error, average_weight_change


def build_neural_net(examples, alpha=0.1, weight_change_threshold=0.00008, hidden_layer_list=[1], max_iter=sys.maxsize,
                     start_nn=None):
    """
    Train a neural net for the given input.
    
    Args: 
        examples (tuple<list<tuple<list,list>>,
                        list<tuple<list,list>>>): A tuple of training and test examples
        alpha (float): the alpha to train with
        weight_change_threshold (float):           The threshold to stop training at
        max_iter (int):                            Maximum number of iterations to run
        hidden_layer_list (list<int>):             The list of numbers of Perceptrons
                                                 for the hidden layer(s). 
        start_nn (NeuralNet):                   A NeuralNet to train, or none if a new NeuralNet
                                                 can be trained from random weights.
    Returns
       tuple<NeuralNet,float>
       
       A tuple of the trained Neural Network and the accuracy that it achieved 
       once the weight modification reached the threshold, or the iteration 
       exceeds the maximum iteration.
    """
    examples_train, examples_test = examples
    num_in = len(examples_train[0][0])
    num_out = len(examples_test[0][1])
    time = datetime.now().time()
    if start_nn is not None:
        hidden_layer_list = [len(layer) for layer in start_nn.hidden_layers]
    print(
        "Starting training at time %s with %d inputs, %d outputs, %s hidden layers, size of training set %d, and size of test set %d" \
        % (str(time), num_in, num_out, str(hidden_layer_list), len(examples_train), len(examples_test)))
    layer_list = [num_in] + hidden_layer_list + [num_out]
    nnet = NeuralNet(layer_list)
    if start_nn is not None:
        nnet = start_nn

    iteration = 0
    train_error = 0
    weight_mod = 1

    while(weight_mod > weight_change_threshold and iteration < max_iter):
        average_error, average_weight_change = nnet.backprop_learning(examples_train, alpha)
        train_error = average_error
        weight_mod = average_weight_change
        """
        Iterate for as long as it takes to reach weight modification threshold
        """
        if iteration%10==0:
            print("! on iteration %d; training error %f and weight change %f" % (iteration,train_error,weight_mod))
        else :
            print('.')

        iteration += 1


    time = datetime.now().time()
    print('Finished after %d iterations at time %s with training error %f and weight change %f' % (
    iteration, str(time), train_error, weight_mod))

    """
    Get the accuracy of your Neural Network on the test examples.
	For each text example, you should first feedforward to get the NN outputs. Then, round the list of outputs from the output layer of the neural net.
	If the entire rounded list from the NN matches with the known list from the test example, then add to test_correct, else add to  test_error.
    """

    test_error = 0
    test_correct = 0
    test_accuracy = 0  # num correct/num total

    for example in examples_test:
        ff_output = nnet.feed_forward(example[0])
        last_layer = ff_output[-1]
        rounded = [round(last_layer[i]) for i in range(len(last_layer))]
        # print(rounded)
        if example[1] == rounded:
            test_correct += 1
        else:
            test_error += 1

    test_accuracy = test_correct/(test_correct + test_error)

    print('Feed Forward Test correctly classified %d, incorrectly classified %d, test percent error  %f\n' % (
    test_correct, test_error, test_accuracy))

    """return something"""

    return nnet