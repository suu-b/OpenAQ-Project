# See README.md
import requests
import os
import subprocess
import logging
from dotenv import load_dotenv

load_dotenv()

# Config
OPEN_AQ_KEY = os.getenv("OPEN_AQ_KEY")
YEAR = "2025"
BBOX = "76.85,26.42,78.29,29.59"  # Delhi-NCR region
PARAMETERS = ['2', '3', '4', '5', '6', '11', '12', '13', '10', '9']

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def s3_prefix_exists(s3_prefix):
    check_cmd = [
        r"C:\Program Files\Amazon\AWSCLIV2\aws.exe", "s3", "ls",
        s3_prefix,
        "--no-sign-request"
    ]
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    return result.returncode == 0 and bool(result.stdout.strip())


def main():
    logging.info("Starting setup...")

    parameters_str = ','.join(PARAMETERS)
    logging.info("Parameters: %s", parameters_str)

    url = f"https://api.openaq.org/v3/locations?iso=IN&bbox={BBOX}&parameters_id={parameters_str}"
    response = requests.get(url, headers={"X-API-KEY": OPEN_AQ_KEY})
    locations = response.json().get("results", [])
    location_ids = [loc["id"] for loc in locations]
    logging.info("Loaded %d location IDs", len(location_ids))

    local_base = "./openaq-data"
    os.makedirs(local_base, exist_ok=True)

    for loc_id in location_ids:
        logging.info("Processing location ID: %s", loc_id)
        s3_prefix = f"s3://openaq-data-archive/records/csv.gz/locationid={loc_id}/year={YEAR}/"

        if not s3_prefix_exists(s3_prefix):
            logging.warning("No files found for %s, skipping", loc_id)
            continue

        local_folder = os.path.join(local_base, f"location_{loc_id}")
        os.makedirs(local_folder, exist_ok=True)

        cmd = [
            r"C:\Program Files\Amazon\AWSCLIV2\aws.exe", "s3", "cp",
            "--no-sign-request",
            "--recursive",
            s3_prefix,
            local_folder
        ]

        logging.debug("Running command: %s", " ".join(cmd))
        try:
            subprocess.run(cmd, check=True)
            logging.info("Successfully copied files for %s", loc_id)
        except subprocess.CalledProcessError as e:
            logging.error("Failed to copy files for %s: %s", loc_id, e)

    logging.info("Setup complete!")


if __name__ == "__main__":
    main()
