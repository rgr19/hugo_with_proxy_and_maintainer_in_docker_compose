import json
import os
import time

from lib.DirectoryFormatter import DirectoryFormatter
from lib.GitExecutor import GitExecutor
from lib.common import build_logger

logger = build_logger(__name__, level="DEBUG")


class Repositories:
	Map = {}

	def __init__(self, name, path, origin):
		self.name = name
		self.path = path
		self.origin = origin

	@staticmethod
	def add(name, path, origin):
		repo = Repositories(name, path, origin)
		Repositories.Map[name] = repo
		return repo

	@staticmethod
	def get(name=None):
		if name is None:
			return Repositories.Map
		else:
			try:
				return Repositories.Map[name]
			except:
				return None

	@staticmethod
	def get_list():
		return Repositories.Map.values()


class Backuper(GitExecutor):
	configs = [
		('user.name', 'Backuper'),
		('user.email', '<>'),
	]

	def __init__(self, root: Repositories, *submodules: Repositories):
		self.root = root
		self.submodules = submodules
		self.repos = (root,) + submodules

	def init_orgins(self):
		self.git_remote_add_origin(self.root.path, self.root.origin)
		for submodule in self.submodules:
			self.git_submodule_add_origin(self.root.path, submodule.path, submodule.origin)
			self.git_submodule_set_origin(self.root.path, submodule.path, submodule.origin)

	def init_backup(self, ):
		for repo in self.repos:
			path = repo.path
			try:
				logger.info(f"Initiate backup for DIR {path}")
				self.git_init_shared(path)
				logger.info("Config backup DB...")
				for config in self.configs:
					self.git_config(*config)
			except:
				pass

	def do_backup(self, ):
		rval = True
		for repo in self.repos:
			path = repo.path
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
			logger.warning("Content directory not specified. Abort formatting.")
		else:
			logger.info("Begin content directory formatting.")
			try:
				logger.info(f"Maintainer try to reformat content at {formatterKwargs['directory']}.")
				hugo_content_formatter(**formatterKwargs)
			except Exception as err:
				logger.error(f"Maintainer failed to reformat content at {formatterKwargs['directory']} due to : {err}")
			return True


def load_settings():
	logger.info("Load project.json settings...")
	with open("project.json") as fp:
		envDict = json.load(fp)

	logger.info("Setup backuper...")

	return envDict


def setup_repositories(envDict):
	repos = Repositories.add('root', envDict['repo']['dir'], envDict['repo']['origin'])
	for name, repo in envDict['repo']['submodules'].items():
		repoDir = repo['dir']
		if os.path.exists(repoDir):
			Repositories.add(name, repo['dir'], repo['origin'])
		else:
			logger.exception(f"Repo DIR {repoDir} does not exist. Abort.")
			return None
	return repos


def setup_backuper(repos):
	backuper = Backuper(repos.get('root'), *repos.get_list())
	backuper.init_backup()
	backuper.init_orgins()
	backuper.do_backup()
	return backuper


def setup_formatter_kwargs(repos, formatterKwargs):
	if not Repositories.get('content'):
		raise logger.warning("Submodule 'content' was not provided. Hugo formatter disabled.")
	else:
		formatterKwargs['directory'] = repos.get('content')


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

	logger.info("Maintainer begin LOOP:")
	while True:
		envDict = load_settings()
		repos = setup_repositories(envDict)
		if repos:
			backuper = setup_backuper(repos)
			setup_formatter_kwargs(repos, formatterKwargs)
			maintenance(backuper, formatterKwargs)
		time.sleep(int(envDict['maintainer']['intervals']))


if __name__ == '__main__':
	main()
