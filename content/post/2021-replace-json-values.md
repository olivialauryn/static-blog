---
author: ["Olivia Snowden"]
title: "Automate Replacing JSON Values with Python"
date: "2021-12-22"
tags: ["Python","Automation"]
ShowToc: true
TocOpen: true
---
![](/json-logo2.jpeg)
**In this post:**

1. **Intro** 

2. **JSON File**

3. **CSV File**

4. **Python Script**

5. **Writing the Python Script**

I was recently tasked with automating the replacement of key:value pairs in a JSON file. The goal was to take the output of a CLI command listing key:value pairs and place those keys/values in specific places within a JSON file. I decided to convert the output of the CLI command to a CSV file and have a python script use that CSV to create a new JSON file with updated keys/values. 

There are a wide variety of python modules that can be used to search and replace values in a file-however the JSON file I was working with presented some challenges. In this post I'll go into detail about the format of that file, the CSV, and how to write a python script to search/update values in JSON. 

#### JSON File

To keep things simple, I have replaced the actual JSON file I used with a fake one. However the format of the file and the location of the values to be replaced are the same. Ideally the python script could automate the replacement of any number of values, but we will only be working with 2 sets of key:value pairs. This project results in 2 JSON files-the original JSON file and a new one with updated values. 
In my project there were 6 values spread across 3 blocks that needed to be replaced. First 2 old keys together in one block, `old-key1` and `old-key2` needed to be updated. 
![](/original-key-block.png)
Further down, both key:value pairs `old-key1:old-value1` and `old-key2:old-value2` needed to be updated in their own blocks- and it was very important that the keys were matched with their corresponding values. 
![](/original-values-block.png)
I discovered that the nested format of the JSON file made it difficult to search for values in the file using python. Additionally-some values were of the type *list* and some were type *dictionaries*. To find the work around for this, see the "Writing the Python Script" section. 

#### CSV File  
The new values to be placed in the json file came from a CSV file I generated from CLI output. However, the CSV can contain just about anything and use any delimiter.  In this case, I used two sets of comma separated values and column headers: 
![](/csv.png)

#### Python Script
![](/entire-script.png)
**Lines 4-12: Setup**

In the first portion of the python script, I import the necessary modules (csv and json) and initialize 2 lists and a total of 6 variables. One list will contain the keys from the CSV, the other will contain the values. This is so the content of the CSV can be easily processed in the script. The variable `y` is set to 1, while the rest are 0-this comes into play later in the script and ensures that the iterations work correctly. 

**Lines 14-19: Accept input from CSV and add values to lists** 

Once everything is setup, the CSV file must be opened and the keys/values be placed into their respective lists. First, line 14 opens the CSV file "input.csv" as the variable `myfile` with read `r` permission. Then the csv module is used to read the file and specify that the delimiter used is a comma ",".  Line 16 specifies to skip the first line in the CSV file since mine contains column headers. Finally, lines 17-29 iterate through the rows in the CSV and add the keys to the `keys_list` and the values to the `values_list`.  This is done by specifying that the keys are in the 0 index of each row, `row[0]`, while the values are in the 1 index `row[1]`. 

**Lines 22-34: Open original JSON file and update keys in file** 

Line 22 opens the JSON file in the same way the CSV was opened, but here the JSON module is used to load the content as `read_content`. Next, 3 separate for loops are used to replace the keys in the JSON file. The first for loop replaces the keys that are together in a nested block in the JSON file, without being paired with their values. This is the only for loop that uses 2 variables to iterate. `a` iterates through `key_list` and since `a` is set to equal 0 the iteration begins at the first key in the `key_list`. `y`, which is set to equal 1, iterates through the original values in the JSON file that are being replaced in this for loop. The original JSON file has 2 values that need to be replaced using this for loop: `old-key1` and `old-key2`. This is specified in line 25 as `"old-key"+str(y)`. So as `y` is increased by 1 in the for loop the old key is replaced with the corresponding new key. 
![](/first-for-loop.png)
The second and third for loops replace the other keys in the script when they are separated with their respective values. This means that the exact location of the value to be replaced is specified, instead of using an if statement like the first loop. 
![](/second-and-third-for-loop.png)

**Lines 37-41: Update values in file** 

The values are replaced in the JSON file similarly to how the keys were replaced using for loops. Here 2 loops are used, each replacing one value in the JSON file which correspond to the second and third loops that replace keys. Once this portion of the script is ran, the key:value pairs that are grouped together in the JSON file are replaced with new key:value pairs.
![](/value-for-loops.png)

**Lines 44-45: Write to new JSON file**

Finally, a new JSON file "new-file.json" is opened as `access_json` with write `w` permission. Then the json module combines the content of the old JSON file `read_content` with the updated content `access_json`. This creates a new JSON file with the updated values while the original JSON file is untouched. 

![](/new-keys.png)
![](/new-keys-and-values.png)


#### Writing the Python Script
Creating the python script involved lots of trial and error since, as mentioned previously, the nesting in the JSON file caused the usual methods I use to find/replace values using python to fail. My first thought was to iterate through the JSON file and use an if statement to say `if oldvalue: oldvalue=newvalue`, `newvalue` being one of the keys/values from the CSV. However, with that method it seemed that python was only going through the outermost layer of the JSON file. While I'm sure there is a "better" way of doing this-I ended up keeping the `if x: x=y` to replace the values in the JSON file, but specified the exact location inside the file to find "x".

This is where the trial and error comes in. For each value that needs to be replaced, I used print statements to narrow down the location of where I was inside the file. The format I used was `read_content` followed by the names of each nested layer in brackets `[]`. This is similar to using indexes to find values in a list. Some layers of the JSON file contained multiple layers of the same name which meant that using `["name of layer"]` wouldn't work. To figure out how to get where I needed, I checked the type of where I was using `print(type(read_content['layer1']['layer2']etc))`. 

I discovered that layers with multiple layers within them are lists-which meant that I could use the index of the layer I wanted to go into as part of the path I was specifying. For example, `read_content ['json']['group2']['resources'][0]` to enter one layer and `read_content ['json']['group2']['resources'][1]` to enter another layer both under json > group2 > resources. 
![](/nesting-script.png) ![](/nesting-terminal.png)

**NOTE**: If you use Visual Studio Code to open the JSON file, you can see the path to a value at the top of the screen if you click on a value. You can use this path separated by brackets instead of using print statements to find the path.
![](/vsc-path.png)