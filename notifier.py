import string
import sys
import time
import logging
import re
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, LoggingEventHandler


# This function go over given line and check if all char are legal
def isKosher(line):
    # set of all legal chars
    kosher_char = set((string.ascii_letters + string.digits))

    # remove all tabs whitespaces and newline
    line = re.sub(r"[\n\t\s]*", "", line)
    # print(line)

    for c in line:
        if c not in kosher_char:
            return False
    return True


def on_modified(self, event):
    what = 'directory' if event.is_directory else 'file'
    filename = event.src_path

    if not filename.endswith('.txt'):
        return

    logging.info("Modified %s: %s", what, event.src_path)
    # print('Checking for suspicious behavior in file')

    with open(filename) as file:
        cnt = 1
        line = file.readline()
        while line:
            if not isKosher(line):
                logging.critical("line %s: in %s was encrypted", cnt, filename)

            # print("Line {}: {}".format(cnt, line.strip()))
            line = file.readline()
            cnt += 1
        file.close()


def main():
    # config logs
    logging.basicConfig(level=logging.CRITICAL,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # read path to directory if given
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    # config event handler -
    # first is only for text files other is logging all events
    event_handler = PatternMatchingEventHandler(patterns='*.txt', ignore_directories=True)
    # log_handler = LoggingEventHandler()

    # override on_modified function in event handler
    PatternMatchingEventHandler.on_modified = on_modified

    # config of observer object
    observer = Observer()
    watch = observer.schedule(event_handler, path, recursive=False)
    # observer.add_handler_for_watch(log_handler, watch)
    observer.start()
    # main loop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
