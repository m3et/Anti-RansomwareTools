import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import *


def on_modified(self,  event):
    print(event.event_type)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = PatternMatchingEventHandler(patterns='*.txt', ignore_directories=True)
    FileSystemEventHandler.on_modified = on_modified
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
