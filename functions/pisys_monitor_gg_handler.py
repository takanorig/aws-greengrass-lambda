from threading import Timer

from pisysmonitor.pisys_monitor import PisysMonitor

__pisys_monitor = None


def run():
    """
    PisysMonitor を非同期で定期実行します。
    """

    global __pisys_monitor
    if (__pisys_monitor is None):
        __pisys_monitor = PisysMonitor()

    __pisys_monitor.monitor()

    Timer(60, run).start()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return


# Start the function
run()
