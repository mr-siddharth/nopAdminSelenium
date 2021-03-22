import traceback

try:
    c = 5/0
except:
    print(traceback.format_exc())

