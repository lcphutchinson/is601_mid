## SU25 IS601-850 Midterm: Advanced REPL Calculator
![Coverage Badge](https://github.com/lcphutchinson/is601_mid/actions/workflows/ci.yml/badge.svg)

Developed for Web Systems Development, by Keith Williams

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

### 🚀 Operation

Launch the calculator with Python:

```bash
python3 main.py
```

Module 3's Calculator supports six arithmetic operations

```bash
add: Adds two operands, x and y.
subtract: Subtracts an operand y from another operand x.
multiply: Multiplies two operands, x and y.
divide: Divides a non-zero operand y from another operand x.
power: Raises an operand x to the nth power, where n == operand y
root: Produces the nth root of operand x, where n == operand y
```

New in v.1.5, Arithmetic operations are called without operands and will request operands in a followup dialogue.
 
```bash
>>$: add
Enter operands for command 'add', or 'cancel' to abort:
>> operandx: 8
>> operandy: 6
Result: 14
>>$:
```

All arithmetic commands can be cancelled during their operand input promps

```bash
>>$: subtract
Enter operands for command 'subtract', or 'cancel' to abort:
>> operandx: cancel
subtract cancelled
>>$:
```

If a command is not parsable or otherwise invalid, an error message will be shown, but the program will not terminate:

```bash
>>$: nonsense
Unknown command: 'nonsense'. Type 'help' for available commands.
>>$:
```

New in v.1.4: Use the special command 'history' to display a log of operations from this session.
```bash
>>$: history
Calculation History
-------------------
1. Addition(8, 6) = 14
>>$:
```

To display a full command list use the special command 'help'
```bash
>>$: help
Available Commands
------------------
add, subtract, multiply, divide, power, root -- Perform calculations
history - Display your calculation history
clear - Clear your calculation history
undo - Undo your last calculation
redo - Redo the last undone calculation
save - Save calculation history to file
load - Load calculation history from file
exit - Exit the calculator
>>$:
```

New to v.1.5, the 'undo' and 'redo' commands walk backwards and forward through the operation history

```bash
>>$: add
Enter operands for command 'add', or 'cancel' to abort:
>> operandx: 8
>> operandy: 6
Result: 14
>>$: undo
Undo successful
>>$: history
No history to display
>>$: redo
Redo successful
>>$: history
Calculation History
-------------------
1. Addition(8, 6) = 14
>>$:
```

v.1.5's 'save' and 'load' commands record and retrieve your operation history from disk, 
and it's 'clear' command wipes system's history and undo/redo stacks.

```bash
>>$: clear
History cleared
>>$: undo
Nothing to undo
>>$:
```

To exit the program, use the command `exit`. By default, the system will save your current history.

```bash
>>$: exit
History saved successfully.
Thank you for using Python REPL Calculator. Exiting...
```

