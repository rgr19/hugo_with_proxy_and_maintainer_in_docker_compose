#!/usr/bin/env python3.7
import logging
import os
import shutil

from lib.common import rreplace, move_tree
from lib.pygtrie import StringTrie

logger = logging.getLogger(__name__)


class DirectoryFormatter(object):

	def __init__(self, directory, excludedDirs, excludedFiles, includedExtensionGlobs):

		self.directory: str = directory
		self.excludedRoots: set = set()
		self.excludedDirs: set = set(excludedDirs) if excludedDirs else set()
		self.excludedFiles: set = set(excludedFiles) if excludedFiles else set()
		self.includedExtensions: set = set(map(lambda x: x.replace('.', '', 1), includedExtensionGlobs))

		self.not_in_excluded_dirs = lambda d: all(map(lambda e: e not in d, self.excludedDirs))
		self.not_in_excluded_files = lambda f: all(map(lambda e: e not in f, self.excludedFiles))
		self.in_included_extensions = lambda f: any(map(lambda e: e in f.rsplit('.', 1)[-1], self.includedExtensions))

		self.is_changeable_filepath = lambda f: \
			self.not_in_excluded_dirs(f) \
			and self.not_in_excluded_files(f) \
			and self.in_included_extensions(f)

	def rename_dirs_with(self, word, replace):
		logger.info(
			f'RENAME DIRS WITH in DIR "{self.directory}" with WORD {word} and REPLACE {replace}:')

		for root, dirs, files in os.walk(self.directory, topdown=False):
			for d in dirs:
				if word == d:
					dpath = os.path.join(root, d)
					if self.not_in_excluded_dirs(dpath):
						dpathNew = rreplace(dpath, word, replace)
						logger.debug(f'OLD: {dpath} => NEW: {dpathNew}')
						move_tree(dpath, dpathNew)

	def rename_files_with(self, word, replace):
		logger.info(
			f'RENAME FILES WITH in DIR "{self.directory}" with WORD {word} and REPLACE {replace}:')

		for root, dirs, files in os.walk(self.directory, topdown=False):
			for f in files:
				if word == f:
					fpath = os.path.join(root, f)
					if self.is_changeable_filepath(fpath):
						fpathNew = fpath.replace(word, replace)
						logger.debug(f'OLD: {fpath} => NEW: {fpathNew}')
						shutil.move(fpath, fpathNew)

	def change_paths_to_lowercase(self):
		logger.info(
			f'CHANGE FILE NAMES TO LOWERCASE in DIR "{self.directory}":')

		for root, dirs, files in os.walk(self.directory, topdown=False):
			paths = StringTrie()
			for f in files:
				fpath = os.path.join(root, f)
				if self.is_changeable_filepath(fpath):
					paths.add(fpath)
			for d in dirs:
				dpath = os.path.join(root, d)
				if self.not_in_excluded_dirs(dpath):
					paths.add(dpath)
			for path in paths:
				if not path.isupper() and not path.islower():
					while len(path) > 1:
						path, _ = os.path.split(path)
						pathNew = path.lower()
						logger.debug(f'OLD: {path} => NEW: {pathNew}')
						move_tree(path, pathNew)

	def replace_word_in_content_of_file_with_pattern(self, word, replace, pattern):
		logger.info(
			f'REPLACE WORD IN CONTENT OF FILE WITH PATTERN in DIR "{self.directory}" with WORD {word} and REPLACE {replace}:')
		filesList = StringTrie()

		for root, dirs, files in os.walk(self.directory, topdown=True):
			for f in files:
				fpath = os.path.join(root, f)
				filesList.add(fpath)

		filesList = filter(self.not_in_excluded_dirs, filesList.iterkeys())
		filesList = filter(self.not_in_excluded_files, filesList)
		filesList = list(filter(self.in_included_extensions, filesList))

		for fpath in filesList:
			if pattern in fpath:
				with open(fpath, 'r') as fp:
					text = fp.read()
				if not word in text:
					continue
				logger.debug(
					f'OLD: {fpath} WORD: {word} => REPLACE: {replace}')
				text = text.replace(word, replace)
				with open(fpath, 'w') as fp:
					print(text, file=fp)


