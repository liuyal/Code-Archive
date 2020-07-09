import os, sys, time
import numpy as np

# np.set_printoptions(edgeitems=30, linewidth=100000)

def bucket_sum_distribution(input_array, buckets, sort_arr=False):
    run_list = input_array.tolist()
    npt = int(len(input_array) / buckets)
    array = {}
    set_max = False

    for j in range(0, buckets): array[j] = []

    for i in range(0, npt):
        set_max = not set_max
        for j in range(0, buckets):
            if set_max:
                max_value = run_list.pop(run_list.index(max(run_list)))
                array[j].append(max_value)
            else:
                min_value = run_list.pop(run_list.index(min(run_list)))
                array[j].append(min_value)

    if len(run_list) > 0:
        set_max = not set_max
        for j in range(0, buckets):
            if set_max:
                max_value = run_list.pop(run_list.index(max(run_list)))
                array[j].append(max_value)
            else:
                min_value = run_list.pop(run_list.index(min(run_list)))
                array[j].append(min_value)
            if len(run_list) == 0: break

    if sort_arr:
        for j in range(0, buckets): array[j] = sorted(array[j])

    return array


if __name__ == "__main__":

    start = 1
    end = 1000
    step = 1
    buckets = 5

    array = np.arange(float(start), float(end + step), float(step))
    print("Input array: ")
    print(array)

    result = bucket_sum_distribution(array, buckets)
    print("\nOrganized into " + str(buckets) + " Buckets\n")

    for row in result:
        print("Bucket " + str(row) + ": ", end="")
        print(result[row])
        print("Sum: " + str(sum(result[row])))
        print("Length: " + str(len(result[row])) + "\n")

    time.sleep(10)