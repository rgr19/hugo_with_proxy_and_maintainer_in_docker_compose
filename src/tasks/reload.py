#!/usr/bin/env python3.7.7
import logging
import os

import coloredlogs

from lib.FilesHandlers import EnvRead, EnvWrite, Env, FileExpandvarsWrite, YamlRewrite

logger = logging.getLogger(__name__)

logger.info("Hello logging!")


def expandvars_in_docker_compose(envFilePath, srcDir, destDir):
	logger.debug(f'{__name__}.expandvars_in_templates')
	srcYml = os.path.join(srcDir, "docker-compose.yml")
	destYml = os.path.join(destDir, "docker-compose.yml")
	FileExpandvarsWrite.by_envfile_to_file(envFilePath, srcYml, destYml)
	YamlRewrite(destYml)


def merge_env_files_in_cwd(envFileDest, *envFilesSrc: str):
	logger.debug(f'{__name__}.merge_env_files_in_cwd')
	envVars: dict = {}
	for envFile in envFilesSrc:
		envVars.update(EnvRead.as_dict(envFile))
	EnvWrite(envFileDest, Env.dict_to_env_lines(envVars))


def find_env_files(path: str):
	for root, dirs, files in os.walk(path):
		for f in files:
			if '.env' == f:
				yield os.path.join(root, f)


def main():
	envFileDest = ".env"
	envFilesSrc = find_env_files("./src/main")
	merge_env_files_in_cwd(envFileDest, *envFilesSrc)
	expandvars_in_docker_compose(envFileDest, "./src/tasks/templates", "./")



if __name__ == '__main__':
	logger = logging.getLogger(__name__)

	infoFormat = "%(asctime)s,%(msecs)03d [%(hostname)s] [%(process)d] [%(programname)s.%(name)s:%(lineno)d] %(levelname)s => %(message)s"
	coloredlogs.install(level='INFO', fmt=infoFormat, )

	main()
