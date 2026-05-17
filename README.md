# Currency Project: Real-time Exchange Rate Tracker & Analyzer

## 🌟 Overview
This project is a Python-based application designed to track real-time currency exchange rates, store historical data, and provide basic analysis through a user-friendly interface. It demonstrates skills in web scraping (or API integration), database management, data processing, and simple web application development using Streamlit.

## ✨ Features
*   **Real-time Exchange Rate Fetching:** Fetches current exchange rates for specified currencies.
*   **Historical Data Storage:** Stores collected currency data in an SQLite database for trend analysis.
*   **Database Management:** Utilizes a simple database manager (`db_manager.py`) to handle currency data storage and retrieval.
*   **Interactive Web Interface:** A Streamlit application (`streamlit_app.py`) for visualizing exchange rates, historical trends, and user interaction.
*   **Automated Data Updates:** (Optional/Future: Can be set up to run daily via cron job or scheduler using `app.bat` for Windows).

## 🚀 Technologies Used
*   **Python:** Core programming language.
*   **Requests & BeautifulSoup4:** For web scraping (if applicable) or a dedicated API client.
*   **Pandas:** For efficient data manipulation and analysis.
*   **SQLite:** Lightweight database for storing historical currency data.
*   **Streamlit:** For creating interactive web applications with Python.
*   **Matplotlib/Plotly:** (Optional, for advanced visualizations within Streamlit).
## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/az2007/currency-project.git
    cd currency-project/currency_project
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install requests beautifulsoup4 pandas streamlit
    ```
    *(Adjust dependencies based on actual use, e.g., if using a different API or visualization library)*

## 💡 How to Run the Application

**For Windows Users (using `app.bat`):**

1.  **Ensure you have Python and the required libraries installed.** (See Installation & Setup above).
2.  **Simply double-click the `app.bat` file** located in the `currency_project` directory.
    *   This script will activate the virtual environment (if configured in the `.bat` file) and then run the Streamlit application.
    *   The application should automatically open in your default web browser.

**For macOS/Linux Users (or manual launch):**

1.  **Ensure your virtual environment is active.**
2.  **Run the Streamlit web application directly:**
    ```bash
    streamlit run streamlit_app.py
    ```
    This will open the application in your web browser.

*(If `currency.py` also needs to be run separately to fetch/update data before launching Streamlit, you might add a step here: `python currency.py`)*

## 📈 Example Usage / Screenshots
*(Here you would insert screenshots or GIFs of your Streamlit app running, showing currency rates, charts, etc.)*

## 🤝 Contribution
Contributions are welcome! If you have suggestions or find issues, please open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License.
