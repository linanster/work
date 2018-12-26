#! /usr/bin/python
#

import time

# caculate latence from requesttime and responsetime
def get_latence_seconds(t1,t2):
    t1_arry = t1.split(".")
    t2_arry = t2.split(".")
    t1_fmt = t1_arry[0]
    t2_fmt = t2_arry[0]
    # convert to time struct
    t1_struct = time.strptime(t1_fmt,"%H:%M:%S")
    t2_struct = time.strptime(t2_fmt,"%H:%M:%S")
    # convert to time stamp
    t1_stamp = time.mktime(t1_struct)
    t2_stamp = time.mktime(t2_struct)
    # minus to obtain seconds
    latence = int(t1_stamp) - int(t1_stamp)
    return int(latence)
def get_latence_microseconds(t1,t2):
    t1_arry = t1.split(".")
    t2_arry = t2.split(".")
    t1_fmt = t1_arry[0]
    t1_microsec = t1_arry[1]
    t2_fmt = t2_arry[0]
    t2_microsec = t2_arry[1]
    # convert to time struct
    t1_struct = time.strptime(t1_fmt,"%H:%M:%S")
    t2_struct = time.strptime(t2_fmt,"%H:%M:%S")
    # convert to time stamp
    t1_stamp = time.mktime(t1_struct)
    t2_stamp = time.mktime(t2_struct)
    # minus to obtain micro seconds
    latence = (int(t2_stamp)*1000000+int(t2_microsec))-(int(t1_stamp)*1000000+int(t1_microsec))
    return int(latence)

if "__main__" == __name__:
    requesttime = "19:14:30.016847"
    responsetime = "19:14:30.017339"
    latence_seconds = get_latence_seconds(requesttime,responsetime) 
    latence_microseconds = get_latence_microseconds(requesttime,responsetime) 
    print "latence_seconds: %s" % latence_seconds
    print "latence_microseconds: %s" % latence_microseconds
