# Data Scraping

### Setup

1. Download chromedriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
2. Change CHROME_DRIVER_PATH in `/sel_scrapy/sel_scrapy/settings.py`
    `CHROME_DRIVER_PATH = '/usr/lib/chromedriver/chromedriver'`

### Anaconda Environment for selenium, scrapy

1. `conda create -y --name scraper python=3.8`
2. scrapy, selenium installation
    ```bash
    conda install -c conda-forge scrapy
    conda install -c conda-forge selenium
    ```


### macOS, Linux Usage

Change your `xpath` and `selector` based on your website and data to scrape in `fleece.py`.

```bash
cd scrappy/sel_scrapy

scrapy crawl fleece -a category="<CATEGORY_NAME>" -a url="<YOUR_URL_TO_SCRAPE>"
```

# Image Downloader

### macOS, Linux usage

1. Install python if necessary through your package manager. Most likely you already have it preinstalled.
2. Download image downloader script from here:
[https://github.com/webscraperio/image-downloader][image-downloader]
7. Change working to `image-downloader` directory.
8. Run image downloader script by typing:
    ````bash
    python image-downloader /path/to/csv
    ````

![Fig. 2: macOS image download][osx-image-download-script]

 [windows-image-download-script]: docs/images/win-image-downloader.gif?raw=true
 [osx-image-download-script]: docs/images/osx-image-downloader.gif?raw=true
 [image-downloader]: https://github.com/webscraperio/image-downloader/releases
 