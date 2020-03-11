import collections
import hashlib
import logging
import os
import shutil

import coloredlogs


def build_logger(name, level='INFO'):
	loggerFormat = collections.OrderedDict(
		dateTime="%(asctime)s,%(msecs)03d",
		hostname="[%(hostname)s]",
		process="[%(process)d]",
		code="[%(programname)s.%(name)s:%(lineno)d]",
		level="%(levelname)s",
		message="=> %(message)s",
	)
	loggerFormat = ' '.join(loggerFormat.values())
	coloredlogs.install(level=level, fmt=loggerFormat, )
	return logging.getLogger(name)


def rreplace(s, old, new, nitems=1):
	return new.join(s.rsplit(old, nitems))


def move_tree(fromRoot, toRoot):
	logger.debug(F'MOVE TREE : FROM {fromRoot} => TO {toRoot}:')
	if not os.path.exists(toRoot):
		logger.debug(F'MOVE TREE => FRESH : {toRoot}:')
		shutil.move(fromRoot, toRoot)
	else:
		logger.debug(F'MOVE TREE => MERGE : {fromRoot} AND {toRoot}:')
		for srcDir, dirs, files in os.walk(fromRoot):
			destDir = srcDir.replace(fromRoot, toRoot, 1)
			if not os.path.exists(destDir):
				os.makedirs(destDir)
			for f in files:
				srcF = os.path.join(srcDir, f)
				destF = os.path.join(destDir, f)
				if os.path.exists(destF):
					os.remove(destF)
				shutil.copy(srcF, destDir)
		shutil.rmtree(fromRoot, ignore_errors=True, onerror=lambda e: logger.exception(f'MOVE TREE error => {e}'))


def get_dir_md5(rootPath):
	"""Build a tar file of the directory and return its md5 sum"""
	hash = hashlib.md5()
	for root, dirs, files in os.walk(rootPath, topdown=True):

		dirs.sort(key=os.path.normcase)
		files.sort(key=os.path.normcase)

		for filename in files:
			filepath = os.path.join(root, filename)
			# If some metadata is required, add it to the checksum
			# 1) filename (good idea)
			hash.update(filename.encode('utf-8'))
			# 2) mtime (possibly a bad idea)
			try:
				st = os.stat(filepath)
				# hash.update(struct.pack('d', st.st_mtime))
				# 3) size (good idea perhaps)
				hash.update(bytes(st.st_size))
			except Exception as err:
				# 4) content
				f = open(filepath, 'rb')
				for chunk in iter(lambda: f.read(65536), b''):
					hash.update(chunk)

	return hash.hexdigest()


logger = build_logger(__name__)
