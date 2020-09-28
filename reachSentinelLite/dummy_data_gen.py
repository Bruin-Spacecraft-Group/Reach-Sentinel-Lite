import time
import datetime
import random
import sys

timep1 = time.time() * 1000

while (True):
    cur_out_string = ""
    random.seed()
    cur_rand_num = random.randint(0, 10)
    temp_rand_num = random.randint(70, 90)
    timep3 = time.time() * 1000 # time in terms of minutes since epoch
    timep3 = timep3 - timep1 # time since beginning of data generation
    cur_out_string += str(timep3)
    cur_out_string += ","
    LEN = 17
    for i in range(0, LEN): # append random number for each of the 17 fields
        if i == 13: # append a more realistic number for temp_rand_num
            cur_out_string += str(temp_rand_num)
        else:
            cur_out_string += str(cur_rand_num)
        if i < LEN - 1:
            cur_out_string += ","
    cur_out_string += "\r\n"
    sys.stderr.write(cur_out_string)
    print(cur_out_string)
    time.sleep(3) # sleep for three seconds minus the amount of time it takes to run an interation