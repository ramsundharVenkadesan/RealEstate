import scrapy, sys
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging


# 1. Define the Item Structure (MODIFIED)
class RealEstateItem(Item):
    """
    Defines the fields for a real estate listing.
    Replaced 'name' with 'address'.
    """
    address = Field()  # MODIFIED: New field for street address
    price = Field()
    agency = Field()
    area = Field()

    # Formatted fields for property features
    beds = Field()
    baths = Field()
    sq_ft = Field()


# 2. Define the Spider
class ListingsSpider(scrapy.Spider):
    name = "listings"
    allowed_domains = ["arizonarealestate.com"]

    # Initialize the spider with the 'area' argument
    def __init__(self, area=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.area = area if area else "maricopa"  # Default to 'maricopa'
        self.start_urls = [f"https://arizonarealestate.com/{self.area}"]
        self.logger.info(f"Spider initialized to scrape: {self.area}")
        self.logger.info(f"Starting URL: {self.start_urls[0]}")

    # Note: Custom settings for the spider are typically handled in the execution block.

    def parse(self, response):
        """
        Parses the main listings page to extract individual listing details and handle pagination.
        """
        # Selector for the gallery of listings
        gallery = response.xpath('//div[@class="si-listing"]')

        for listing in gallery:
            item = RealEstateItem()

            # --- MODIFIED: Extract ONLY the street address ---
            # The address is typically the first part of the 'name' XPath
            # .//div[@class="si-listing__title-main"]/text()
            address_raw = listing.xpath(
                './/div[@class="si-listing__title-main"]/text()'
            ).get()

            # Clean up the address: strip whitespace and assign
            if address_raw:
                item['address'] = address_raw.strip()
            # --- END MODIFIED SECTION ---

            # Extract price
            item['price'] = listing.xpath('.//div[@class="si-listing__photo-price"]/span/text()').get()

            # Extract agency
            item['agency'] = listing.xpath('.//div[@class="si-listing__footer"]/div/text()').get()

            # Set the area that was passed during initialization
            item['area'] = self.area

            # Extract and format beds, baths, and sq_ft
            # Extract raw text nodes from the listing info section
            raw_data = listing.xpath(
                './/div[@class="si-listing__info"]//div[@class="si-listing__info-label"]/text() | '
                './/div[@class="si-listing__info"]//div[@class="si-listing__info-value"]/descendant::*/text()'
            ).getall()

            # Clean and normalize the raw data
            cleaned_data = [''.join(x.split()).replace(',', '') for x in raw_data if x is not None and x.strip()]

            # Default values
            item['beds'] = None
            item['baths'] = None
            item['sq_ft'] = None

            # Iterate through the cleaned data to find and assign values
            # The data is structured as [VALUE, LABEL, VALUE, LABEL, ...]
            for i, val in enumerate(cleaned_data):
                # Check for the label, and assume the preceding element is the value
                if i > 0 and val.lower() == 'beds':
                    # Extract the numerical value for beds
                    item['beds'] = cleaned_data[i - 1]
                elif i > 0 and 'bath' in val.lower():  # Catches 'Baths', '1/2 Baths', etc.
                    # Extract the numerical value (or fraction) for baths
                    item['baths'] = cleaned_data[i - 1]
                elif i > 0 and val.lower() == 'sq.ft.':
                    # Extract the numerical value for square feet
                    item['sq_ft'] = cleaned_data[i - 1]

            yield item

        # --- START PAGINATION LOGIC ---
        # Find the 'Next' button link using the class selector
        next_page = response.xpath('//a[contains(@class, "next")]/@href').get()

        if next_page:
            self.logger.info(f"Found next page: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        # --- END PAGINATION LOGIC ---


# 3. Execution Block for Standalone Script
# This section runs the spider and directs the output to a JSON file.
if __name__ == '__main__':
    # 1. Handle command line input
    # Check if an argument (the area name) was passed.
    try:
        # sys.argv[0] is the script name; sys.argv[1] is the first argument
        area_input = sys.argv[1]
    except IndexError:
        # If no argument is provided, print usage and exit gracefully
        print("Error: Please provide a real estate area (e.g., tempe, phoenix) as an argument.")
        print("Usage: python Spider.py <area_name>")
        sys.exit(1)

    output_filename = f"{area_input}.json"

    # Configure logging to show essential information
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    # Define settings for the process, including output format and file path
    process = CrawlerProcess(settings={
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 5,  # Delay between requests to be polite
        "USER_AGENT": "BenignCrawlerProject/1.0 (+research purposes)",

        # Settings to output the scraped data to a JSON file, using the dynamic filename
        "FEEDS": {
            output_filename: {
                "format": "json",
                "encoding": "utf8",
                "store_empty": False,
                # IMPORTANT: Specify the new fields order for the output, using 'address'
                "fields": ['address', 'price', 'agency', 'area', 'beds', 'baths', 'sq_ft'],
                "indent": 4,
                "item_classes": [RealEstateItem],
                "overwrite": True,
            }
        },
    })

    print("-" * 50)
    print(f"Starting Scrapy spider for area: {area_input}")
    print(f"Data will be saved to '{output_filename}' upon completion.")
    print("-" * 50)

    # Start the crawl, passing the area_input as the 'area' argument
    process.crawl(ListingsSpider, area=area_input)
    process.start()  # The script will block here until the crawl is finished

    print("-" * 50)
    print(f"Crawl finished. Check '{output_filename}' for the results.")
    print("-" * 50)
