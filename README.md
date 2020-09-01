## The `d(ata)mark(down)` Thesis

In the world of plaintext, you're made to choose between static "human writable" prose-style documents (.md, .txt) and explicitly "computer writable" data files (.json, .xml). To combine prose with modifiable data, you're forced to rely on editor macros, which are limiting.

No more! `dmark` is a markdown derivative and parser solving this problem. It exists to

1. provide an arbitrarily structured and modifiable data standard within markdown, and
2. provide a visual demarcation between data and prose.

## Quick start

Example file:

```
// todo.dm

### LONG TERM

- Write romantic poem
- Become CEO of Apple

"Stew or stew not. There is no fry." - Yoda

### MID TERM

- Fix home server
- Update CV


Stats:
@tasks-completed: 278
@tasks-remaining: 4
@average-daily-completions: 6.13333333333333333

@todo-list[
@[
	@date: Tuesday, September 1 2020 

	@incomplete[
		@: task3
		@: task4
		@: {task5 is a paragraph
which spans multiple lines}
	]

	@complete[
		@: task1
		@: task2
	]

	Let's consider this the day's notes!

]
]

```

Parsing:
```
import dmark

doc = dmark.open("todo.dm");

# doc["tasks-completed"]                 == "278"
# doc[0]                                 == "278"

# doc["todo-list"][0]["date"]            == "Tuesday, September 1 2020"
# doc["todo-list"][0]["incomplete"][0]   == "task3"

```

Editing:
```
doc["tasks-completed"] = 279

doc.write();
doc.close();

# OR

doc.close();

```

Out:
```
...
Stats:
@tasks-completed: 278
...

```

Add and Remove 1:
```
doc.append(0, "new-statistic"

doc["todo-list"][0]["incomplete"].remove("task3")
doc["todo-list"][0]["complete"].append("task3")

```

Out:
```
...
	@incomplete[
		@: task4
		@: {task5 is a paragraph
which spans multiple lines}
	]

	@complete[
		@: task1
		@: task2
		@: task3
	]
...

```

Add and Remove 2:
```
doc["todo-list"].insert(0, "", "", Type.WRAP)

doc["todo-list"][0].append("Wednesday, September 2 2020", "date")

doc["todo-list"][0].append("", "incomplete", Type.WRAP)
doc["todo-list"][0]["incomplete"].append("task0")

doc["todo-list"][0].append("", "complete", Type.WRAP)


```

Out:
```
...

@todo-list[
@[
	@date: Wednesday, September 2 2020

	@incomplete[
		@: task0

	]

	@complete[]

]

@[
	@date: Tuesday, September 1 2020 
...

```




