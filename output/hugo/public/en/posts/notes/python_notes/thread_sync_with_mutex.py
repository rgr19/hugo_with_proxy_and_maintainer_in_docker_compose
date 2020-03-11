import sys
from contextlib import contextmanager
@contextmanager
def other_threads_suspended():
    checkinterval_original = sys.getcheckinterval()
    try:
        sys.setcheckinterval(sys.maxint)
        yield None
    finally:
        sys.setcheckinterval(checkinterval_original)

# Example usage:
with other_threads_suspended():
    print "Here we might log system state info that we do no want changed by"
    print "    another thread until we are finished logging. When logging is"
    print "    complete then other threads will be allowed to run as normal."
    print "    If the system state was entirely encapsulated by an object"
    print "    then exclusive thread access could be managed there; however,"
    print "    few systems are so clean that you can guarantee this."
