
"""
RUNNING TOTAL
-------------

* Make running_total a coroutine function that can receive values via
  `send(value)` and prints out the sum of all the numbers it has ever received.
  The print statements should look something like: f"Total so far: {total}"

* Update `total_calculator` so it is an instance of this coroutine, and will be
  able to receive new values via `send()`
"""

def running_total():
    pass  # TODO: Make this a coroutine function


# TODO: Make this a coroutine instance
total_calculator = None


# Don't change the code below here
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("Calculating Running Total")

for value in [8, 13, 6, 7, 3, 5]:
    print(f"Adding {value}")
    total_calculator.send(value)


"""
RUNNING AVERAGE
---------------

If you have more time take a look at this now, otherwise you could have a go
later.

* Make running_average a coroutine that receives values and prints out an
  average of all the numbers it has ever received (sum of all the values it
  has received divided by the number of values it has received).

* Switch the boolean condition from `if False` to `if True` so that the code
  runs, run the script, and check that the output looks reasonable.
"""


def running_average():
    pass  # TODO: Make this a coroutine function


# TODO: Switch this condition to `if True`
if False:
    print("Calculating Running Average")

    average_calculator = running_average()
    next(average_calculator)

    for value in [2, 4, 6, 12, 7, 13]:
        print(f"Adding {value}")
        average_calculator.send(value)
