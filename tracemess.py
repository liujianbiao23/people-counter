#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.4.1
#
# SOURCES
#    https://stackoverflow.com/questions/3056048/filename-and-line-number-of-python-script
#    https://pypi.python.org/pypi/dweepy/


import os
import uuid
import json
import ts_dweepy
import time
import datetime
from inspect import currentframe


def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno


class TraceMess:

    def __init__(self, platform, verbose=False, src="not specified"):
        self.trace_on = False
        self.hb_freq = 60
        self.hb_time = datetime.datetime(2000, 1, 1, 1, 1, 1, 1)
        self.run_stamp = {
            "mess-type": "EXEC",
            "run-id": str(uuid.uuid4()),
            "run-time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "run-status": "init",
            "run-platform": os.uname()[1],
            "run-source": src,
            "verbose": verbose,
            "timer-start": None,
            "timer-stop": None,
            "version": "0.3.0"
        }

    def start(self, on=False):
        self.trace_on = on

        self.run_stamp["run-status"] = "start"
        self.run_stamp["run-time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.gmtime())
        if self.trace_on is True:
            if self.run_stamp["verbose"] is True:
                print(json.dumps(self.run_stamp))
            else:
                print(json.dumps({"INFO": {"trace started":
                                           self.run_stamp["run-time"]}}))

        return self

    def stop(self):
        self.trace_on = False

        self.run_stamp["run-status"] = "stop"
        self.run_stamp["run-time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.gmtime())
        if self.trace_on is True:
            if self.run_stamp["verbose"] is True:
                print(json.dumps(self.run_stamp))
            else:
                print(json.dumps({"INFO": {"trace stopped":
                                           self.run_stamp["run-time"]}}))

    def time_start(self, mess=None):
        if self.trace_on is False:
            return

        # start the timer
        self.run_stamp["timer-start"] = datetime.datetime.now()
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "INFO",
                              "run-id": self.run_stamp["run-id"],
                              "timer-start": t, "mess-text": mess}))
        else:
            print(json.dumps({"INFO": {"timer-start": t, "mess-text": mess}}))

    def time_stop(self, mess=None):
        if self.trace_on is False:
            return

        # stop the timer
        self.run_stamp["timer-stop"] = datetime.datetime.now()
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "INFO",
                              "run-id": self.run_stamp["run-id"],
                              "timer-stop": t, "mess-text": mess}))
        else:
            print(json.dumps({"INFO": {"timer-stop": t, "mess-text": mess}}))

    def time_elapsed(self, mess=None):
        if self.trace_on is False:
            return

        # return the total number of seconds between the start and end interval
        t = (self.run_stamp["timer-stop"]
             - self.run_stamp["timer-start"]).total_seconds()

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "INFO",
                              "run-id": self.run_stamp["run-id"],
                              "timer-interval": t, "mess-text": mess}))
        else:
            print(json.dumps({"INFO": {"timer-interval": t,
                                       "mess-text": mess}}))

    def info(self, mess):
        if self.trace_on is False:
            return

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "INFO",
                              "run-id": self.run_stamp["run-id"],
                              "mess-text": mess}))
        else:
            print(json.dumps({"INFO": mess}))

    def error(self, mess):
        if self.trace_on is False:
            return

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "ERROR",
                              "run-id": self.run_stamp["run-id"],
                              "mess-text": mess}))
        else:
            print(json.dumps({"ERROR": mess}))

    def warning(self, mess):
        if self.trace_on is False:
            return

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "WARNING",
                              "run-id": self.run_stamp["run-id"],
                              "mess-text": mess}))
        else:
            print(json.dumps({"WARNING": mess}))

    def feature(self, mess):
        if self.trace_on is True:
            if self.run_stamp["verbose"] is True:
                print(json.dumps({"mess-type": "FEATURE",
                                  "run-id": self.run_stamp["run-id"],
                                  "mess-text": mess}))
            else:
                print(json.dumps({"FEATURE": mess}))

        try:
            ts_dweepy.dweet_for(self.run_stamp["run-platform"],
                                {"mess-type": "FEATURE",
                                 "run-id": self.run_stamp["run-id"],
                                 "mess-text": mess})
        except requests.exceptions.RequestException as e:
            #exc_info = sys.exc_info()
            print("Communication error within ts_dweepy")
            #pass

    def heart_freq(self, freq):
        self.hb_freq = freq

    def heartbeat(self, mess):
        t = datetime.datetime.now()
        if (t - self.hb_time).total_seconds() > self.hb_freq:
            self.hb_time = t

            if self.trace_on is True:
                if self.run_stamp["verbose"] is True:
                    print(json.dumps({"mess-type": "HEARTBEAT",
                                      "run-id": self.run_stamp["run-id"],
                                      "mess-text": mess}))
                else:
                    print(json.dumps({"HEARTBEAT": mess}))

            try:
                ts_dweepy.dweet_for(self.run_stamp["run-platform"],
                                {"mess-type": "HEARTBEAT",
                                 "run-id": self.run_stamp["run-id"],
                                 "mess-text": mess})
            except requests.exceptions.RequestException as e:
                #exc_info = sys.exc_info()
                print("Communication error within ts_dweepy")
                #pass
