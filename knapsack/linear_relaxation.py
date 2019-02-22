
# linear_relaxation

def calc_max_value_with_lr(item_values, item_weights, k):
	value_per_weight = [v/w for (v, w) in zip(item_values, item_weights)]

	total_weight = 0
	total_value = 0

	while True:

		if len(value_per_weight) == 0:
			break

		max_vpw_i = value_per_weight.index(max(value_per_weight))

		if total_weight + item_weights[max_vpw_i] <= k:

			total_weight += item_weights[max_vpw_i]
			total_value += item_values[max_vpw_i]

			del item_weights[max_vpw_i]
			del item_values[max_vpw_i]
			del value_per_weight[max_vpw_i]
		
		else:
			remainder = (k - total_weight)/item_weights[max_vpw_i]
			total_value += item_values[max_vpw_i] * remainder
			break

	return total_value

