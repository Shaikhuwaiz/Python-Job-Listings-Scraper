# Python Job Listings Scraper

A beginner-friendly Python web scraper that collects job listings from the
[Fake Python Jobs](https://realpython.github.io/fake-jobs/) website and stores
the results in a CSV file.

## What It Scrapes

For each job posting, the scraper extracts:

- Job title
- Company name
- Location
- Job detail page URL

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

## Usage

Run the scraper:

```powershell
python scraper.py
```

By default, the scraper writes results to `jobs.csv`.

You can also choose a custom output file:

```powershell
python scraper.py --output python_jobs.csv
```

## View In Browser

You do not need a separate frontend project. This repository includes a small
Flask app that displays the scraped jobs in an HTML table.

Run the web app:

```powershell
python app.py
```

Then open this URL in your browser:

```text
https://python-job-listings-scraper.vercel.app/
```

## Output Format

The CSV file contains these columns:

```text
job_title,company_name,location,detail_url
```

## Project Structure

```text
.
├── app.py
├── README.md
├── requirements.txt
├── scraper.py
└── templates/
    └── jobs.html
```
