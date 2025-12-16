# Python Mail Sender

This project sends POST requests to a specified endpoint for each email address in a given CSV file. It uses Python, the `requests` library, and handles configuration via environment variables.

## Prerequisites

- **Conda** (Anaconda or Miniconda) must be installed.
- An API Key and Endpoint URL for the service you are targeting.

## Setup

1.  **Configure Environment Variables**:
    
    Copy the template file to `.env`:
    ```bash
    cp env.template .env
    ```
    
    Open `.env` in a text editor and fill in your `API_KEY` and `ENDPOINT_URL`.

2.  **Prepare your CSV**:
    Create a CSV file (e.g., `emails.csv`) with your email addresses. The script looks for the first column or expects a single list of emails.

## Usage

### Using the Bash Script (Recommended)

The included `run.sh` script handles creating/updating the Conda environment and running the Python script in one go.

```bash
./run.sh path/to/your/emails.csv
```

### Manual Setup

If you prefer to run things manually:

1.  **Create/Update Conda Environment**:
    ```bash
    conda env create --file environment.yml
    # OR if it exists
    conda env update --file environment.yml
    ```

2.  **Activate Environment**:
    ```bash
    conda activate python-mail-env
    ```

3.  **Run Script**:
    ```bash
    python surveyMail.py emails.csv
    ```

## File Structure

- `surveyMail.py`: Main Python script.
- `environment.yml`: Conda environment specification.
- `run.sh`: Helper script for setup and execution.
- `.env`: (Not committed) Stores secrets.
- `env.template`: Template for `.env`.

