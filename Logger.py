

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
            Logger.instance = Logger.__Logger(write_path)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def log(self, msg, status):
        if not status:
            status = "Unspecified"
        with open(self.instance.write_path, 'a+') as out_stream:
            out_stream.write("%s: %s" % (status, msg))
            out_stream.close()
