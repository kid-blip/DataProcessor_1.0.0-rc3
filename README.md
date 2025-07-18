**DataProcessor** is a powerful and versatile tool developed in **Python**, offering comprehensive solutions for reading, processing, filtering, and generating reports from various data sources. From its initial **Alpha version 0.2** as a basic console application to the current **Release 1.0.0** with a full graphical user interface and an executable distribution, the program is designed for efficient automation of data analysis and presentation tasks.

## About the Project

`DataProcessor` has undergone significant development. Starting as a simple console script (~120 lines of code), it has been continuously expanded and improved, including bug fixes (version 0.2.1) and the addition of complex new functionalities. The current **Version 1.0.0** is a fully functional application with an intuitive Graphical User Interface (GUI) that does not require Python or additional libraries to be installed on the user's computer, thanks to its distribution as a **self-contained executable (.exe) file**.

Special attention has been paid to stability, a wide range of features, cross-language support, and maximum user convenience.

## Key Features (Version 1.0.0)

### 1. Graphical User Interface (GUI) - NEW!

* **Intuitive Design:** A clean and minimalist interface, implemented using Tkinter.
* **Easy Navigation:** Functionality is divided into tabs (CSV, Logs, JSON, Web Pages, URL Monitoring, Settings), providing straightforward access to all features.

### 2. CSV File Processing

* **Reading:** Successfully reads data from CSV files, with file selection via the GUI.
* **Filtering:** Powerful capabilities for filtering records based on specified conditions for any column (value comparisons, substring search), with visual input fields for criteria.
* **Reporting:** Generates detailed summary reports for all or filtered CSV data.

### 3. Text Log Analysis

* **Reading:** Reads content from plain text files.
* **Keyword Filtering:** Extracts lines containing a specific word or phrase.
* **Regular Expression (Regex) Filtering:** Advanced filtering of lines based on complex patterns.
* **Reporting:** Provides summaries of log data.

### 4. JSON File Processing

* **Reading:** Loads data from JSON files into Python structures.
* **Filtering:** Ability to filter JSON objects by specified keys and values (supports flat structures).
* **Reporting:** Generates reports on JSON content, including object count and key overview.

### 5. Web Page Parsing (HTML Web Scraping)

* **Content Download:** Retrieves the full HTML content from a specified URL.
* **Custom URLs:** Users can enter URL addresses directly in the GUI.
* **Text Extraction:** Extracts all visible text from a page.
* **Specific HTML Element Extraction:** Automatically detects and extracts content from `<h1>`, `<h2>`, `<p>`, `<a>` tags.
* **Reporting:** Generates reports about the web page.

### 6. Real-time URL Monitoring (NEW!)

* **Background Monitoring:** Ability to specify a URL and an interval for the program to periodically check the page for changes or collect data.
* **Control:** Buttons to start and stop monitoring.

### 7. Multilingual Interface (Localization)

* Full interface support in three languages: **Russian**, **English**, and **Spanish**, with language selection available in the "Settings" section.
* System for detecting missing translations (`LOSING TRANSLATE KEY`) for quick bug fixing.

### 8. Report Saving

* Ability to save all generated reports to text files for later analysis or archiving, with file selection via the GUI.

### 9. Distributed as an .EXE file (NEW!)

* The program is distributed as a self-contained executable file for Windows, requiring no Python installation or additional libraries for the user. Simply download and run!

## How to Run

### Requirements

* Windows operating system (to run the .EXE file).
* For running from source code (if not using the .EXE): Python 3.x and dependencies listed below.

### Running the Executable (.EXE)

1.  Download the `DataProcessor.exe` file from the [Releases](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME/releases) section.
2.  Run the file by double-clicking it.

### Running from Source Code (for Developers)

1.  **Install dependencies**:
    ```bash
    pip install requests beautifulsoup4 # Add any other libraries you used for GUI, e.g., Pillow
    ```
2.  **Clone the repository**:
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git)
    ```
3.  **Navigate to the project directory**:
    ```bash
    cd YOUR_REPOSITORY_NAME
    ```
4.  **Run the program**:
    ```bash
    python your_main_script.py  # Replace with the name of your main Python file
    ```

*Make sure `example.csv`, `example.txt`, `example.json` (if applicable) are in the same directory as the executable or script.*

## Examples of Use (Screenshots)
<img width="1005" height="720" alt="Снимок" src="https://github.com/user-attachments/assets/cdc58f3a-2661-4557-af7a-7509a1ca803d" />
<img width="997" height="739" alt="Снимок3" src="https://github.com/user-attachments/assets/270013af-bba9-4e55-8dcb-694138c7e85e" />
<img width="1002" height="715" alt="Снимок2" src="https://github.com/user-attachments/assets/f5f99b05-7ff1-4f41-a0fc-36f80f8c669a" />

**Example Screenshot: Main GUI Window**
![Main GUI Window](images/main_gui_window.png)
*(Replace 'images/main_gui_window.png' with your actual path and filename)*

**Example Screenshot: CSV Processing Tab**
![CSV Processing Tab](images/csv_tab.png)
*(Replace 'images/csv_tab.png' with your actual path and filename)*

**Example Screenshot: URL Monitoring Tab**
!https://chromewebstore.google.com/detail/tab-monitor/fbfenbmamfnkidjhndnkngincoblnjgk(images/url_monitoring_tab.png)
*(Replace 'images/url_monitoring_tab.png' with your actual path and filename)*
---

## What I Learned While Working on This Project

This project was a huge step forward for me in programming. I gained valuable practical experience in:

* Developing a **full-fledged Graphical User Interface (GUI)** using Tkinter.
* **Packaging Python applications into executable files (.exe)** for easy distribution to users.
* Working with diverse data formats, including structured (CSV, JSON), unstructured (logs), and semi-structured (HTML).
* Implementing **background monitoring** for web resources.
* Applying regular expressions for powerful and flexible text filtering.
* Using external libraries (`requests`, `BeautifulSoup4`) for network requests and web page parsing.
* Implementing a **multilingual interface (localization)**, including handling missing translations.
* Effectively structuring a large amount of code (over 1200 lines!) for better readability and manageability.
* Recognizing the critical importance of code commenting, maintaining code cleanliness, and thorough error handling for creating a stable product.

This experience has significantly expanded my skills and understanding of developing complex, release-ready applications, as well as effectively managing a project from an early Alpha version to a full Release.

## Example Files

The repository includes the following files for demonstration and testing the program's functionality:

* `example.csv`
* `example.txt`
* `example.json` (if you added one)

## Author

kid-blip
