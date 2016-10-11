# course-recommendations
Course recommendations using AI

## Inputs
+ courses enjoyed
+ teachers enjoyed
+ year
+ major / concentration

## Starting data
```
year .... liked
----------------
2020  ...  18.02 Alice, 8.01 Bob, 3.091 Eve
```

## After Python script to transform data
```
year liked           also liked
------------------
2020 18.02 Alice     8.01 Bob
2020 8.01 Bob        Alice
2020 18.02 Alice     3.091 Eve
....etc
```

## `tranform.py`
### Requirements
+ pip
