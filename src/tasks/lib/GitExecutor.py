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

	def git_status(self, path, *argv) -> bool:
		return self(self.STATUS, path).with_args(*argv).spawn()

	def git_config(self, path, *argv) -> bool:
		return self(self.CONFIG, path).with_args(*argv).spawn()

	def git_init_shared(self, path, *argv) -> bool:
		return self(self.INIT, path).with_flags(self.SHARED).with_args(*argv).spawn()

	def git_add_all(self, path, *argv) -> bool:
		return self(self.ADD, path).with_flags(self.ALL).with_args(*argv).spawn()

	def git_commit(self, path, *argv) -> bool:
		commitMessage = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.now())
		return self(self.COMMIT, path).with_kwarg(self.MESSAGE, commitMessage).with_args(*argv).spawn(exitOnError=False, quietError=True)
