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
f-string Mode:
	m0:	the whole match, match.group(0)
	m#:	m1,m2,etc, each regex group in turn, match.group(#)
	name:	matches against (?<name>...) in the regex
	m:	the match object itself, including all its attributes
```
## Examples
```
multimv -n re -g  '\.(?![^.]+$)'  ' ' \
	'dumb.movie.[1080p].[5.1].[etc].mkv'

- 'dumb.movie.[1080p].[5.1].[etc].mkv'
+ 'dumb movie [1080p] [5 1] [etc].mkv'


multimv -n re -g  ' *\[.*?\]'  '' \
	'dumb movie [1080p] [5 1] [etc].mkv'

- 'dumb movie [1080p] [5 1] [etc].mkv'
+ 'dumb movie.mkv'


multimv -n re --fstring '\d+' '{int(m0)+1:0>{len(m0)}}' \
	page000 page001 page002 index

~ index
- page002
+ page003
- page001
+ page002
- page000
+ page001
```
