#!/usr/bin/env perl -w
# usage: script.pl words text >newfile
use English;

# poor man's argument handler
open(WORDS, shift @ARGV) || die "failed to open words file: $!";
open(REPLACE, shift @ARGV) || die "failed to open replacement file: $!";

my @words;
# get all words into an array
while ($_=<WORDS>) {
  chop; # strip eol
  push @words, split; # break up words on line
}

# (optional)
# sort by length (makes sure smaller words don't trump bigger ones); ie, "then" vs "the"
@words=sort { length($b) <=> length($a) } @words;

# slurp text file into one variable.
undef $RS;
$text = <REPLACE>;

# now for each word, do a global search-and-replace; make sure only words are replaced; remove possible following space.
foreach $word (@words) {
     $text =~ s/\b\Q$word\E\b\s?//sg;
}

# output "fixed" text
print $text;
