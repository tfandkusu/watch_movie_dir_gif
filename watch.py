import os
import time
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileCreatedEvent
from watchdog.observers import Observer
from pathlib import PurePath
import subprocess
import signal


class Mp4FileSystemEventHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        if(type(event) == FileCreatedEvent):
            src_path = event.src_path
            pp = PurePath(src_path)
            if pp.suffix != '.gif':
                output_path = "%s/%s.gif" % (
                    os.path.dirname(src_path), pp.stem)
                subprocess.run(['ffmpeg', '-i', event.src_path, '-vf',
                                'scale=320:-1', '-r', '10', output_path])


exit_flag = False


def handle_exit(sig, frame):
    global exit_flag
    exit_flag = True


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

path = "%s/movie" % os.environ['HOME']
event_handler = Mp4FileSystemEventHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()
while exit_flag == False:
    time.sleep(1)

observer.stop()
observer.join()
