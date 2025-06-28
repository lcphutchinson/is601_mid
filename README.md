## SU25 IS601-850 Midterm: REPL Calculator w/Design Patterns
![Coverage Badge](https://github.com/lcphutchinson/is601_mid/actions/workflows/ci.yml/badge.svg)

Created for Web Systems Development, a course by Prof. Keith Williams of NJIT

This project builds upon a basic application premise (the arithmetic calculator) to demonstrate various modern programming techniques such as automated testing, logging, and a number of Object-Oriented Design Patterns--specifically the Command, Strategy, Factory, Observer, Memento, and Facade patterns. 

### 📑 Project Description

Python REPL Calculator (v.1.6) is a Python application for the bash shell environment that provides ten basic arithmetic operations over three input modes (Binary, Unary, and Guided), as well as a robust operation history with save, load, undo and redo functionalities. For full details, see 🚀 **Operation** below.

<details>
<summary>
📦 Environment Setup (Verbose)
</summary>

> This setup guide is copied from the original module, [here](github.com/kaw393939/module3_is601)

---

### 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

### 🧩 2. Install and Configure Git

#### Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

#### Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

#### Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
 
(Press Enter at all prompts.)

2. Start the SSH agent: 

 ```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

### 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

### 🛠️ 4. Install Python 3.10+

#### Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---
</details>
<details>
<summary>
🛠️ Requirements & Installation
</summary>


Running this project will require:

- Bash or a similar Unix shell
- A Git installation configured for use with Github (see Verbose)
- Python version 3.13+, optionally with an installed venv module

--- 

### 📦 Quick Setup

- **Retrieve the Project**

```bash
git clone git@github.com:lcphutchinson/is601_3.git
cd is601_3.git
```

- **Generate a Virtual Environment (Optional)**

```bash
python3 -m venv venv
source venv/bin/activate
```

- **Install Project Requirements**

```bash
pip install -r requirements.txt
```
</details>

---

### 🔧 Customization

Python REPL Calculator has a number of configuration settings that can be modified by adding a .env file to the root project folder 'is601_mid'

Below are the example contents of an is601_mid/.env file:
```bash
CALCULATOR_BASE_DIR=. # Default parent directory for /logs and /history
CALCULATOR_LOG_DIR=./logs # Default directory for log files
CALCULATOR_HISTORY_DIR=./history # Default directory for saved history
CALCULATOR_LOG_FILE=./logs/calculator_log.log # Logging filepath
CALCULATOR_HISTORY_FILE=./history/calculator_history.csv # History filepath
CALCULATOR_MAX_HISTORY_SIZE=1000 # Maximum number of saved calculations
CALCULATOR_AUTO_SAVE=True # When True, performs a Save after each calculation
CALCULATOR_PRECISION=10 # Sets the precision of decimal results
CALCULATOR_MAX_INPUT_VALUE=1e999 # Sets the max value for operation inputs
CALCULATOR_DEFAULT_ENCODING=utf-8 # Sets the default encoding
```

---

### 🚀 Operation

Launch the calculator with Python:

```bash
python3 main.py
```

**Arithmetic Operations**
Version 1.6 supports ten arithetic operations:

```bash
Addition ['add', '+']: Adds two Decimal operands
Subtraction ['subtract', '-']: Performs a subtraction using two operands
Multiplication ['multiply', '*']: Multiplies two Decimal operands
Division ['divide', '/']: Performs a division using two operands
Power ['^']: Performs an exponentiation using two operands
Root []: Performs a root operation using two operands
Modulus ['mod', 'modulo', '%']: Performs a modulo division using two operands
IntegerDivision ['int_divide', '//']: Performs an integer division using two operands
Percentage []: Constructs a percentage using two operands
Distance ['abs_diff']: Calculates the distance between two operands
```

Values in the bracketed tags on each operation name can be used as aliases or operand values to call the operation in question. For example, the commands 'add' and 'Addition' are both sufficient to launch an Addition operation.

---

Arithmetic Operations in version 1.6 can make use of three input modes:

**Binary Inputs**
Using an operation's operator (+. -. *, etc.,) you may launch an operation by entering it as you would in a traditional calculator:

```bash
>>[0]$: 5 + 5
Result: 10
>>[10]$:
```

Note the result of a binary operation is stored in the total field to the left of the cursor.

**Unary Inputs**
When entering only an operator and a single operand, the second operand is inferred to be the running total, as in a traditional calculator:

```bash
>>[10]$: ^ 2
Result: 100
>>[100]$:
```

**Guided Inputs**
When only a command is entered, the REPL Calculator will request each operand individually before performing the operation

```bash
>>[100]$: int_divide
Enter operands for command 'int_divide' or 'cancel' to abort:
>> operandx: 100
>> operandy: 3
Result: 33
>>[33]$:
```

---

**Interface Commands**

Version 1.6 supports eight Interface Commands, which manage the calculator and its history in numerous ways.

```bash
Interface Commands
------------------
Clear: Clears the current operation history
Exit: Saves the current history and exits the Calculator
Help: Displays a list of available commands
History: Displays the current calculator history
Load: Loads a saved calculation history from file
Redo: Redoes the last undone calculation
Save: Saves your calculation history to file
Undo: Undoes the most recent calculation
```

The above text is generated by the Help command, along with the summary text for Arithmetic Operations from the previous section

---

The Clear, History, Undo, Redo, Save, and Load operations manage the calculator's operation history. See the below output:

```bash
>>[0]$: 8 + 6
Result: 14
>>[14]$: 6 * 8
Result: 48
>>[48]$: save
Save Successful
>>[48]$: undo
Undo successful
>>[14]$: history
Calculation History
-------------------
1. Addition(8, 6) = 14

>>[14]$: redo
Redo successful
>>[48]$: history
Calculation History
-------------------
1. Addition(8, 6) = 14
2. Multiplication(6, 8) = 48

>>[48]$: clear
History cleared
>>[0]$: load
Load Successful
>>[48]$: history
Calculation History
-------------------
1. Addition(8, 6) = 14
2. Multiplication(6, 8) = 48

>>[48]$:
```

Note that, as of v.1.6, History items loaded from file are not available for the undo function.

Finally, the exit command saves the current history state and exits the program:

```bash
>>[0]$: exit
History Saved Successfully

Thank you for using Python REPL Calculator. Exiting...
```

