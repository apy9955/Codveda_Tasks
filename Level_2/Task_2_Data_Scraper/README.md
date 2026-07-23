# Codveda | Data Scraper

A professional, dark-themed desktop GUI application built with **Tkinter** for scraping heading text (`h1`, `h2`, `h3`) from any website and exporting the results to CSV.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 🎨 Modern dark-themed Tkinter interface
- 🌐 Fetches any webpage via `requests`
- 🔍 Parses HTML with `BeautifulSoup` to extract `h1`, `h2`, and `h3` headings
- 📋 Displays results in a sortable `Treeview` table
- 💾 Exports scraped data to CSV using `pandas`
- ⚠️ Robust error handling for invalid URLs, connection failures, and timeouts
- 🧹 One-click clear and exit controls

## Project Structure

```
codveda-data-scraper/
├── data_scraper.py     # Main application (GUI + scraping logic)
├── scraped_data.csv    # Sample output produced by "Save CSV"
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── .gitignore          # Files/folders excluded from git
```

## Requirements

- Python 3.9 or higher
- Tkinter (included with most standard Python installations)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/codveda-data-scraper.git
   cd codveda-data-scraper
   ```

2. **(Optional) Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python data_scraper.py
```

1. Enter a full website URL (e.g. `https://example.com`) in the input field.
2. Click **Scrape** (or press `Enter`) to fetch and extract headings.
3. Review the extracted `h1`/`h2`/`h3` headings in the results table.
4. Click **Save CSV** to export the results to a CSV file of your choice.
5. Click **Clear** to reset the table, or **Exit** to close the app.

## Error Handling

The application gracefully handles:

- Empty or malformed URLs
- Missing URL scheme (`http://` / `https://`)
- Network/connection failures
- Request timeouts
- HTTP error responses (4xx / 5xx)
- Pages with no `h1`/`h2`/`h3` headings

All errors and successes are surfaced to the user via native message boxes.

## Tech Stack

| Purpose            | Library          |
|---------------------|------------------|
| GUI                 | `tkinter`, `ttk` |
| HTTP requests       | `requests`       |
| HTML parsing        | `beautifulsoup4` |
| CSV export          | `pandas`         |

## Notes on Ethical Scraping

- Always review a website's `robots.txt` and terms of service before scraping.
- Avoid sending excessive requests to a single server in a short period.
- This tool is intended for educational and personal research purposes.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Codveda**
