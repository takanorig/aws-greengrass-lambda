from threading import Timer

from pisys_monitor import PisysMonitor


def run():
    """
    PisysMonitor を非同期で定期実行します。
    """

    pisys_monitor = PisysMonitor()
    Timer(5, pisys_monitor.monitor).start()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return


# Start the function
run()
