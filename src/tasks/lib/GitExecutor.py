from datetime import datetime

from lib.Executor import ExecutorCallerAbstract, Executor


class GitExecutor(ExecutorCallerAbstract):
	GIT = 'git'
	INIT = 'init'
	BARE = 'bare'
	SHARED = 'shared'
	COMMIT = 'commit'
	PUSH = 'push'
	ADD = 'add'
	ALL = 'all'
	MASTER = 'master'
	LOCAL = 'local'
	ORIGIN = 'origin'
	REMOTE = 'remote'
	MESSAGE = 'message'
	CONFIG = 'config'
	FORCE = 'force'
	SUBMODULE = 'submodule'
	SET_URL = 'set-url'

	def __call__(self, subcommand, path):
		command = [self.GIT]
		return Executor(command) \
			.with_cwd(path) \
			.with_subcommand(subcommand)

	def git_config(self, path) -> bool:
		return self(self.CONFIG, path).spawn()

	def git_init_shared(self, path) -> bool:
		return self(self.INIT, path).with_flags(self.SHARED).spawn()

	def git_remote_add_origin(self, path, originUrl) -> bool:
		return self(self.REMOTE, path).with_args(self.ADD, self.ORIGIN, originUrl).spawn()

	def git_submodule_add_origin(self, rootPath, path, originUrl) -> bool:
		return self(self.SUBMODULE, rootPath).with_args(self.ADD, originUrl, path).spawn()

	def git_submodule_set_origin(self, rootPath, path, originUrl) -> bool:
		return self(self.SUBMODULE, rootPath).with_args(self.SET_URL, path, originUrl).spawn()

	def git_add_all(self, path) -> bool:
		return self(self.ADD, path).with_flags(self.ALL).spawn()

	def git_commit(self, path) -> bool:
		commitMessage = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.now())
		return self(self.COMMIT, path).with_kwarg(self.MESSAGE, commitMessage).spawn(exitOnError=False, quietError=True)
