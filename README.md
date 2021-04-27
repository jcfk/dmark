## The theory of `d(ata)mark(down)`

In the world of plaintext, you have to choose between "livable" human-friendly documents in .md and .txt (for your minimalist todo lists and such) and entirely "computer writable" data files (.json, .xml). But what if you want to combine prose with programmatically read/writeable data in one file?

`dmark` is first and foremost a language which adds the json syntax to human-friendly prose documents to make documents that are both livable and programmatically read/writeable. The point is to bridge the gap between these two styles of plaintext.

`dmark.py` contains a `Dmark` class which can be used to parse and modify `dmark` files.

The `.dm` extension is hereby seized for `dmark` files!

## `dmark` language

See the [JSON spec](https://www.json.org/json-en.html).

The `dmark` language is identical in function to JSON. Roughly, in the terminology of the JSON spec, a value can be an "object" (dict), "array" (list), string, or number. An object maps strings to values, and an array contains values. The syntax for a `dmark` value is determined by both the type of the value and the type of the value containing it. Parent-child relationships are shown with indentation.

Strings and numbers inside an object:
```
@key1: stringstringstring
@key2: 420133769
```

One can access the values like this: `object["key1"]`.

Strings and numbers inside an array:
```
@ iamtheverymodelofamodernmajorgeneral
@ 3.1415
```

One can access the values like this: `array[0]`.

An object inside an object:
```
@key1
	@key2: singsingsing
	@key3: -111
```

One can access the values like this: `object["key1"]["key2"]`.

An object inside an array:
```
@
	@key1: iveinformationvegetableanimalandmineral
	@key2: 0
```

One can access the values like this: `array[0]["key1"]`.

Using the `Dmark` class in `dmark.py`, the document object is the `value` attribute. See below for examples.

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
dm.write()
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

