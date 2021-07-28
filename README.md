# multimv
Multi mv via fixed string / regex / bash pattern substitutions
## Usage
```
Usage:
	multimv [OPTIONS] COMMAND [ARGS]...

Options:
	-n, --dry-run	Don't touch the filesystem

Commands:  
	multimv [OPTIONS] re [RE-OPTIONS] PATTERN REPLACEMENT [FILES]...

Re-Options:  
	-g, --global	Replace all matches instead of just the first
	--fstring	Treat the REPLACEMENT as an f-string
```
