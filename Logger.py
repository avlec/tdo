

# Logger is a singleton class used for logging
# errors and behaviour throughout the lifetime
# of the program.
class Logger():
    class __Logger:
        def __init__(self, write_path):
            self.write_path = write_path

        def __str__(self):
            return repr(self) + self.write_path

    instance = None

    # Used for creating references to the object
    # @params
    #   str write_path: used to direct file output of logger
    def __init__(self, write_path):
        if not Logger.instance:
            if write_path:
                Logger.instance = Logger.__Logger(write_path)
            else:
                Logger.instance = Logger.__Logger('logfile.txt')

    def __getattr__(self, name):
        return getattr(self.instance, name)
