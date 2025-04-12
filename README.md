# Package Diff Tool

This utility allows you to compare binary packages between the ALT Linux branches (`sisyphus` and `p10`).
It uses the public REST API to get data about packages and compares them by architecture, availability, and versions.

## Requirements

*   Python 3.6+
*   `requests` library
*   `packaging` library

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/gargulia/package_diff
    cd package_diff
    ```
2.  **Install dependencies:**

The utility requires Python 3.6+ and the rpm library to work. Install dependencies using pip:

```bash
pip install requests
```

To install the packaging package in ALT Linux, using pip:

```apt-get update
pip install packaging
```

## Usage

Run the script using the command:

```bash
python3 package_diff.py [options]
```

### Options

- `-o, --output <file>` — Save the result in a JSON file.
- `-v, --verbose` — Display detailed information about the comparison.

### Examples

1. **Save the result to a file:**

```bash
 python3 package_diff.py -o result.json
```

2. **Output detailed information:**

```bash
 python3 package_diff.py -v
```

3. **Save the result and output detailed information:**

```bash
 python3 package_diff.py -o result.json -v
```

## Result

The comparison result includes the following data for each architecture:

- `p10_only`: Packages that are only in the `p10` branch.
- `sisyphus_only': Packages that are only in the `sisyphus` branch.
- `version_diff`: Packages whose versions differ between branches.


## Notes

*   This tool relies on the availability and structure of the ALT Linux RDB API.  Changes to the API may break the tool.
*   Error handling is included to catch network issues and JSON parsing errors.
*   The tool iterates through all architectures present in either `sisyphus` or `p10`.
