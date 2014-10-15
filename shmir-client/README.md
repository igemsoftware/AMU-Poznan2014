shmir_client
============

Client for [sh-miR Designer RESTful API](https://github.com/Nozdi/shmir)

Example usage:

Fold sequence via mfold:
```
./shmir_client.py mfold ACTGAUUUGAC
```

Create sh-miR from one siRNA strand (active) or two siRNa strands separated by space.<br>
First strand is active, both are in 5-3 orientation
```
./shmir_client.py from_sirna UUUGUAUUCGCCCUAGCGC CGCUAUGGCGAAUACAAACA
```

Create sh-miR from transcript name.<br>
Optional parameters
* --min_gc : Minimal "GC" content in strand -- default: `40`
* --max_gc : Maximal "GC" content in strand -- default: `60`
* --max_offtarget : Maximal offtarget of strand -- default: `10`
* --mirna_name : The name of miRNA backbone to use -- default: `"all"`
* --stymulators : One of `["yes", "no", "no_difference"]` -- default: `"no_difference"`
```
./shmir_client.py from_transcript NM_001618.3 --mirna_name miR-30a --min_gc 22
```
