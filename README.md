# TurboParse
This is a parser designed for
[TURBOMOLE™](http://www.cosmologic.de/turbomole/home.html) outputs to extract
essential information, and output a CSV file.

## Information Extracted
- [x] Ground energy
- [x] Excited energy (nm)
- [x] Excited energy (eV)
- [x] Molecular orbitals ≥10% contribution
    - [x] Orbital numbers
    - [x] Contribution coefficient
- [x] Oscillator strength (length)

## Supported Functions
- [x] escf
- [x] ricc2

## Requirements
- Python 3.5+
- Windows, macOS, or Linux

## Usage
For Windows users:
```
turboparse [-h] [-m] [-v] METHOD PATH NUM
```
- It is not recommended to use turboparse on WSL (#1).

For Linux/macOS users:
```
chmod +x ./turboparse
./turboparse [-h] [-m] [-v] METHOD PATH NUM
```

The script can be added to $PATH, although the location of the list file must
be absolute or relative to the current working folder.

## Arguments
### Required
```
  METHOD      Method to parse
  PATH        Path of list file
  NUM         Number of excited states to parse
```

### Optional
```
  -h, --help  Show this help message and exit
  -m          Parse HOMO-LUMO orbitals
  -v          Verbose
```

## List File Format
The list file is essentially a CSV file in `PATH,NAME` format. The paths can
be absolute or relative to the location of the list file.

E.g.,
```
/home/mushinako/proj/molecule1,aldosterone
/home/mushinako/proj/molecule2,corticosterone
```

## Contribution
All contributions are greatly appreciated. Due to the specialty and the nature
of this project, I honestly do not expect any contribution.

## License
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
</a>

This work is licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
Creative Commons Attribution-ShareAlike 4.0 International License
</a>.

[TURBOMOLE™](http://www.cosmologic.de/turbomole/home.html) is the trademark of
Turbomole GmbH.
