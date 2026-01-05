### Collecting Data
The data is sourced by [OpenAQ](https://openaq.org/).   
My project makes use of there API and S3 public bucket. See `collect_data.py` script for more.     
Broadly, the script first gets all the available station ids in the NCR region thru OpenAQ API. Then, iterates over the ids and copies the data of the station into local system by AWS CLI through the open aq public bucket.

Requirements: OpenAQ API key, AWS CLI setup   
Setup:   
    1. Install required packages.   
    2. Get the requirements fulfilled.   
    3. Run `python collect_data.py` in the venv to get the data in folder `./open-aq-data`. You can move it to your desired place.

***