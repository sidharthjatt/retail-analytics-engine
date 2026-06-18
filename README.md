# Retail Analytics & Insight Engine

An end-to-end analytics pipeline built on over one million real e-commerce
transactions. The project cleans raw transactional data, analyses revenue
across products, customers, and markets, and automatically surfaces
business insights that would normally require manual investigation.

## Background

This project uses the UCI Online Retail II dataset — real transaction
records from a UK-based online retailer between 2009 and 2011. With more
than a million rows, it carries the kind of messiness found in production
data: cancelled orders, negative prices, missing customer identifiers, and
operational line items mixed in with actual product sales. Handling this
correctly, rather than blindly dropping rows, was a core part of the work.

## Objectives

The pipeline is designed to answer three practical questions a business
would care about:

- Where does the revenue actually come from, and how concentrated is it?
- Which products and customers drive the most value?
- Are there risks or trends hidden in the data that need attention?

## Approach

The work is split into clear, ordered stages, each in its own script:

1. **Initial inspection** — understanding shape, types, and data quality issues.
2. **Cleaning** — separating cancellations from sales, removing invalid
   prices, and handling missing customer IDs based on the analysis they serve,
   rather than discarding data indiscriminately.
3. **Analysis** — revenue breakdowns by product, country, and customer,
   including a top-N-per-group ranking of customers within each market.
4. **Insight engine** — a module that automatically generates written
   business insights, such as flagging revenue concentration risk or
   detecting trend shifts, so the analysis adapts to any new data.
5. **Visualisation** — a set of charts where each title states the finding,
   not just the axis.

## Key Findings

- The UK accounts for roughly 85% of total revenue, indicating a heavy
  dependence on a single market — a clear business risk.
- Revenue is driven largely by decorative homeware products.
- Cancellations make up around 1.8% of transactions, a useful signal for
  monitoring product or service issues.
- Sales show seasonal movement, peaking ahead of the holiday period.

## Project Structure

    retail-analytics-engine/
    ├── data/        Raw and cleaned datasets
    ├── src/         Pipeline scripts, ordered 01 to 05
    ├── outputs/     Generated charts
    └── README.md

## Running the Project

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    python3 src/01_first_look.py
    python3 src/02_cleaning.py
    python3 src/03_analysis.py
    python3 src/04_insight_engine.py
    python3 src/05_visualizations.py

## Tech Stack

Python, Pandas, NumPy, Matplotlib.

## Author

Sidharth Choudhary