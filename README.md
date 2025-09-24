Project: JSON to Excel Web Converters

1. Overview
This project is a web-based application designed to convert various types of JSON files into structured Excel spreadsheets. Originally developed as several separate scripts in Google Colab, it has been consolidated into a single, robust web tool that can be accessed by anyone with a web browser.

The application provides a simple user interface where users can select the appropriate JSON format, upload their file, and instantly download a perfectly formatted Excel file, ready for analysis.

2. Key Features

- Multi-Converter Support: The tool handles five distinct JSON formats:
    - Globosat (Composite)
    - Globosat (Planning)
    - FUBOLN
    - A "Generic" converter that can flatten almost any JSON structure.
    - Frequency

- Web-Based Interface: Users interact with a clean, modern webpage, eliminating the need for them to run code in Colab or have Python installed.

- Template-Based Formatting: For specific formats (Globosat, FUBOLN), the output Excel file is structured to match a predefined template, ensuring consistency and ease of use.

- Cloud-Native: The application is built to run on Google Cloud Run, making it a serverless, scalable, and cost-effective solution that requires minimal maintenance.

3. How It Works: Technical Architecture

The project is a Flask web application packaged inside a Docker container. This structure makes it portable and easy to deploy.

- main.py: Runs the Flask web server. It handles webpage rendering, processes user requests (like file uploads), and calls the appropriate conversion logic.

- converters.py: The "engine" of the application. It contains a separate Python function for each of the JSON types, encapsulating the specific data transformation logic.

- templates/index.html: The HTML file that defines the structure of the user interface.

- static/style.css: The CSS file that provides the modern styling and professional look for the webpage.

- Dockerfile: A set of instructions to package the entire application into a standardized container, ready for deployment on any system that supports Docker (including Google Cloud Run).

- requirements.txt: Lists all the necessary Python libraries (like Flask and pandas) required for the application to run.

4. How to Use, Test and Deploy

Local Testing
1-) Setup: On a local machine with Python and VS Code, create a Virtual Environment and install the dependencies from file requirements.txt.

1.1. Open the correct Project Folder and create a new terminal ("Ctrl + '")
1.2. Create the Virtual Environment: "python -m venv .venv"
1.3. Activate the Virtual Environment: ".\.venv\Scripts\Activate"
1.4. Press Ctrl + Shift + P and type Python: Select Interpreter (choose the one with .venv / Recommended)
1.5. Install the required dependencies: "pip install Flask pandas openpyxl"

2-) Run: Execute the main.py script ("python main.py").
3-) Access: Open a web browser and navigate to the provided URL to use/test the tool locally. You can use command "deactivate" to safely return the terminal to its normal state.

Cloud Deployment (Publishing)
1-) Prerequisites: A Google Cloud project with billing and the necessary APIs (Cloud Run, Cloud Build) enabled.
2-) Deploy: From the project directory, a single gcloud command builds the container and deploys the application to Google Cloud Run. If using Google Cloud SDK, this command should be enough "gcloud run deploy json-converter-app --source . --allow-unauthenticated". Make sure to first use commands "gcloud auth login", "gcloud config set project YOUR_PROJECT_ID" and "gcloud config set run/region YOUR_REGION" before running the actual deployment command.
3-) Access: The application becomes instantly available on a public, shareable URL provided by Google Cloud. Access can be restricted using Google's Identity-Aware Proxy (IAP) if needed.