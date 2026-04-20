from __future__ import annotations

from flask import Flask, render_template

from scraper import DEFAULT_URL, fetch_page, parse_jobs


app = Flask(__name__)


@app.route("/")
def index():
    """Scrape jobs and display them in a table."""
    html = fetch_page(DEFAULT_URL)
    jobs = parse_jobs(html, base_url=DEFAULT_URL)
    return render_template("jobs.html", jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)
