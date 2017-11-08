# `csvprint`

Command-line utility for pretty printing csv files.

## Example

```
» csvprint imdb.csv
Title                  Release Year Estimated Budget
Shawshank Redemption   1994         $25 000 000
The Godfather          1972         $6 000 000
The Godfather: Part II 1974         $13 000 000
The Dark Knight        2008         $185 000 000
12 Angry Men           1957         $350 000
```

Compare to e.g.

```
» column -t -s ',' imdb.csv
Title                   Release Year  Estimated Budget
Shawshank Redemption    1994          $25 000 000
The Godfather           1972          $6 000 000
The Godfather: Part II  1974          $13 000 000
The Dark Knight         2008          $185 000 000
12 Angry Men            1957          $350 000
```
Creating an alias for `column -t -s ','` could work, but I found it a bit lacking, as it doesn't provide support for various justification or decoration.

## Installation

Clone the repo and add an alias for `python /path/to/csvprint/csvprint.py` to your shell config, e.g.

```
git clone https://github.com/vegarsti/csvprint.git ~/path/to/csvprint
echo "alias csvprint='python3 /path/to/csvprint/csvprint.py'" >> ~/.bash_profile
```

## Features
`csvprint -h` prints a help message. By default, all columns except the left-most are right-justfied.

* `-s` to specify delimiter (default is comma)
* `-n` to specify number of rows to show (default is 1000) (like with `head`, so e.g. `csvprint file.csv -n 10` is like `head -n 10`)
* `--justify` to specify which justification to choose (left or right). Can provide one argument per column or just one argument
* `-d` decorator to separate fields by (e.g. `' '`, which is default)
* `--header` add line above and under the first line
* `--markdown` produces a valid markdown table. If you just want this, though, you should probably use [`csvtomd`](https://github.com/mplewis/csvtomd).

## Justification example

```
» csvprint imdb.csv --justify left right right
OR
» csvprint imdb.csv -j l r r
Title                  Release Year Estimated Budget
Shawshank Redemption           1994      $25 000 000
The Godfather                  1972       $6 000 000
The Godfather: Part II         1974      $13 000 000
The Dark Knight                2008     $185 000 000
12 Angry Men                   1957         $350 000
```

## Markdown example

```
» csvprint imdb.csv --markdown --justify right
                 Title | Release Year | Estimated Budget
-----------------------|--------------|-----------------
  Shawshank Redemption |         1994 |      $25 000 000
         The Godfather |         1972 |       $6 000 000
The Godfather: Part II |         1974 |      $13 000 000
       The Dark Knight |         2008 |     $185 000 000
          12 Angry Men |         1957 |         $350 000
```

When rendered as markdown, this looks like

Title                  | Release Year | Estimated Budget
-----------------------|--------------|-----------------
Shawshank Redemption   |         1994 |      $25 000 000
The Godfather          |         1972 |       $6 000 000
The Godfather: Part II |         1974 |      $13 000 000
The Dark Knight        |         2008 |     $185 000 000
12 Angry Men           |         1957 |         $350 000


## TODO: Planned features
* Add centering justification
* Choice of columns to show (if csv file is "wide")