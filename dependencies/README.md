# Requirements Lambda Layer
## Prerequisites
- Python 3.11 installed
- Permissions set on `install.sh` file
### Python 3.11 install
Assuming no previous installation of python, these are the steps I took for a new Macbook
- Install [Homebrew](https://brew.sh/)
- Use Homebrew to install `pyenv`: `brew install pyenv`
- Setup shell (Zsh) for pyenv, following instructions in the [pyenv documentation](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)
  ```
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
  echo 'eval "$(pyenv init -)"' >> ~/.zshrc
  ```
- Restart shell for changes to take effect: `exec "$SHELL"`
- Use pyenv to install python 3.11: `pyenv install 3.11`
- Set global python version using pyenv: `pyenv global 3.11`
- Check python version now 3.11: `python --version`
### Permissions on `install.sh` file
Running the `install.sh` script will probably fail due to a `permission denied` error - set the permissions on the file by running:
- `cd dependencies` (this directory)
- `chmod 744 install.sh`
## Run install script
Run the requirements install script to create a local virtual environment ("create_layer"), then install all dependencies in the directory `/python`:
`./install.sh`