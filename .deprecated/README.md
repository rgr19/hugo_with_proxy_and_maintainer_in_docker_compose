# Initial setup

Go to github, create two repositories:

- <user>.hugo.io :
    - private to hide src of blog

- <user>.github.io :
  - public or private if we have premium github to hide static site and password
  - set it as github site and enforce https encryption

After that go to script `setup_git_and_connect_to_github.sh`.

Change its content to match your email, user and cname, and execute.

It will setup your local directory as git repo, link it to github repository <user>.hugo.io, add git submodule in public directory and link it to <user>.github.io githu repository.

Go to godaddy and buy some domain <cname>, then write it to CNAME file.

Write <password_raw> to PASSWORD_RAW file, it will be simply hashed to <hashed_password> and saved to PASSWORD_HASHED file. Then website content will be hidden under <cname>/<hashed_password>.


## Requirements

- hugo
- git
- git-lfs
- bash
- python

# Development and publishing

> NOTE: All files in content and directories shall have lower case and be without spaces.

For local development execute script `run.sh` from root of project and let it run, hugo will
provide link that should be open in browser. Any change will trigger rebuild of site that
takes up to 1[s] for big content.

For uploading site to github execute script `upload.sh` from root of project. It will first
clean whole repo from any garbage then upload new content.

Both of this files use `reformat.sh` script that is internal. It require to have directory _password, CNAME, IGNORED_FILES with proper python list, config.toml.template, PASSWORD_RAW, config.py, password_generator.py .

# Images

To make images use some screenshot tool with keybinding `alt+a` with option to copy to clippoard.

To paste images use extension `paste image` with keybinding `alt+v`.

Make sute to have that settings in vs-code:

```
	"settings": {
		"pasteImage.namePrefix": "${currentFileNameWithoutExt}_",
		"pasteImage.forceUnixStyleSeparator": true,
		"pasteImage.filePathConfirmInputBoxMode": "onlyName",
		"pasteImage.defaultName": "Y-MM-DD_HH-mm-ss",
		"pasteImage.path": "/${currentFileDir}/${currentFileNameWithoutExt}/images",
		"pasteImage.basePath": "/${projectRoot}/",
		"pasteImage.insertPattern": "![${imageFileNameWithoutExt}](images/${imageFileName}${imageSyntaxSuffix}"
	}
```
