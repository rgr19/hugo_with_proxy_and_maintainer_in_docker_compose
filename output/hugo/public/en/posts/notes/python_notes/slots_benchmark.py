import time
import sys
import gc

gc.disable()
sys.setcheckinterval(sys.maxsize//2)

class WithSlots(object):
	__slots__ = ('a', 'b', 'c')

class WithSlotsAndCtor(object):
	__slots__ = ('a', 'b', 'c')

	def __init__(self):
		self.a = 1
		self.b = 2
		self.c = 3

class WithoutSlots(object):
	pass

class WithoutSlotsAndCtor(object):
	def __init__(self):
		self.a = 1
		self.b = 2
		self.c = 3

def benchmark(cls):
	t = time.time
	l = []

	for i in xrange(5):
		s = t()

		for i in xrange(100000):
			cls()

		l.append(t() - s)

	return l

def print_benchmarks(*classes):
	columns = [
		{'title': '',     'func': lambda cls, dur: cls.__name__},
		{'title': 'Avg.', 'func': lambda cls, dur: '%.3f' % (sum(dur) / len(dur))},
		{'title': 'Min.', 'func': lambda cls, dur: '%.3f' % min(dur)},
		{'title': 'Max.', 'func': lambda cls, dur: '%.3f' % max(dur)},
	]

	rows = []
	for cls in classes:
		durations = benchmark(cls)
		rows.append([col['func'](cls, durations) for col in columns])

	widthes = [max(len(row[i]) for row in rows) for i in xrange(len(columns))]

	print (' | '.join(col['title'].ljust(widthes[i]) for i, col in enumerate(columns)))
	for row in rows:
		print ('-+-'.join('-' * w for w in widthes))
		print (' | '.join(row[i].ljust(widthes[i]) for i in xrange(len(columns))))

#	c1_lenth = max(len(cls.__name__ for cls in classes))

#	print ' | '.join(' ' * c1_length

print_benchmarks(WithSlots, WithSlotsAndCtor, WithoutSlots, WithoutSlotsAndCtor)

#print 'Avg: %.4f' % (sum(durations) / len(durations))
#print 'Min: %.4f' % min(durations)
#print 'Max: %.4f' % max(durations)
