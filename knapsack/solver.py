#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import pandas
import numpy
Item = namedtuple("Item", ['index', 'value', 'weight'])


def calculate_value_of_taken(item_values, taken):
    return sum(v * taken[i] for (i, v) in enumerate(item_values))


def calc_max_value_with_lr(item_values, item_weights, k):

    item_values_local = list(item_values)
    item_weights_local = list(item_weights)
    value_per_weight = [v/w for (v, w) in zip(item_values_local, item_weights_local)]

    total_weight, total_value = 0, 0

    while True:

        if len(value_per_weight) == 0:
            break

        max_vpw_i = value_per_weight.index(max(value_per_weight))

        if total_weight + item_weights_local[max_vpw_i] <= k:

            total_weight += item_weights_local[max_vpw_i]
            total_value += item_values_local[max_vpw_i]

            del item_weights_local[max_vpw_i]
            del item_values_local[max_vpw_i]
            del value_per_weight[max_vpw_i]

        else:
            remainder = (k - total_weight)/item_weights_local[max_vpw_i]
            total_value += item_values_local[max_vpw_i] * remainder
            break

    return total_value


def build_optimization_tree(item_values, item_weights, k, x, taken=[], value=0):

    local_taken = list(taken)

    global max_value
    global optimal_list_of_taken

    if len(item_values) == 0:
        if max_value < value:
            max_value = value
            optimal_list_of_taken = local_taken
            return optimal_list_of_taken
        else:
            return optimal_list_of_taken

    else:
        if x == 1:
            value_increment, weight_increment = item_values[0], item_weights[0]
            local_taken.append(1)

        elif x == 0:
            value_increment, weight_increment = 0, 0
            local_taken.append(0)

        value += value_increment
        capacity = k - weight_increment

        if capacity < 0:
            return

        local_item_values = list(item_values)
        local_item_weights = list(item_weights)
        del local_item_values[0]
        del local_item_weights[0]

        optimistic_value_at_point = value + calc_max_value_with_lr(local_item_values, local_item_weights, k=capacity)

        if max_value > optimistic_value_at_point:
            return

        else:
            build_optimization_tree(item_values=local_item_values, item_weights=local_item_weights, k=capacity,
                                    taken=local_taken, value=value, x=1)
            build_optimization_tree(item_values=local_item_values, item_weights=local_item_weights, k=capacity,
                                    taken=local_taken, value=value, x=0)



def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    item_values = []
    item_weights = []

    for item in items:
        item_values.append(item.value)
        item_weights.append(item.weight)


    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full

    build_optimization_tree(item_values=item_values, item_weights=item_weights, k=capacity, x=1)
    build_optimization_tree(item_values=item_values, item_weights=item_weights, k=capacity, x=0)


    value = calculate_value_of_taken(item_values, optimal_list_of_taken)
    taken = optimal_list_of_taken
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

optimal_list_of_taken = []
max_value = 0

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()

        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

