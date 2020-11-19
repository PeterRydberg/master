# master
Master project containing the different programming exercises done for the thesis.

## Setup

### Backend
Create a new environment using `python3 -m venv /path/to/new/virtual/environment`, then activate it.

Run `pip install -r requirements.txt`.

NOTE: Follow [the guide provided in this repository](https://github.com/NVIDIA/ai-assisted-annotation-client) to set up the Python client for AIAA inference on the machine.

Create an `.env` file, and add the following parameters:
* AWS_SECRET_KEY=[Secret key to your AWS access]
* AWS_PUBLIC_KEY=[Public key to your AWS access]

* DATA_SOURCE_PATH=[Location of the data source directory (e.g. `data_sources\\`)]
* FULL_DIRECTORY_PATH=[Full directory path to this repository]

* AIAA_SERVER=[The IP of the AIAA server, including port if remote]

Create a DynamoDB table called `DigitalTwins` and populate it using the `generate.py` script.

### Frontend
Make sure Node.js is installed.

Run `cd health_platform_manager` to navigate to the correct folder.

Create an `.env` file, local to this folder, and add the following parameters:

* REACT_APP_AWS_SECRET_KEY=[Secret key to your AWS access]
* REACT_APP_AWS_PUBLIC_KEY=[Public key to your AWS access]

* REACT_APP_DATA_SOURCE_PATH=[Location of the data source directory (e.g. `data_sources\`)]
* REACT_APP_FULL_DIRECTORY_PATH=[Full directory path to this repository]

Run `npm install` to install dependencies, then `npm start` to start using the project.
