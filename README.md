## The `d(ata)mark(down)` Thesis

In the world of plaintext, you're made to choose between static "human writable" prose-style documents (.md, .txt) and explicitly "computer writable" data files (.json, .xml). To combine prose with modifiable data, you're forced to rely on editor macros, which are limiting.

No more! `dmark` is a markdown derivative and parser solving this problem. It exists to

1. provide an arbitrarily structured and modifiable data standard within markdown, and
2. provide a visual demarcation between data and prose.

## Quick start

The data in the following file `dmark.dm` is deserialized into a  with

```
import dmark

doc = dmark.read("dmark.dm");
```


```
// dmark.dm
### A prose header

- A
- prose
- list

This is prose. Prose is not read by dmark.

@not-prose: I am data! You can access me with `doc[0]` or `doc[not-prose]`.

@: 123567890

Anonymous data is accessed by index: `doc[1]` is `"1234567890"`.

@i-am-a-wrapper[

	@inside-wrapper: hi!

	@[
		@: indent
	@: to any
@: level
	]

	Wrapper elements create lists, essentially: `doc[i-am-a-wrapper][0]` is `"hi!"`, and `doc[i-am-a-wrapper][1][0]` likewise is `"indent"`.

]

Again, prose is ignored.

@paragraph: {I am a paragraph in data.
I can span multiple lines.}

`doc[paragraph]` is `"I am a paragraphi in data.\n I can span multiple lines."`
```


