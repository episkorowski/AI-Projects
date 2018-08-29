# utility functions for neural net project

import random


def get_nn_pen_data(filename="datasets/pendigits.txt", limit=100000):
    """
    returns limit # of examples from penDigits file
    """
    examples = []
    data = open(filename)
    line_num = 0
    for line in data:
        in_vector = [0] * 16
        out_vector = [0] * 10  # which digit is output
        count = 0
        for val in line.split(','):
            if count == 16:
                out_vector[int(val)] = 1
            else:
                in_vector[count] = int(val) / 100.0  # need to normalize values for inputs
            count += 1
        examples.append((in_vector, out_vector))
        line_num += 1
        if line_num >= limit:
            break
    return examples


def get_list(num, length):
    the_list = [0] * length
    the_list[num - 1] = 1
    return the_list


def build_examples_from_pen_data(size=10000):
    """
    build Neural-network friendly data struct
            
    pen data format
    16 input(attribute) values from 0 to 100
    10 possible output values, corresponding to a digit from 0 to 9

    """
    if size != 10000:
        pen_data_train_list = get_nn_pen_data("datasets/pendigitsTrain.txt", int(.8 * size))
        pen_data_test_list = get_nn_pen_data("datasets/pendigitsTest.txt", int(.2 * size))
    else:
        pen_data_train_list = get_nn_pen_data("datasets/pendigitsTrain.txt")
        pen_data_test_list = get_nn_pen_data("datasets/pendigitsTest.txt")
    return pen_data_train_list, pen_data_test_list


def build_potential_hidden_layers(num_inputs, num_outputs):
    """
    This builds a list of lists of hidden layer layouts
    num_inputs - number of inputs for data
    some -suggestions- for hidden layers - no more than 2/3 # of input nodes per layer, and
    no more than 2x number of input nodes total (so up to 3 layers of 2/3 # ins max
    """
    res_list = []
    tmp_list = []
    max_num_nodes = max(num_outputs + 1, 2 * num_inputs)
    if max_num_nodes > 15:
        max_num_nodes = 15

    for lyr1cnt in range(num_outputs, max_num_nodes):
        for lyr2cnt in range(num_outputs - 1, lyr1cnt + 1):
            for lyr3cnt in range(num_outputs - 1, lyr2cnt + 1):
                if lyr2cnt == num_outputs - 1:
                    lyr2cnt = 0

                if lyr3cnt == num_outputs - 1:
                    lyr3cnt = 0
                tmp_list.append(lyr1cnt)
                tmp_list.append(lyr2cnt)
                tmp_list.append(lyr3cnt)
                res_list.append(tmp_list)
                tmp_list = []
    return res_list


def test_pen_data(hidden_layers=[24]):
    pen_data = build_examples_from_pen_data()
    from NeuralNet import build_neural_net
    return build_neural_net(pen_data, max_iter=200, hidden_layer_list=hidden_layers)


def average(mylist):
    return sum(mylist)/len(mylist)


def std_dev(mylist):
    import math
    mean = average(mylist)
    sum_diff_sq = 0
    for x in mylist:
        sum_diff_sq += (x-mean)**2
    return math.sqrt(sum_diff_sq/len(mylist))

def restarts(hidden_layers=[10]):
    max_calls = 5
    results = []

    for i in range(max_calls):
        accuracy = test_pen_data(hidden_layers)
        results.append(accuracy)

    print("Size: ", hidden_layers[0])
    print("Max: ", max(results))
    print("Average: ", average(results))
    print("Standard Deviation: ", std_dev(results))

def main():

    #test_pen_data()
    #restarts()
    
    layers = 0
    while layers <= 40:
        restarts([layers])
        layers += 5
    
    

main()
