# master
Master project containing the different programming exercises done for the thesis.

## Notes for future development

This code is written for the master's thesis titled *"Developing a Digital Twin-Based Prototype for Medical Knowledge Generation and AI-Assisted Image Segmentation"*. Read it first if you're going to use any of this code.

Most of this code was developed during autumn 2020. A lot has changed since the release of [Clara Train 4.0](https://docs.nvidia.com/clara/clara-train-sdk/index.html), as it now incorporates Monai as a part of its framework. I strongly suggest writing the ecosystem from scratch with these new updates in mind. Only use this repository as experimental guidance at best.

**Things to note:**
* Most of the code is written in such a way that it *locally* uses SSH to execute scripts on a remote server. In other words, you need to set up the repo on your own computer *and* on the server you're training your models on. This is just a bad and early design choice, so I suggest re-writing the code to work in a Docker container on the same server with GPUs you're using. This will also simplify directory paths a lot.
  * The paths in this project are specific and should be changed.
* The three components are written as Python classes that interact with each other, initially because it was convenient. Now it's overly complicated. Make these components into RESTful APIs or something. That way, the components can run independently (maybe even on different servers if desired) and query each other when needed.
* Currently, the Knowledge Bank scans all newly updated digital twins for images to do inference on. Rewrite this so that the digital twin can query the Knowledge Bank directly for predictions (e.g. using a RESTful approach).
* The *docker\_\*.sh* scripts, along with most of the files in the root folder, were made for convenience. Use them as you wish if you find them useful.
* The *health_platform_manager* makes AWS calls directly for some reason. Make sure this is only done in the Digital Twin component.

## Setup

### Backend
Create a new environment using `python3 -m venv /path/to/new/virtual/environment`, then activate it.

Run `pip install -r requirements.txt`.

NOTE: Follow [the guide provided in this repository](https://github.com/NVIDIA/ai-assisted-annotation-client) to set up the Python client for AIAA inference on the machine.

Set up an AWS Dynamo instance.

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
