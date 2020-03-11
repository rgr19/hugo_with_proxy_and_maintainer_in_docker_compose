import argparse
import os
import sys
import time

from lib.DirectoryFormatter import DirectoryFormatter
from lib.GitExecutor import GitExecutor
from lib.common import build_logger

logger = build_logger(__name__, level="DEBUG")


class Backuper(GitExecutor):
	configs = [
		('user.name', 'Backuper'),
		('user.email', '<>'),
	]

	def __init__(self, *paths):
		self.paths = paths

	def init_backup(self, ):
		for path in self.paths:
			logger.info(f"Initiate backup for DIR {path}")
			self.git_init_shared(path)
			logger.info("Config backup DB...")
			for config in self.configs:
				self.git_config(*config)
		self.do_backup()

	def do_backup(self, ):
		for path in self.paths:
			logger.info(f"Try to backup in DIR {path}")
			try:
				self.git_add_all(path)
				return self.git_commit(path)
			except Exception as err:
				logger.error(f"Backup did not succeed : {err}.")


def hugo_content_formatter(directory, excludedDirs=None, excludedFiles=None, includedExtensionsGlobs=None):
	SPACE = ' '
	INDEX = 'index'
	UNDERSCORE = '_'
	UNDERSCORE_INDEX = UNDERSCORE + INDEX

	formatter = DirectoryFormatter(directory, excludedDirs, excludedFiles, includedExtensionsGlobs)
	formatter.rename_dirs_with(UNDERSCORE_INDEX, INDEX)
	formatter.rename_files_with(UNDERSCORE_INDEX, INDEX)
	formatter.rename_files_with(SPACE, UNDERSCORE)
	formatter.rename_files_with(UNDERSCORE + UNDERSCORE, UNDERSCORE)
	formatter.change_paths_to_lowercase()
	formatter.replace_word_in_content_of_file_with_pattern(UNDERSCORE_INDEX, INDEX, INDEX)

	return True


def maintenance(backuper, formatterKwargs):
	if backuper.do_backup():
		logger.info("Begin maintenance...")
		if formatterKwargs['directory'] is None:
			logger.error("formatterKwargs key 'directory' need to have non-none value.")
		else:
			logger.info("Reformat data begin")
			try:
				logger.info(f"Maintainer try to reformat content at {formatterKwargs['directory']}.")
				hugo_content_formatter(**formatterKwargs)
			except Exception as err:
				logger.error(f"Maintainer failed to reformat content at {formatterKwargs['directory']} due to : {err}")
			return True


def main(argv):
	formatterKwargs = {
		'directory': None,
		'excludedDirs': [
			'code', '.git', 'github', 'raw', '.vscode', '.rawdata',
			'codes', 'src', 'node_modules', 'venv', '.idea'
		],
		'excludedFiles': [],
		'includedExtensionsGlobs': ['.md', '.markdown', '.git']
	}

	mainParser = argparse.ArgumentParser(
		prog="MAINTAINER", description="Backup and content reformatter.")

	mainParser.add_argument('-e', '--projectDirectory', dest='PROJECT_ROOT', required=False, default='./')
	mainParser.add_argument('-f', '--contentDirectory', dest='PROJECT_CONTENT', required=False, default='./content')
	mainParser.add_argument('-d', '--maintenanceIntervals', dest='MAINTENANCE_INTERVALS', required=False, default=10, type=int)

	kwargv = vars(mainParser.parse_args(argv))

	MAINTENANCE_INTERVALS = kwargv['MAINTENANCE_INTERVALS']
	PROJECT_ROOT = kwargv['PROJECT_ROOT']
	PROJECT_CONTENT = kwargv['PROJECT_CONTENT']

	formatterKwargs['directory'] = PROJECT_CONTENT
	backuper = Backuper(PROJECT_ROOT, PROJECT_CONTENT)


	logger.info("Maintainer begin LOOP:")
	while True:
		maintenance(backuper, formatterKwargs)
		time.sleep(MAINTENANCE_INTERVALS)


if __name__ == '__main__':
	main(sys.argv[1:])
