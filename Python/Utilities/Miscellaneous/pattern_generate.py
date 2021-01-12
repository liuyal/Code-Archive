n = 50*2

counter = 0
im_index = 0
flag = True

for i in range(0, n):

    if counter > 3:
        counter = 0
        flag = not flag

    if flag:
        if i % 2 > 0:
            print(i, counter, flag, 1, im_index)
            im_index += 1
        else:
            print(i, counter, flag, 0, im_index)
    else:
        if i % 2 > 0:
            print(i, counter, flag, 0, im_index)
            im_index += 1
        else:
            print(i, counter, flag, 1, im_index)


    counter += 1
