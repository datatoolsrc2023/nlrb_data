# README

## TODO

- Extract case data from [NLRB case search site](https://nlrb.gov/search/case) by either
    - Manually downloading CSV(s) of case data, then parsing CSV(s) for case links and scraping additional data for individual cases, or
    - Scraping HTML tables of case data using requests and BeautifulSoup (and following case links to scrape additional data for individual cases using Scrapy) from [advanced case search site](https://www.nlrb.gov/advanced-search)
- Transform and clean case data using PETL or Polars
- Load case data to database
- Analyze and visualize case data with Plotly or something else