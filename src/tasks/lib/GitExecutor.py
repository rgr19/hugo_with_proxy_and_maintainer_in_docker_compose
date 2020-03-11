import os
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

	def __call__(self, subcommand: str = None):
		gitRepository = os.environ['GIT_REPOSITORY']
		command = [self.GIT]
		return Executor(command) \
			.with_cwd(gitRepository) \
			.with_subcommand(subcommand)

	def git_status(self, *argv) -> bool:
		return self(self.STATUS).with_args(*argv).spawn()

	def git_config(self, *argv) -> bool:
		return self(self.CONFIG).with_args(*argv).spawn()

	def git_init_shared(self, *argv) -> bool:
		return self(self.INIT).with_flags(self.SHARED).with_args(*argv).spawn()

	def git_add_all(self, *argv) -> bool:
		return self(self.ADD).with_flags(self.ALL).with_args(*argv).spawn()

	def git_commit(self, *argv) -> bool:
		commitMessage = '{:%Y_%m_%d_%H_%M_%S}'.format(datetime.now())
		return self(self.COMMIT).with_kwarg(self.MESSAGE, commitMessage).with_args(*argv).spawn(exitOnError=False, quietError=True)
