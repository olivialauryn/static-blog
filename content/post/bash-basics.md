---
author: osnowden
comments: true
date: 2020-10-03 17:50:51+00:00
layout: post
link: http://oliviasnowden.me/2020/10/03/bash-basics/
slug: bash-basics
title: BASH BASICS
tags: [bash, linux]
---




Bash, or the Bourne-Again SHell, is named after the creator of the Unix shell Stephen Bourn. Bash is a command language interpreter that can execute commands and process text files as input. Shell scripts are, basically, files containing a series of commands. You can schedule Bash scripts to run at certain times to automate tasks for you. 







If you are using a Linux machine, you can write and execute Bash scripts in terminal. Through the terminal you can use your preferred text editor (nano, vim, etc.) to write your script and save it with the extension .sh. If you are using a MacBook, like me, you can use the terminal or Visual Studio Code to write Bash scripts- just save them with the .bash extension.   







I love Linux, and I love Bash scripting, but it can be hard to learn. Here are some basics. 







#### Set-up, Execution, and Redirection 







The Bash shell scripting language allows for loops, selection statements, input/output, and functions like other programming languages.  Each shell script starts with a comment that states which interpreter to use to run the script. For Bash, begin each file with the shebang: `#!/bin/bash`. 







To execute a Bash script, you must first change the permissions of the file using `chmod 755 _script_name_`. Then, you can execute a script by running `./script_name` on the command line or by hitting the play button in Visual Studio Code. 







Sometimes it can be useful to redirect Bash input/output. `script_name> filename` will redirect output to a file, `script_name >> filename` will append the output of the bash script to an existing file, and `script_name< filename` redirects a file as input to a script. 







#### Variables and Math







The body of a Bash script can consist of variables, commands, and arithmetic operations. Variables are a basic building block of Bash scripts. `VARIABLE=VALUE` is the basic assignment statement, notice there are no spaces. To call a variable in a Bash script, use` $VARIABLE`. The "print statement" for Bash scripting is echo. If you want to output something to the user use `echo "statement"/$VARIABLE`.







If you want to assign an interpreted value with spaces to a variable, you must include double quotes around the value. If you want to interpret the value with spaces literally, use single quotes. Below is an example of a Bash script and its output that shows the difference between single and double quotes.







![](/bash-1.png)







![](/bash-2.png)













Bash interprets everything as strings, meaning that if you want to do math-you need to explicitly tell Bash. To do that, include an arithmetic operation in `$(()) `or place `let` before it. Bash can't perform arithmetic on decimals or fractions. Below is a list of arithmetic operators bash can process: 







![](/bash-3.png)







#### Read and Parameters 







Getting input from users in Bash is a little different. Anywhere that you want to insert a user's input into a Bash script place $1, $2, $3, etc. Input is accepted as parameters, and the parameters are placed in those spots in the order they are given. If the number of parameters given exceeds the number of spots for them in the script, the extra parameters are ignored. 







If you want to provide the user a prompt, and assign their parameters names, you can use the read statement in your script: `read -p "message" var1 var 2 ...`







Sometimes, you want to use metadata about parameters in your script. Bellow is a list of helpful symbols that you can use in your scripts: 







  * $parameter: calls a parameter
  * shift: rotates all parameters down one position, used in loops
  * $0: returns the name of the script
  * $$: returns the PID of the script
  * $#: returns the number of parameters the user supplied
  * $@: returns a list of all parameters






Example script:







![](/bash-4.png)







![](/bash-5.png)



