#!/usr/bin/env python3.7.7
import logging
import os

import coloredlogs
import toml

from lib.FilesHandlers import EnvRead, EnvWrite, Env, FileExpandvarsWrite, YamlRewrite

logger = logging.getLogger(__name__)
logger.info("Hello logging!")


def get_hugo_theme_version(themePath):
	THEME_TOML = 'theme.toml'
	PATH_THEME_TOML = os.path.join(themePath, THEME_TOML)
	with open(PATH_THEME_TOML, 'r') as fp:
		parsedToml = toml.loads(fp.read())
		return parsedToml['min_version']


def expandvars_in_docker_compose(envVars, srcDir, destDir):
	logger.debug(f'{__name__}.expandvars_in_templates')
	srcYml = os.path.join(srcDir, "docker-compose.yml")
	destYml = os.path.join(destDir, "docker-compose.yml")
	FileExpandvarsWrite.by_keywords_to_file(srcYml, destYml, **envVars)
	YamlRewrite(destYml)


def merge_env_files_in_cwd(envFileDest, *envFilesSrc: str):
	logger.debug(f'{__name__}.merge_env_files_in_cwd')
	envVars: dict = {}
	for envFile in envFilesSrc:
		envVars.update(EnvRead.as_dict(envFile))
	EnvWrite(envFileDest, Env.dict_to_env_lines(envVars))
	FileExpandvarsWrite.by_envfile_to_file(envFileDest)


def find_env_files(path: str):
	for root, dirs, files in os.walk(path):
		for f in files:
			if '.env' == f:
				yield os.path.join(root, f)


def main():
	MAIN = 'main'
	TASKS = 'tasks'
	TEMPLATES = 'templates'
	SRC = 'src'
	THEMES = 'themes'
	DOT_ENV = '.env'
	DIR_ROOT = '.'
	DIR_SRC_TASKS = os.path.join(SRC, TASKS)
	DIR_SRC_MAIN = os.path.join(SRC, MAIN)
	DIR_SRC_TASKS_TEMPLATES = os.path.join(DIR_SRC_TASKS, TEMPLATES)

	envFilesSrc = find_env_files(DIR_SRC_MAIN)
	merge_env_files_in_cwd(DOT_ENV, *envFilesSrc)

	envVars: dict = EnvRead.as_dict(DOT_ENV)

	hugoThemePath = os.path.join(envVars['HOST_HUGO_ROOT'], SRC, THEMES, envVars['HUGO_THEME_BLOG'])
	hugoThemeVersion = get_hugo_theme_version(hugoThemePath)

	envVars['HUGO_VERSION_BLOG'] = hugoThemeVersion
	hugoThemePath = os.path.join(envVars['HOST_HUGO_ROOT'], SRC, THEMES, envVars['HUGO_THEME_DOCS'])
	hugoThemeVersion = get_hugo_theme_version(hugoThemePath)
	envVars['HUGO_VERSION_DOCS'] = hugoThemeVersion

	expandvars_in_docker_compose(envVars, DIR_SRC_TASKS_TEMPLATES, DIR_ROOT)


if __name__ == '__main__':
	logger = logging.getLogger(__name__)

	infoFormat = "%(asctime)s,%(msecs)03d [%(hostname)s] [%(process)d] [%(programname)s.%(name)s:%(lineno)d] %(levelname)s => %(message)s"
	coloredlogs.install(level='INFO', fmt=infoFormat, )

	main()
