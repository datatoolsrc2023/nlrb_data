# 04_pages

Running this task will scrape raw `.html` `<article>` sections for all cases in the `cases` table and insert the raw text into your db. This info is used in later tasks for parsing out cases' participants, docket activity, related cases, and voting information that's unavailable (or difficult to glean) from the original raw `.csv` downloads from the NLRB site.

## Running the task
The scraping task can take quite some time depending on the number of cases in your `cases` table, your internet connection, etc. Given the inconsistencies and reliability limitations when running requests multiple times, you may need to stop and restart this task.

- To start the task: `cd` into this directory, and run `make`. 
- If you need to stop scraping: `^C` to Keyboard Interrupt. It may take a few seconds for all threads to terminate and exit out gracefully. You'll get a prompt on how many cases remain to scrape.
- To **restart** the task after a keyboard interrupt or due to a connection error that stalls it out: run `make task post`.

## Notes
The scraper runs parallel threads. It defaults to 5 workers. To tune this, change the `max_workers` variable near the top of `task.py` in this directory.
Each fetch can take anywhere from about 2 to 20 seconds, settling near the lower end of that range once it's up and running. With 5 parallel threads, the task should scrape roughly 100 cases per minute. For a large dataset (such as all ~400,000 cases through 2022), this process will take many hours.