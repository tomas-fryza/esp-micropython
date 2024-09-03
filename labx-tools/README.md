# Lab 1: Tools for programming and debugging ESP32 microcontrollers

* [Pre-Lab preparation](#preparation)
* [Part 1: Wokwi simulator](#part1)
* [Part 2: Thonny IDE](#part2)
* [Part 3: Wi-Fi scanner](#part3)
* [(Optional) Experiments on your own](#experiments)
* [References](#references)

### Components list

* ESP32 board, USB cable

### Learning objectives

After completing this lab you will be able to:

* Understand what MicroPython is and how it differs from traditional Python
* Use the tools and software for MicroPython development
* Use the MicroPython REPL to interact with the microcontroller in real-time
* Execute basic Python commands on the microcontroller
* Control GPIO pin to turn on/off LED

The purpose of this laboratory exercise is to provide a foundational understanding of MicroPython and hands-on experience with microcontroller programming.

<a name="preparation"></a>

## Pre-Lab preparation

1. If you don't have any, create a free account on [GitHub](https://github.com/login).

2. For future synchronization of local folders with GitHub, download and install [git](https://git-scm.com/). Git is free, open source, and available on Windows, Mac, and Linux platforms. Window users may also need to use the Git Bash application (installed automatically with git) for command line operations.



1. (Optional) If you have option to use ESP32 board and logic analyzer, download and install [Saleae Logic 1](https://support.saleae.com/logic-software/legacy-software/older-software-releases#logic-1-x-download-links).

<a name="part1"></a>

## Part 1: GitHub

GitHub serves as a platform for hosting code, facilitating collaboration, and managing version control. It enables you and your collaborators to work together on projects, retain a history of all prior changes, create distinct branches, and offers a multitude of additional features.

1. In GitHub, create a new public repository titled **esp-micropython**. Initialize a README, Python template `.gitignore`, and [MIT license](https://choosealicense.com/licenses/mit/).

2. Use any available Git manuals, such as [Markdown Guide, Basic Syntax](https://www.markdownguide.org/basic-syntax/) and add the following sections to your README file.

   * Headers H1, H2, H3
   * Emphasis (*italics*, **bold**)
   * Lists (ordered, unordered)
   * Links
   * Table
   * Listing of Python source code (with syntax highlighting)

3. Use your favorite file manager and run the Git Bash (Windows) or Terminal (Linux) application inside your home folder `Documents`.

4. With help of Git command, clone a local copy of your public repository.

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

6. (Optional) Using branches in Git is a fundamental concept that allows you to work on different features or aspects of a project simultaneously without affecting the main codebase. Using branches in Git allows for efficient code management, parallel development, and collaboration in a team setting. It helps prevent conflicts between different features or bug fixes being worked on simultaneously. Here is the basic way to use branches in Git.

   a. **Create a New Branch:** To create a new branch, use the following command:

      ```bash
      git branch branch_name
      ```

   Replace `branch_name` with the name you want to give to your new branch. This command creates a new branch but doesn't switch to it yet.

   b. **Switch to a Branch:** To switch to a branch, use the following command:

      ```bash
      git checkout branch_name
      ```

   Replace `branch_name` with the name of the branch you want to switch to. After executing this command, you're working in the context of the chosen branch.

   Alternatively, you can use a single command to create and switch to a new branch:

      ```bash
      git checkout -b new_branch_name
      ```

   c. **Make Changes:** Now that you're on the new branch, you can make changes to your project. These changes are isolated to this branch and won't affect the main or other branches.

   d. **Commit Changes:** After making changes, commit them to your branch using the following commands:

      ```bash
      git add .
      git commit -m "Descriptive commit message"
      ```

      The `git add .` command stages your changes, and `git commit` records them with a meaningful commit message.

   e. **Push Branch (Optional):** If you want to share your branch and collaborate with others, you can push it to a remote repository:

      ```bash
      git push origin branch_name
      ```

   f. **Merge or Rebase (Optional):** Once your changes on the branch are complete, you can merge the branch back into the main branch or another target branch using commands like `git merge` or `git rebase`.

   g. **Delete Branch (Optional):** After the branch's changes have been merged or are no longer needed, you can delete it:

      ```bash
      git branch -d branch_name
      ```

      The `-d` flag stands for "delete." If the branch contains unmerged changes, you may need to use `-D` instead: `git branch -D branch_name`.



## Part 1: Wokwi simulator

Wokwi is a web-based platform for simulating and visualizing electronics projects right in your web browser. You can use it to simulate Arduino, ESP32, STM32, and many other popular boards, parts and sensors in C, MicroPython or Rust language.

1. Open your web browser, visit the [Wokwi](https://wokwi.com/micropython) website, and select **ESP32 Blink** starter template. Wokwi provides a work area with the circuit on the right where you can add and connect components like LEDs, sensors, or other peripherals and a code editor on the left. Here, you can write MicroPython code that will run on the virtual ESP32 microcontroller.

   ![wokwi_blink](images/wokwi_blink.png)

2. The Blink template consists of ESP32 microcontroller, LED, and resistor. Simulate the circuit by clicking on a **Star the simulation** button. This will start the simulation, and you will see how your code interacts with the virtual components.

3. Go through each line of the source code and clarify its function. Change the duration of the `sleep()`` function and observe the changes during simulation.

4. Incorporate an additional LED and resistor into the circuit, designate an available GPIO pin, establish the LED connection using an active-low configuration, and develop the code to achieve alternating blinking of two LEDs.

<a name="part2"></a>

## Part 2: Thonny IDE

Thonny is an integrated development environment (IDE) designed primarily for Python programming. It provides a user-friendly and beginner-friendly environment for writing, running, and debugging Python code. It can also be used with MicroPython for programming microcontrollers like the ESP8266 and ESP32. Thonny is available for multiple platforms, including Windows, macOS, and Linux.

> **IMPORTANT:** Before continue, your ESP32/ESP8266 board needs to be flashed with MicroPython firmware (see the [installation](../../README.md)).

1. Use micro USB cable and connect the ESP32 board to your computer. Run Thonny IDE and go to menu **Run > Select interpreter... > Interpreter** and select `ESP32` or `ESP8266`. Click on red **Stop/Restart** button or press the on-board reset button if necesary.

2. In MicroPython programming, REPL stands for `Read-Eval-Print Loop`. It is an interactive mode that allows you to enter and execute Python code commands directly, one at a time, without the need to write and upload entire scripts or programs. Use the following commands in **Shell**.

    ```python
    # Print string to a Shell
    >>> print("Hi there!")
    Hi there!

    >>> a = 10
    >>> b = 3
    >>> print(f"add: {a+b}, sub: {a-b}, div: {a/3}, div_int: {a//3}")
    >>> print(f"rem: {a%b}, mul: {a*b}, exp: {a**b}")

    # Convert numbers
    >>> x = 65
    >>> bin(x)  # to binary representation
    '0b1000001'
    >>> hex(x)  # to hexadecimal
    '0x41'
    >>> chr(x)  # to unicode string
    'A'
    >>> ord("a")  # to unicode code
    97
    ```

    See MicroPython tutorials, such as [MicroPython Programming Basics with ESP32 and ESP8266](https://randomnerdtutorials.com/micropython-programming-basics-esp32-esp8266/) for detailed explanation.

    Test some other useful commands from [Quick reference for the ESP32](https://docs.micropython.org/en/latest/esp32/quickref.html):

    ```python
    # A platform identifier
    >>> import sys
    >>> sys.platform
    'esp32'

    # Get the current frequency of the CPU and RTC time
    >>> import machine
    >>> help(machine)
    >>> machine.freq()
    >>> machine.RTC().datetime()

    # Get Flash size in Bytes
    >>> import esp
    >>> esp.flash_size()

    # Read the internal temperature (in Fahrenheit)
    >>> import esp32
    >>> esp32.raw_temperature()
    # FYI: temp_c = (temp_f-32) * (5/9)
    #      temp_f = temp_c * (9/5) + 32
    ```

    Write code to read the ESP core temperature and print it in both Fahrenheit and Celsius.

3. In Thonny IDE, create a new source file in menu **File > New Ctrl+N**, copy/paste the [example blink](https://raw.githubusercontent.com/tomas-fryza/esp-micropython/main/examples/01-blink/main.py) code and run the application by **Run > Run current script F5**. Save the code as `01-blink.py` to your local folder.

   ![thonny_blink](images/thonny_blink.png)

   > **IMPORTANT:** When a program is running at an interactive console, pressing `Ctrl+C` will raise a `KeyboardInterrupt` exception on the main thread to stop the script. If it does not respond, press the onboard `reset` button.
   >
   > Interrupting a running MicroPython code on an ESP32 microcontroller can be done in several ways. Here are two common methods:
   >
   >   * **Keyboard Interrupt `Ctrl+C`:**
   >      If you are running code interactively on a MicroPython REPL (Read-Eval-Print Loop), you can stop the execution by sending a keyboard interrupt `Ctrl+C`. This works when you are connected to the ESP32's REPL via a terminal or a serial console. When you press `Ctrl+C`, it will raise a `KeyboardInterrupt` exception on the main thread to stop the code execution and return you to the REPL prompt.
    >
    >   * **Hardware Reset:**
    >      In case the code is running as a standalone script (i.e., not interactively on the REPL), and you cannot stop it through `Ctrl+C`, you can perform a hardware reset. This can be done by pressing the reset button on your ESP32 board, or by momentarily disconnecting and reconnecting the power source.

<a name="part3"></a>

## Part 3: Wi-Fi scanner

Because ESP32 microcontroller consists of Wi-Fi module, you can use MicroPython's `network` module to perform a simple Wi-Fi scan.

1. In Thonny IDE, create a new source file in menu **File > New Ctrl+N**, copy/paste the [example](https://raw.githubusercontent.com/tomas-fryza/esp-micropython/main/examples/03-wifi-scan/main.py) code and run the application. Save the code as `01-wifi-scan.py` to your local folder.

    ```python
    import network

    # Initialize the Wi-Fi interface in Station mode and activate it
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    # Perform the Wi-Fi scan
    nets = wifi.scan()

    # Print the list of available Wi-Fi networks
    for net in nets:
        print("Signal Strength (dBm):", net[3])
        print("SSID:", net[0].decode("utf-8"))
        print("")
    ```

    This code initializes the WLAN interface in Station mode, performs a Wi-Fi scan, and then prints the SSID and signal strength (in dBm) of each available network.

2. Start a new access point on your smartphone and repeat the application. Try several distances between the phone and ESP32 board and observe the RSSI parameter.



3. After completing your work, ensure that you synchronize the contents of your working folder with both the local and remote repository versions. This practice guarantees that none of your changes are lost. You can achieve this by using Git commands to add, commit, and push all local changes to your remote repository. Check GitHub web page for changes.

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

1. Modify the Wokwi example and build an application that will repeatedly trasnmit the string `PARIS` on a LED in the Morse code. Choose the duration of "dot" and "dash" so that they are visible during the simulation and/or implementation. Note that the proper Morse code timing is explained [here](https://morsecode.world/international/timing.html).

2. If you have your own ESP32/ESP8266 board, follow the [instructions](https://github.com/tomas-fryza/esp-micropython/wiki/How-to-use-MicroPython-and-ESP32-ESP8266) and install the MicroPython interpreter on it.

<a name="references"></a>

## References

1. [Getting started with MicroPython on the ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

2. MicroPython Documentation. [Quick reference for the ESP32](https://docs.micropython.org/en/latest/esp32/quickref.html)

3. Stephen C. Phillips. [Morse Code Timing](https://morsecode.world/international/timing.html)
