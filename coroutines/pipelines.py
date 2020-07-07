import os
import time
import logging


# The directory containing this file
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Set default logging config with level set to INFO
logging.basicConfig(level=logging.INFO)


"""
CHAINING COROUTINES
~~~~~~~~~~~~~~~~~~~

In this section, you'll chain two coroutines together, to define a new
coroutine which will receive strings, filter the ones which contain the
substring 'whale', and then write these strings to a file.

* Update `file_writer` so that it is a coroutine function which receives strings
  through `send()` and then writes them to the file at `filename`. You can
  leave the start of the function as it is, and just replace the `pass`
  statement.

* Update `grep` so that is a coroutine function which receives strings through
  `send()`, and sends them on to another coroutine (`target`) if they contain
  the substring `pattern`.

* Update `whale_filter` so it is a chained coroutine which uses `grep` and
  `file_writer` to filter lines which contain the string 'whale', and write
  them to the file `whale_lines_path` (this is already defined). You'll need
  to add some more lines of code to achieve this.

"""

def file_writer(filename):
    "A coroutine 'sink' function which receives values and writes them to file"
    print(f"\nFile writer initialised. Writing to {filename}...")
    # Using buffering=1 ensures that lines are written immediately.
    with open(filename, 'w', buffering=1) as file:
        # TODO: Update this function so that it returns a coroutine which
        # writes each value it receives to file (using file.write(...))
        pass


def grep(pattern, target):
    """A coroutine 'filter' function which matches strings containing `pattern`

    Sent values which contain the substring `pattern`, are sent on to the
    `target` coroutine.
    """
    # TODO Update this function so it returns a coroutine, which filters lines
    # that contain `pattern` as a substring, and sends matching lines on to the
    # specified `target` coroutine.
    pass


whale_lines_path = os.path.join(THIS_DIR, 'whale_lines.txt')

# TODO: Use `grep` and `file_writer` to define whale_filter.
whale_filter = NotImplemented


# DON'T CHANGE THE CODE BELOW THIS LINE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("Writing to", whale_lines_path)
with open(__file__) as this_file:
    for line in this_file:
        whale_filter.send(line)
print("Writing complete\n")


"""
DATA SOURCES
~~~~~~~~~~~~

The watch function below polls a file for new lines, and when a new line
is added, prints it to stdout.

* Update the condition from `False` to `True` at the bottom of this section.
  Run the script, you should see `Line 1`, `Line 2`, `Line 3` etc. printed out.
  If you add a new line to the bottom of the file `source.txt`, then that will
  print out as soon as you save the file.

  (You'll have to use `Ctrl + C` to stop the program running)

* Update `watch` so that it expects a second argument called `target`, which
  is a coroutine. Instead of printing each line to stdout, `watch` should
  `send` the line to the `target` coroutine.

* Create a new `file_writer` coroutine instance which will write to
  `destination_file`, and use this as the `target` in the call to
  `watch`

"""


def watch(filename):
    """A data source that watches for additions to a file"""
    print(f"Watching for file changes in: {filename}")
    with open(filename) as file:
        try:
            while True:
                next_line = file.readline()
                if next_line:
                    print(next_line)
                # Wait a little before fetching the next line or polling again
                time.sleep(0.2)
        except KeyboardInterrupt:
            print(f"\nNo longer watching changes in {filename}")


source_file = os.path.join(THIS_DIR, 'source.txt')
destination_file = os.path.join(THIS_DIR, 'destination.txt')


if False:
    # TODO: Update this call so that it uses a new `file_writer` as a target
    watch(source_file)


"""
PIPELINES
~~~~~~~~~

* Update `broadcast` so that it is a coroutine function which receives
  values through `send` and then forwards these on to each of the coroutines in
  the list of `targets`.

* Combine the functions `watch`, `broadcast`, `grep`, `file_writer` and
  `stdout_logger` to build a single pipeline which:

  - watches the file `log_path` for updates.
  - logs any file changes to stdout (using the stdout_logger)
  - copies any log lines that contain the strings 'anna' or 'amit' to the file
    `filtered_log_path`.

  You won't need to change the function `stdout_logger`. This is a coroutine
  function which logs any data it receives through `send()`. An instance is
  already created for you to use in the pipeline.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                              #
#                              +--> grep('anna') --+                           #
#       watch  --> broadcast --|                   |--> file_writer            #
#    (log_file)                |--> grep('amit') --+    (filtered_log_file)    #
#                              |                                               #
#                              +----------------------> stdout_logger          #
#                                                                              #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


def broadcast(targets):
    "A coroutine to broadcast one 'input' to several targets"
    print(f"\nBroadcasting to {len(targets)} targets\n")
    # TODO: Whenever a value is sent to `broadcast` the same value should
    # be sent to each of the coroutines in the `targets` array.
    pass


def stdout_logger(message_prefix):
    """A coroutine function that takes values, and logs them to stdout"""
    logger = logging.getLogger(__name__)
    print('Initializing logger.')
    while True:
        next_value = yield
        logger.info(f'{message_prefix}: {next_value.strip()}')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


log_path = os.path.join(THIS_DIR, 'logs.txt')
filtered_log_path = os.path.join(THIS_DIR, 'filtered.txt')

# Create a logger instance
logger = stdout_logger('New log message received.')

# TODO: Finish defining the pipeline as described above, and start it running
