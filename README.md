# scrapy-rtl

Scrapy Project for crawling national news articles on rtl.lu, today.rtl.lu, 5minutes.rtl.lu
and saving them to a MongoDB.

## Requirements

Install Python3

```bash
sudo apt install python3
```

Install MongoDB

```bash
sudo apt install mongodb-org
```

## Installation

Create a virtual environment with [python3](https://www.python.org/downloads/source/) 

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

```bash
scrapy crawl
```
