import time

def print_log(text):
    print("{} {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), text))