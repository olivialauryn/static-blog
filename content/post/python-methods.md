---
author: osnowden
comments: true
date: 2021-01-18 20:23:20+00:00
layout: post
link: http://oliviasnowden.me/2021/01/18/python-methods-classes/
slug: python-methods-classes
title: PYTHON METHODS & CLASSES
tags: [code]
---




Once you get past your first "Hello World" Python script, it's good to learn how to use Python methods and classes. **Methods** and **functions **are a self-contained block of code that can be reused over and over. There are built-in functions that beginners in Python may already be familiar with, like print() and sum(). A user can also define a function (called a user-defined function) that executes a task they need done in their script multiple times. This is especially useful because it keeps the user from having to write that same chunk of code repeatedly. Variables that exist outside of the function can be passed to the function as **parameters**, but they are not required. The format of defining your own function is below:






    
    <code>def function_name(parameters):
        body_of_code
        return variable_to_be_returned</code>







The **return statement** of a user-defined function basically provides the "output" of that function. Since functions are self-contained, if you want a variable returned from what task the function carried out you need to specify that variable in a return statement. Functions return a value or a group of values, while methods generally do not. 







Python is an object oriented language, meaning that you can model real-world things through programming. An **object** represents an entity in the real world that has a unique state, identity, and behaviors (such as a phone, a button, or a person). **Classes** define objects of the same type. For example, a type of class could be a car. However, each individual car would be an object with their own characteristics (color, fuel type, etc.). 







![](/python-1.jpeg)







To create an object in a class you use **constructors**, which are a type of method. In Python the constructor is _init_(self). This is the format to define a class:






    
    <code>class name_of_class:
        def ___init___(self):
             class_body</code>







Class, objects, and constructors can be difficult to wrap your mind around initially, but they are incredibly useful. To help explain, below is an example  that creates unique Python User accounts for an organization:







The goal is to create an object-oriented class (PythonUsers) for generating new users. This class should have the following attributes: **_first_name, last_name, age, username and current_ password_**.  When defining the class, it should a method that generates a password for the user based on the first and last initials followed by the current time stamp.







First, we define the PythonUsers class, and in the constructor method _init_() we include the variables each user object will need (including the "self" keyword, it is required). Inside the class, we call the constructor method to assign each of those variables to become a class variable. Notice that the password variable is not included here, since a separate method will create the passwords. 






    
    <code>#PythonUsers class
    class PythonUsers:
        def __init__(self, first_name, last_name, age, username):
            self.firstName = first_name
            self.lastName = last_name
            self.age = age
            self.username = username</code>







Once the basic setup of the class is finished, we define a method that generates the password. We import the time module so that we can include the time stamps, and then compile the password using the index of the first letters of the user's first/last names (0) and the time module mentioned previously. Notice that since we are still defining an element of the class, the "self" keyword is used in the password method. 






    
    <code>#Method that generates a password for the user
        def passwordGen(self):
            import time
            ts = time.time()
            password = self.firstName[0] + self.lastName[0] + str(ts)
            self.password = password</code>







Now that we have a class defined to create users, we need a method (**_calcAverageAge_**) that accepts a list of users as a parameter and returns the average of their ages. 






    
    <code>#Method that calculates average age of the students
    def calcAverageAge(sum, n):
        average=sum/((n + 1) - 1)
        return average</code>







Next, we need a method (**validateAge**) that validates the age of a user. For the purposes of this example, assume a user should be at least 15 years old and not more than 45 years old. If a user enters a date of birth that does not meet the above requirement, the method should keep prompting the user until a valid age is entered. 






    
    <code>#Method that validates user's age
    def validateAge(age):
        while age > 45 or age < 15:
            age = int(input("Please enter the age of user " + str(i + 1) + " [15-45]: "))
        return age</code>







Using the class and methods implemented above, we can complete our script. For each user, we should request for the user to provide the **_first_name, last_name, username _**and**_ age_**. Remember we need to validate each users age (using the**_ validateAge _**method). We then print to the screen the list of users including their full name, age and default password. Once the users are created and validated, we can we can compute the average age of users using the **_calcAverage _**method and print that out. 






    
    <code>#Main program that accepts integer from user and creates a Python user
    sum=0
    userList=[]
    n=int(input("Please enter the number of users: "))
    for i in range(n):
        first_name=input("Please enter the name of user " + str(i+1) + ": ")
        last_name=input("Please enter the last name of user " + str(i+1) + ": ")
        username=input("Please enter the username of user " + str(i+1) + ": ")
        age=int(input("Please enter the age of user " + str(i+1) + " [15-45]: "))
    #Validate the user's age using validateAge
        age = validateAge(age)
        sum = age + sum
        object=PythonUser(first_name, last_name, age, username)
        object.passwordGen()
        userList.append(object)
    #Print name, age, and password - outside the loop, separate loop for printing
    for i in range(len(userList)):
        fullname = userList[i].firstName + "," + userList[i].lastName
        age = userList[i].age
        newpassword= userList[i].password
        print(fullname + "\t" + str(age) + "\t" + str(newpassword))
    #Compute average age of user with calcAverage
    avg = calcAverageAge(sum, n)
    print("Average Age of users: " + str(avg))</code>







Here we used methods and classes to generate users, but the same concepts can be applied to a variety of situations where a script can be used to automate a task. Overall, methods/functions and classes are useful aspects of Python that can make writing a script easier-and save you a lot of typing.



