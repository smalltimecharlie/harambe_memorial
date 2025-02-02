# Golf Society Web App

A web application for managing golf players, recording scores, and generating leaderboards.

## Setup

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd golf_society
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   uvicorn main:app --reload
   ```
