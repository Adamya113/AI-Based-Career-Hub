import gradio as gr
import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, OnSiteOrRemoteFilters
import pandas as pd

# Configure logging
logging.basicConfig(filename="job_scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize job data storage
job_data = []

# Event Handlers
def on_data(data: EventData):
    job_data.append({
        'Date Posted': data.date,
        'Title': data.title,
        'Company': data.company,
        'Location': data.location,
        'Job Link': data.link,
        'Description Length': len(data.description),
        'Description': data.description,
    })

def on_end():
    logging.info("[ON_END] Scraping completed.")

# Scraper function
def scrape_jobs(query, locations, time_filter):
    global job_data
    try:
        job_data = []

        scraper = LinkedinScraper(
            chrome_executable_path=None,
            chrome_binary_location=None,
            chrome_options=None,
            headless=True,
            max_workers=5,
            slow_mo=0.8,
            page_load_timeout=100,
        )

        scraper.on(Events.DATA, on_data)
        scraper.on(Events.END, on_end)

        if time_filter == "From Past Month":
            time_filter = TimeFilters.MONTH
        elif time_filter == "From Last 24 Hours":
            time_filter = TimeFilters.DAY
        else:
            time_filter = TimeFilters.MONTH  

        queries = [
            Query(
                query=query,
                options=QueryOptions(
                    locations=locations.split(','),
                    apply_link=True,
                    skip_promoted_jobs=False,
                    page_offset=0,
                    limit=100,
                    filters=QueryFilters(
                        # relevance=RelevanceFilters.RECENT,
                        time=time_filter,
                    ),
                ),
            ),
        ]

        scraper.run(queries)
        
        if job_data:
            df = pd.DataFrame(job_data) 
            message = f"Jobs ({len(job_data)}) data successfully scraped."
            logging.info(message)
            return df, message
        else:
            logging.warning("No job data found.")
            return pd.DataFrame(), 'No jobs found.'

    except Exception as e:
        # Handle specific exceptions and log detailed information
        logging.error(f"An error occurred during scraping: {e}", exc_info=True)
        message = f"An error occurred during scraping: {e}. Please check the logs for more details."
        return None, message

def gradio_interface(query, locations, time_filter):
    df, message = scrape_jobs(query, locations, time_filter)
    return df, message

# App Layout
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="Job Query", placeholder="e.g., Data Scientist", value="Blockchain developers"),
        gr.Textbox(label="Locations (comma-separated)", placeholder="e.g., United States, India", value="United States, United Kingdom, India"),
        gr.Dropdown(
            label="Time Filter",
            choices=["From Past Month", "From Last 24 Hours"],
            value="From Last 24 Hours",  # Default option
            type="value",
            ),
    ],
    outputs=[
        gr.Dataframe(label="Job Results", headers=['Date','Company', 'ApplyLink'], interactive=True),
        gr.Textbox(label="Message"),
    ],
    title="Job Scraper",
    description="Enter a job query and locations to scrape job postings and display the results in a table.",
)

if __name__ == "__main__":
    iface.launch()
