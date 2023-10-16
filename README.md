# Plass
Are you always some lecture behind? Now you can automatically get these planned out for you. Try it, it's simple!

## Features
- Keep track of the missed lectures
  - Use <code>plass get</code> to see the full list
  - Use <code>plass complete \[lecture]</code> to update the list
- Automatically set the week day for the lecture (or specific days otherwise) so the planner gets automatically updated

## Usage
Type <code>plass help</code> to see available actions.

## Examples

<code>plass get</code><br>
> <span style="color:white">You are currently 3 lectures behind.<br><br>
> <span style="color:orange">[2 -> 04-10] CG  Chimica Generale</span><br>
> <span style="color:orange">[1 -> 11-10] AM2 Analisi Matematica 2</span><br>
> <span style="color:white">[0 -> 15-10] FAI Fundaments of Artificial Intelligence</span><br>
---

<code>plass complete AM2</code><br>
> <span style="color:lime">AM2 lecture of 11-10 completed<br><br> 
> <span style="color:orange">[2 -> 04-10] CG  Chimica Generale</span><br>
> <span style="color:white">[0 -> 18-10] AM2 Analisi Matematica 2</span><br>
> <span style="color:white">[0 -> 15-10] FAI Fundaments of Artificial Intelligence</span><br>
---

<code>plass add AM2 16-10</code><br>
> AM2 lecture of 16-10 added<br><br> 
> <span style="color:orange">[2 -> 04-10] CG  Chimica Generale</span><br>
> <span style="color:orange">[0 -> 16-10] AM2 Analisi Matematica 2</span><br>
> <span style="color:white">[0 -> 25-10] FAI Fundaments of Artificial Intelligence</span><br>
---

<code>plass remove AM2 16-10</code><br>
> AM2 lecture of 16-10 removed<br><br> 
> <span style="color:orange">[2 -> 04-10] CG  Chimica Generale</span><br>
> <span style="color:white">[0 -> 18-10] AM2 Analisi Matematica 2</span><br>
> <span style="color:white">[0 -> 15-10] FAI Fundaments of Artificial Intelligence</span><br>
