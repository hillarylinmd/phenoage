# Phenoage Calculator

This Streamlit application calculates the phenotypic age based on various biomarker inputs. Enter your lab results to determine your phenotypic age using a scientifically validated formula.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The Phenoage Calculator app uses several biomarkers from lab reports to calculate an individual's phenotypic age, providing insight into biological age relative to chronological age.

## Features

- Parse unstructured lab reports to extract relevant biomarker values.
- Calculate phenotypic age using a scientifically validated formula.
- User-friendly interface to input lab report data.

## Installation

### Prerequisites

- Python 3.7 or higher

### Steps

1. Clone the repository:

    ```sh
    git clone https://github.com/hillarylinmd/phenoage.git
    cd phenoage
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:

    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8502` to access the app.

3. Paste your lab report into the provided text area and click "Calculate" to get your phenotypic age.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add your message'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact:

- Name: Hillary Lin
- Email: hillary@livorahealth.com
- GitHub: [hillarylinmd](https://github.com/hillarylinmd)
