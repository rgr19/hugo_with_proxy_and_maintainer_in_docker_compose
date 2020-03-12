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
	STATUS = 'status'
	MASTER = 'master'
	LOCAL = 'local'
	ORIGIN = 'origin'
	REMOTE = 'remote'
	MESSAGE = 'message'
	CONFIG = 'config'
	FORCE = 'force'

	def __call__(self, subcommand, path):
		command = [self.GIT]
		return Executor(command) \
			.with_cwd(path) \
			.with_subcommand(subcommand)

	def git_status(self, path) -> bool:
		return self(self.STATUS, path).spawn()

	def git_config(self, path) -> bool:
		return self(self.CONFIG, path).spawn()

	def git_init_shared(self, path) -> bool:
		return self(self.INIT, path).with_flags(self.SHARED).spawn()

	def git_remote_add_origin(self, path, origin) -> bool:
		return self(self.REMOTE, path).with_

	def git_add_all(self, path) -> bool:
		return self(self.ADD, path).with_flags(self.ALL).spawn()

	def git_commit(self, path) -> bool:
		commitMessage = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.now())
		return self(self.COMMIT, path).with_kwarg(self.MESSAGE, commitMessage).spawn(exitOnError=False, quietError=True)
