# Verge Scraper

This is an example scraper that scrapes [The Verge](https://www.theverge.com) and smartly extracts all the articles link, headline, authors, and date of publication.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required dependencies.

_for example:_
```sh
pip install selenium
```

## Steps to run:
1. Clone the repo: 
    ```sh
    git clone git@github.com:AmnGrg0511/verge.git
    ```

1. Change current working directory:
    ```sh
    cd Verge
    ```

1. Run the script:
    ```sh
    python scrape_the_verge.py
    ```
    > Note: If you see any errors, please make sure all the packages are installed. 

    <br/>
    
1. Read the generated verge.db:
    ```sh
    python read_db.py
    ```
    Or open the generated csv file to see the data

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
