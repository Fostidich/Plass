# Plass
Keep track of your lessons (or whatever else) by storing dates. 

## Usage
This is a terminal line app, here are some examples.
- Use <code>plass get</code> to see the full list
- Use <code>plass step \[lecture]</code> to update the list
- Use <code>plass help</code> or <code>plass example</code> to show all commands

---

### Notes

1. When a command requires to insert a course, this has to be specified via its code (case-sensitive).
For example, you have to use <code>plass get TdS</code> instead of <code>plass get Teoria_dei_sistemi</code>.
2. Dates have to be specified with format "dd-mm". For example: "12-10", "09-12", "8-7" will be accepted;
"12/12", "09 11", "6 sep" will be rejected (<code>plass add CG 10-10</code>).
3. The full name of a course must not be created using white spaces. Instead, underscores are requires
(but they will be displayed as white spaces). For example, instead of "Chimica generale" you have to use "Chimica_generale"
(<code>plass create CG Chimica_generale</code>).
4. For the import command (<code>plass import CG < your/import/file.txt</code>), the .txt file must have a single date for each line.
For example, [here](#File) is a correct-written file.
5. In case of corruption, you can delete the full plass-data folder so that a fresh new one
will be generated (e-mail me the folder, maybe I can recover it if you need).


###### File
```text
13-09
14-09
29-09
18-10
02-11
02-12
```
