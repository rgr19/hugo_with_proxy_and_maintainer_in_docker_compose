import os
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
			try:
				logger.info(f"Initiate backup for DIR {path}")
				self.git_init_shared(path)
				logger.info("Config backup DB...")
				for config in self.configs:
					self.git_config(*config)
			except:
				pass
		self.do_backup()

	def do_backup(self, ):
		rval = True
		for path in self.paths:
			logger.info(f"Try to backup in DIR {path}")
			try:
				self.git_add_all(path)
				rval &= self.git_commit(path)
			except Exception as err:
				logger.error(f"Backup did not succeed : {err}.")
		return rval


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


def main():
	formatterKwargs = {
		'directory': None,
		'excludedDirs': [
			'code', '.git', 'github', 'raw', '.vscode', '.rawdata',
			'codes', 'src', 'node_modules', 'venv', '.idea'
		],
		'excludedFiles': [],
		'includedExtensionsGlobs': ['.md', '.markdown', '.git']
	}

	MAINTENANCE_INTERVALS = os.environ['MAINTAINER_INTERVALS']
	PROJECT_ROOT = os.environ['PROJECT_ROOT']
	PROJECT_CONTENT = os.environ['PROJECT_CONTENT']
	PROJECT_HUGO = os.environ['PROJECT_HUGO']
	PROJECT_ROOT_ORIGIN = os.environ['PROJECT_ROOT_ORIGIN']
	PROJECT_CONTENT_ORIGIN = os.environ['PROJECT_CONTENT_ORIGIN']
	PROJECT_HUGO_ORIGIN = os.environ['PROJECT_HUGO_ORIGIN']

	formatterKwargs['directory'] = PROJECT_CONTENT
	backuper = Backuper(PROJECT_ROOT, PROJECT_CONTENT, PROJECT_HUGO)

	logger.info("Maintainer begin LOOP:")
	while True:
		maintenance(backuper, formatterKwargs)
		time.sleep(MAINTENANCE_INTERVALS)


if __name__ == '__main__':
	main()
