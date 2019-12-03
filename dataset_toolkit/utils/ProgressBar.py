import time
import datetime


class ProgressBar:

    def __init__(self, max_count):
        self.start_time = time.time()
        self.last_time = self.start_time
        self.counter = 0
        self.max_count = max_count

    def lap(self):
        self.counter += 1
        elapsed_time = time.time() - self.last_time
        total_time = time.time() - self.start_time
        avg_time = total_time / self.counter
        self.last_time = time.time()
        end_time = avg_time * (self.max_count - self.counter)
        end_time = str(datetime.timedelta(seconds=end_time))

        print("{}/{}".format(self.counter, self.max_count))
        print("Time elapsed for last file: ", elapsed_time)
        print("Total time: ", total_time)
        print("Avg. time: ", avg_time)
        print("End time: ", end_time)
