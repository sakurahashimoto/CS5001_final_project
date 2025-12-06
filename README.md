##### CS5001 Final Project

### Description

This project is a simple TODO application that helps you make progress on difficult tasks
by prompting you to break tasks up into mangeable chunks and gamifying getting stuff done.

### Running

[uv](https://github.com/astral-sh/uv) is used to manage dependencies and provide a shared
environment.

To get started:
* Fetch all required dependencies: `uv sync`
* Run a python file: `uv run file_name`

### Sakura Notes

## Navigating

## VSCode

1. Open `~/Documents/github/CS5001_final_project/`
    * File -> Open Folder

## Terminal

1. Open `Ghostty`
2. `cd ~/Documents/github/CS5001_final_project/`

## Using jj

# Steps
1. Make some code change
2. Add a change description with: `jj describe`
    * To exit the text editor: `ctrl + o` then `enter` then `ctrl + x`
3. Push the change to github with: `jj git push -c @`
4. On github create a new pull request
5. Rebase and merge the pull request
6. Pull down latest changes: `jj git fetch`
7. Prepare to make new changes: `jj rebase -d main`
