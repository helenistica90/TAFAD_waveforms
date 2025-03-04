📡 TAFAD Waveforms - Automatic Seismic Data Downloader

This repository contains a Python script for automating the downloading of seismic waveforms from TAFAD (Turkish National Seismic Network) using Selenium. It retrieves MiniSEED files for a selected seismic station, organizes them based on earthquake magnitude, and ensures efficient data collection.

📌 Overview

This script automates the search, selection, and download of seismic records from TAFAD, filtering data based on a specific seismic station. It also extracts earthquake magnitudes (MW, ML, or MD) from the event details and categorizes the downloaded waveforms accordingly.

📊 Features

✔ Automated Login & Navigation – The script logs in as a guest and handles the website’s interface.
✔ Seismic Event Search – Finds earthquake records for a predefined station.
✔ MiniSEED Downloading – Extracts and downloads seismic waveforms.
✔ Magnitude Extraction – Reads and identifies the earthquake’s magnitude.
✔ File Organization – Saves files into structured folders based on magnitude.
✔ Duplicate Prevention – Avoids re-downloading already processed events.
✔ Error Handling & Recovery – Manages unexpected errors and reconnects if needed.

📂 Required Data

Before running the script, set up the following:
	•	Station Code (station_code_to_search) → Select the seismic station of interest.
	•	Download Path (base_path) → Define where the files will be stored.
	•	Used Event Numbers File (used_event_numbers.txt) → Keeps track of processed events to avoid repetition.

🛠 Usage

1️⃣ Installation

Ensure Python 3.x is installed, along with the required dependencies:

pip install selenium

2️⃣ Setup
	•	Update the station_code_to_search variable with the desired station code.
	•	Modify the download folder path (base_path) to match your system.

3️⃣ Run the script

python TAFAD_waveforms.py

The script will begin downloading and organizing seismic waveforms automatically.

📬 Reference

If you use this code for research, please cite:
Seivane H. (2025). Automatic Downloading of TAFAD Waveforms.
Available at: https://github.com/helenistica90/TAFAD_waveforms

📧 Contact

For questions or collaborations, feel free to reach out:
📩 helena.seiv@outlook.com
