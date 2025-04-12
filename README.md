# Package Diff Tool

This tool compares binary packages between the `sisyphus` and `p10` branches of the ALT Linux repository using the public REST API.

## Requirements

*   Python 3.6+
*   `requests` library
*   `rpm` (python-rpm) library

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/gargulia/package_diff
    cd package_diff
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install requests python-rpm
    ```

## Usage

1.  **Run the `package_diff_cli.py` script:**

    *   **To print the JSON output to the console:**

        ```bash
        python package_diff_cli.py
        ```

    *   **To save the JSON output to a file:**

        ```bash
        python package_diff_cli.py -o output.json
        ```

        or

        ```bash
        python package_diff_cli.py --output output.json
        ```

## Output

The tool outputs a JSON structure containing the following information for each architecture:

*   `p10_only`: A list of package names that are present in the `p10` branch but not in the `sisyphus` branch.
*   `sisyphus_only`: A list of package names that are present in the `sisyphus` branch but not in the `p10` branch.
*   `version_diff`: A list of packages where the version-release is greater in `sisyphus` than in `p10`. Each entry in the list contains:
    *   `name`: The name of the package.
    *   `sisyphus_version`: The version-release of the package in `sisyphus`.
    *   `p10_version`: The version-release of the package in `p10`.

**Example Output:**

json
{
    "x86_64": {
        "p10_only": [
            "package1",
            "package2"
        ],
        "sisyphus_only": [
            "package3"
        ],
        "version_diff": [
            {
                "name": "package4",
                "sisyphus_version": "2.0-1",
                "p10_version": "1.5-2"
            }
        ]
    },
    "noarch": {
        "p10_only": [],
        "sisyphus_only": [
            "package5"
        ],
        "version_diff": []
    }
}


## Notes

*   This tool relies on the availability and structure of the ALT Linux RDB API.  Changes to the API may break the tool.
*   Error handling is included to catch network issues and JSON parsing errors.
*   The version comparison uses the `rpm` library for accurate version comparison according to RPM packaging rules.
*   The tool iterates through all architectures present in either `sisyphus` or `p10`.
