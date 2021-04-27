## The theory of `d(ata)mark(down)`

In the world of plaintext, you have to choose between "livable" human-friendly documents in .md and .txt (for your minimalist todo lists and such) and entirely "computer writable" data files (.json, .xml). But what if you want to combine prose with programmatically read/writeable data in one file?

`dmark` is first and foremost a language which adds the json syntax to human-friendly prose documents to make documents that are both livable and programmatically read/writeable. The point is to bridge the gap between these two styles of plaintext.

`dmark.py` contains a `Dmark` class which can be used to parse and modify `dmark` files.

The `.dm` extension is hereby seized for `dmark` files!


## `dmark.py` examples


Document "todo.dm":
```
### LONG TERM

- Write romantic poem
- Become CEO of Apple

Who would even want to become CEO of Apple?


### MID TERM

- Fix home server
- Update CV

Stats:
@completed: 278
@remaining: 4

@days
	@
		@date: Tuesday, September 1 2020 
		@incomplete
			@: task3
			@: task4
		@complete
			@: task1
			@: task2
```

Reading:
```
from dmark import Dmark

dm = Dmark("todo.dm")

dm.value["completed"]                       == 278
dm.value["days"][0]["date"]                 == "Tuesday, September 1 2020"
dm.value["days"][0]["incomplete"][0]        == "task3"
```

Write 1:
```
today = dm.value["days"][0]
today["complete"].append(today["incomplete"].pop())
dm.value["completed"] += 1
dm.write();
```

Out 1:
```
...
Stats:
@completed: 278
...
@days
	@
		@date: Tuesday, September 1 2020 
		@incomplete
			@: task3
		@complete
			@: task1
			@: task2
			@: task4
...
```

Write 2:
```
dm.value["days"].insert(0, {date: todaystring, incomplete: [], complete: []})
dm.value["days"][0]["incomplete"].extend(dm.value["days"][1]["incomplete"])
dm.value["days"][1]["incomplete"] = []
dm.write()
```

Out 2:
```
...
@days
	@
		@date: Wednesday, September 2 2020 
		@incomplete
			@: task3
			@: task4
		@complete
	@
		@date: Tuesday, September 1 2020 
		@incomplete
		@complete
			@: task1
			@: task2
...
```

