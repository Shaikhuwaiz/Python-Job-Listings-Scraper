from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


DEFAULT_URL = "https://realpython.github.io/fake-jobs/"
DEFAULT_OUTPUT = "jobs.csv"
FIELDNAMES = ["job_title", "company_name", "location", "detail_url"]
MISSING_VALUE = "N/A"


def fetch_page(url: str) -> str:
    """Download the HTML content for the given URL."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def clean_text(element) -> str:
    """Return normalized text for an element, or a default value if missing."""
    if element is None:
        return MISSING_VALUE

    text = element.get_text(strip=True)
    return text if text else MISSING_VALUE


def get_detail_url(card, base_url: str) -> str:
    """Extract the job detail URL from a listing card."""
    detail_link = card.find("a", string=lambda text: text and text.strip().lower() == "apply")

    if detail_link is None:
        detail_link = card.find("a", href=True)

    if detail_link is None or not detail_link.get("href"):
        return MISSING_VALUE

    return urljoin(base_url, detail_link["href"])


def parse_jobs(html: str, base_url: str = DEFAULT_URL) -> list[dict[str, str]]:
    """Parse all job cards from the page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    job_cards = soup.select("div.card-content")
    jobs = []

    for card in job_cards:
        job = {
            "job_title": clean_text(card.select_one("h2.title")),
            "company_name": clean_text(card.select_one("h3.company")),
            "location": clean_text(card.select_one("p.location")),
            "detail_url": get_detail_url(card, base_url),
        }
        jobs.append(job)

    return jobs


def save_jobs_to_csv(jobs: list[dict[str, str]], output_path: str | Path) -> None:
    """Write job listings to a CSV file."""
    output_path = Path(output_path)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(jobs)


def scrape_jobs(url: str = DEFAULT_URL, output_path: str | Path = DEFAULT_OUTPUT) -> list[dict[str, str]]:
    """Fetch, parse, and save job listings."""
    html = fetch_page(url)
    jobs = parse_jobs(html, base_url=url)
    save_jobs_to_csv(jobs, output_path)
    return jobs


def build_parser() -> argparse.ArgumentParser:
    """Build the command line argument parser."""
    parser = argparse.ArgumentParser(description="Scrape job listings from Fake Python Jobs.")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"Page to scrape. Default: {DEFAULT_URL}")
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"CSV file to create. Default: {DEFAULT_OUTPUT}",
    )
    return parser


def main() -> None:
    """Run the scraper from the command line."""
    parser = build_parser()
    args = parser.parse_args()

    jobs = scrape_jobs(url=args.url, output_path=args.output)
    print(f"Saved {len(jobs)} job listings to {args.output}")


if __name__ == "__main__":
    main()
