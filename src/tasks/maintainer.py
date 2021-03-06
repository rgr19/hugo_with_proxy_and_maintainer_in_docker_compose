import enum
import json
import os
import time
from typing import List

import datas

from lib.DirectoryFormatter import DirectoryFormatter
from lib.GitExecutor import GitExecutor
from lib.common import build_logger

logger = build_logger(__name__, level="DEBUG")


class RepositoryType(enum.Enum):
	root = 1
	submodule = 2


class Repositories:
	Map = datas.autodict()

	def __init__(self, rootPath, name, path, origin, type: RepositoryType, depth):
		self.name = name
		self.path = path
		self.origin = origin
		self.type = type
		self.rootPath = rootPath
		self.depth = depth

	def __str__(self):
		return f"Repositories(name: {self.name}, path: {self.path}, origin: {self.origin}, type: {self.type}, rootPath: {self.rootPath}, depth: {self.depth})"

	def __repr__(self):
		return self.__str__()

	@staticmethod
	def add(name, path, origin, type, rootPath=None, depth=0):
		repo = Repositories(rootPath, name, path, origin, type, depth)
		Repositories.Map[type][name] = repo
		return repo

	@staticmethod
	def get(name=None, type: RepositoryType = None):
		try:
			if name is None and type is None:
				return Repositories.Map
			elif name is None:
				return Repositories.Map[type]
			else:
				for type in RepositoryType:
					if name in Repositories.Map[type]:
						return Repositories.Map[type][name]
		except:
			return None

	@staticmethod
	def get_list(type: RepositoryType = None):
		if type is None:
			repos = []
			for type in RepositoryType:
				repos.extend(Repositories.Map[type].values())
			repos = sorted(repos, key=lambda r: r.depth)
			return repos
		else:
			return Repositories.Map[type].values()


class Backuper(GitExecutor):
	configs = [
		('user.name', 'Backuper'),
		('user.email', '<>'),
	]

	def __init__(self, reposList: List[Repositories]):
		self.reposList = reposList

	def init_orgins(self):
		for repo in self.reposList:
			if repo.type is RepositoryType.root:
				self.git_remote_add_origin(repo.path, repo.origin)
			elif repo.type is RepositoryType.submodule:
				self.git_submodule_add_origin(repo.rootPath, repo.path, repo.origin)
				self.git_submodule_set_origin(repo.rootPath, repo.path, repo.origin)

	def init_backup(self, ):
		for repo in self.reposList:
			if repo.rootPath is not None:
				path = os.path.join(repo.rootPath, repo.path)
			else:
				path = repo.path
			try:
				logger.info(f"Initiate backup for DIR {path}")
				self.git_init_shared(path)
				logger.info("Config backup DB...")
				for config in self.configs:
					self.git_config(path, *config)
			except:
				pass

	def do_backup(self, ):
		rval = True
		for repo in self.reposList[::-1]:  # we start from leafs, finish at root
			if repo.rootPath is not None:
				path = os.path.join(repo.rootPath, repo.path)
			else:
				path = repo.path
			logger.info(f"Try to backup in DIR {path}")
			try:
				if self.git_add_all(path):
					rval &= self.git_commit(path)
				else:
					rval = False
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

	return envDict


def setup_submodules(repos, name, repoDict, rootPath, depth):
	repoDir = repoDict['dir']
	if os.path.exists(os.path.join(rootPath, repoDir)):
		repos.add(name, repoDir, repoDict['origin'], RepositoryType.submodule, rootPath, depth)
	else:
		logger.exception(f"Repo DIR {repoDir} does not exist. Abort.")
		return None
	if 'submodules' in repoDict:
		for name, subrepoDict in repoDict['submodules'].items():
			setup_submodules(repos, name, subrepoDict, os.path.join(rootPath, repoDir), depth + 1)
	return repos


def setup_repositories(envDict):
	repos = Repositories.add('root', envDict['repo']['dir'], envDict['repo']['origin'], RepositoryType.root, depth=0)
	for name, repoDict in envDict['repo']['submodules'].items():
		setup_submodules(repos, name, repoDict, envDict['repo']['dir'], depth=1)
	return repos


def setup_backuper(repos):
	logger.info("Setup backuper...")
	backuper = Backuper(repos.get_list())
	backuper.init_backup()
	backuper.init_orgins()
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
