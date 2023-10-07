# Lab 2: Programming in Python

### Learning objectives

After completing this lab you will be able to:

* Understand ...
* Use ...
* Control ...

The purpose of this laboratory exercise is to ...

### Table of contents

* [Pre-Lab preparation](#preparation)
* [Part 1: ...](#part1)
* [Part 2: ...](#part2)
* [Part 3: ...](#part3)
* [(Optional) Experiments on your own](#experiments)
* [References](#references)

### Components list

* ESP32 board, USB cable

<a name="preparation"></a>

## Pre-Lab preparation

1. If you don't have any, create a free account on [GitHub](https://github.com/login).

2. For future synchronization of local folders with GitHub, download and install [git](https://git-scm.com/). Git is free, open source, and available on Windows, Mac, and Linux platforms. Window users may also need to use the Git Bash application (installed automatically with git) for command line operations.

<a name="part1"></a>

## Part 1: GitHub

GitHub is a code hosting platform for collaboration and version control. GitHub lets you and others work together on projects, keep all previous modifications, create different branches, and much more.

1. In GitHub, create a new public repository titled **esp-micropython**. Initialize a README, Python template .gitignore, and [MIT license](https://choosealicense.com/licenses/mit/).

2. Use any available git manuals, such as [Markdown Guide, Basic Syntax](https://www.markdownguide.org/basic-syntax/) and add the following sections to your README file.

   * Headers H1, H2, H3
   * Emphasis (*italics*, **bold**)
   * Lists (ordered, unordered)
   * Links
   * Table
   * Listing of Python source code (with syntax highlighting)

3. Use your favorite file manager and run the Git Bash (Windows) or Terminal (Linux) application inside your home folder `Documents`.

4. With help of `git` command, clone a local copy of your public repository.

   > **Important:** To avoid future problems, never use national characters (such as éščřèêö, ...) and spaces in folder- and file-names.
   >
   > **Help:** Useful git command is `git clone` - Create a local copy of remote repository. This command is executed just once; later synchronization between remote and local repositories is performed differently.
   >
   > Useful bash commands are `cd` - Change working directory. `mkdir` - Create directory. `ls` - List information about files in the current directory. `ls -a` - List information aout all files in the current directory. `pwd` - Print the name of the current working directory.

   ```bash
   ## Windows Git Bash or Linux:
   git clone https://github.com/your-github-account/esp-micropython
   cd esp-micropython/
   ls -a
   ## You should see these three files
   .gitignore  LICENSE  README.md
   ```

5. Set username and email for your repository (values will be associated with your later commits):

   ```shell
   git config user.name "your-git-user-name"
   git config user.email "your-email@address.com"
   ```

   You can verify that the changes were made correctly by:

   ```shell
   git config --list
   ```

<a name="part2"></a>

## Part 2: Basic operations in Python

1. Use micro USB cable and connect the ESP32 board to your computer. Run Thonny IDE and check if selected interpreter is Micropython (ESP32). If not, go to menu **Run > Select interpreter... > Interpreter** and select `ESP32` or `ESP8266`. Click on red **Stop/Restart** button or press the on-board reset button if necesary.

2. In the **Shell** window, try the following arithmetic, binary, and string operations:

    ```python
    ```

<a name="part3"></a>

## Part 3: Functions in Python

1. In Thonny IDE, create a new source file in menu **File > New Ctrl+N**, copy/paste the [...]() code and run the application by **Run > Run current script F5**. Save the code as `xxx.py` to your local folder.







8. When you finish, always synchronize the contents of your working folder with the local and remote versions of your repository. This way you are sure that you will not lose any of your changes. To do that, use **Source Control (Ctrl+Shift+G)** in Visual Studio Code or git commands to add, commit, and push all local changes to your remote repository. Check GitHub web page for changes.

   > **Help:** Useful git commands are `git status` - Get state of working directory and staging area. `git add` - Add new and modified files to the staging area. `git commit` - Record changes to the local repository. `git push` - Push changes to remote repository. `git pull` - Update local repository and working folder. Note that, a brief description of useful git commands can be found [here](https://github.com/tomas-fryza/esp-micropython/wiki/Useful-Git-commands) and detailed description of all commands is [here](https://github.com/joshnh/Git-Commands).
   >
   > ```bash
   > ## Windows Git Bash or Linux:
   > $ git status
   > $ git add -A
   > $ git status
   > $ git commit -m "Creating functions in Python"
   > $ git status
   > $ git push
   > $ git status
   > ```

   ![git](images/git_basics.png)

<a name="experiments"></a>

## (Optional) Experiments on your own

1. TBD

<a name="references"></a>

## References

1. [Markdown Guide, Basic Syntax](https://www.markdownguide.org/basic-syntax/)
