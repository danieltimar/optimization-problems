

# linear_relaxation

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


max_optimistic_value = 0


def build_optimization_tree(item_values, item_weights, k, x=0, taken=[], value=0):

    if len(item_values) == 0:
        return taken

    else:
        if x == 1:
            value_increment, weight_increment = item_values[0], item_weights[0]
            taken.append(1)

        elif x == 0:
            value_increment, weight_increment = 0, 0
            taken.append(0)

        value += value_increment
        capacity = k - weight_increment
        del item_values[0]
        del item_weights[0]

        optimistic_value_at_point = value + calc_max_value_with_lr(item_values, item_weights, k=capacity)

        global max_optimistic_value

        if max_optimistic_value > optimistic_value_at_point:
            pass

        else:
            max_optimistic_value = optimistic_value_at_point
            build_optimization_tree(item_values=item_values, item_weights=item_weights, k=capacity, taken=taken, x=1)
            build_optimization_tree(item_values=item_values, item_weights=item_weights, k=capacity, taken=taken, x=0)



if __name__ == "__main__":
    max_optimistic_value = 0
    item_values = [45, 48, 35]
    item_weights = [5, 8, 3]

    taken = build_optimization_tree(item_values=item_values, item_weights=item_weights, k=10, x=0)
    print(taken)







