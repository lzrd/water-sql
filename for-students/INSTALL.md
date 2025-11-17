# Installation Guide - Washington State Water Quality Data Package

This guide will help you set up everything you need to analyze water quality data on Windows, macOS, or Linux.

**← [Back to README](README.md)** | **[Quick Start Guide](QUICKSTART.md) →**

## Table of Contents

1. [Windows Installation](#windows-installation)
2. [macOS Installation](#macos-installation)
3. [Linux Installation](#linux-installation)
4. [Understanding requirements.txt](#understanding-requirementstxt)
5. [Verifying Installation](#verifying-installation)
6. [Running the Analysis](#running-the-analysis)
7. [Troubleshooting](#troubleshooting)

---

## Windows Installation

### Recommended Approach: Using VSCode

VSCode provides the best experience for beginners - built-in terminal, file explorer, and markdown preview all in one application.

### Step 1: Install Python (if needed)

**Check if you already have Python:**
Open PowerShell and type:
```powershell
py --version
```

If this shows "Python 3.7" or higher, you're ready! Skip to Step 2.

**If you need to install Python:**

**Option A: From Microsoft Store (Easiest)**
1. Open Microsoft Store
2. Search for "Python 3.12" (or latest version)
3. Click "Get" to install
4. Python will be added to your PATH automatically

**Option B: From Python.org**
1. Visit https://www.python.org/downloads/
2. Download "Windows installer (64-bit)"
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

**Verify installation**:
```powershell
py --version
```
Should show: `Python 3.x.x`

### Step 2: Install VSCode

1. Download from https://code.visualstudio.com/
2. Run the installer (use default settings)
3. Launch VSCode when installation completes

### Step 3: Extract the Package

1. Right-click `washington_water_data.tar.gz`
2. Select "Extract All..." (or use 7-Zip if needed)
3. Choose a location like `C:\Users\YourName\Documents\`
4. Click "Extract"

*Note: You may need 7-Zip or WinRAR to extract `.tar.gz` files*
- Download 7-Zip: https://www.7-zip.org/

### Step 4: Open in VSCode

1. Launch VSCode
2. File → Open Folder
3. Navigate to and select the extracted package folder
4. Click "Select Folder"

**You should see:**
- File explorer on the left showing all files
- README.md and other documentation
- Python_Scripts folder
- washington_water.db file

### Step 5: Open Terminal in VSCode

Press **Ctrl+`** (backtick key, usually above Tab)

Or: View menu → Terminal

You should see a PowerShell terminal at the bottom of VSCode.

### Step 6: Install Python Packages

**Important:** Windows PowerShell uses backslashes `\` in file paths!

In the terminal, type:
```powershell
pip install -r .\Python_Scripts\requirements.txt
```

**Note the backslash `\` and the dot `.\` at the beginning!**

**Common messages you might see (these are NORMAL):**

⚠️ **"WARNING: You are using pip version X.Y.Z; however, version A.B.C is available..."**
   - This is just informing you that pip could be updated
   - **Safe to ignore!** Your packages will still install correctly
   - If you want to upgrade pip (optional): `python -m pip install --upgrade pip`

⚠️ **"Requirement already satisfied: pandas..."**
   - Good news! The package is already installed from previous work
   - No action needed

Wait for "Successfully installed..." message.

### Step 7: Run the Analysis Script

**Windows path syntax** (note the backslashes):
```powershell
python .\Python_Scripts\analyze_water_quality_sqlite.py
```

**💡 Tip: Use Tab Completion!**
Type `python .\P` and press **TAB** - PowerShell will auto-complete the path for you!

**If you see "python was not found":**
Try these alternatives:
```powershell
py .\Python_Scripts\analyze_water_quality_sqlite.py
```

Or use the VSCode Run button:
1. Click on `analyze_water_quality_sqlite.py` file to open it
2. Look for the **▷ Run** button in the top-right corner
3. Click it - VSCode finds Python automatically!

**Wait 15-20 seconds** - you'll see progress messages:
- "Opening database file (this may take 10-15 seconds)..."
- "Verifying database structure..."
- The program is working, not frozen!

### Step 8: View the Results

**In VSCode:**
1. Look at the file explorer on the left
2. You should see new PNG files created:
   - water_quality_analysis.png
   - county_comparison.png
   - temporal_coverage.png
3. Click any PNG file to view it in VSCode

**Scroll up in the terminal** to see printed statistics and the "Next Steps" guidance!

---

### Alternative: Command Prompt (No VSCode)

If you prefer not to use VSCode:

1. Extract the package
2. Open File Explorer and navigate to the extracted folder
3. Type `cmd` in the address bar and press Enter (opens Command Prompt in that folder)
4. Run:
   ```cmd
   pip install -r Python_Scripts\requirements.txt
   python Python_Scripts\analyze_water_quality_sqlite.py
   ```
5. Open PNG files with Windows Photos or any image viewer

---

## macOS Installation

### Step 1: Install Python

**Check if Python is installed**:
```bash
python3 --version
```

**If not installed or version < 3.7**:

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3
```

**Option B: From Python.org**
1. Visit https://www.python.org/downloads/macos/
2. Download the macOS installer
3. Run the installer package
4. Follow the installation wizard

### Step 2: Extract the Package

```bash
# Navigate to where you downloaded the file
cd ~/Downloads

# Extract
tar -xzf washington_water_data.tar.gz

# Move to a permanent location
mv washington_water_data ~/Documents/
cd ~/Documents/washington_water_data
```

### Step 3: Install Python Packages

```bash
pip3 install -r requirements.txt
```

*If you get a permission error, try*:
```bash
pip3 install --user -r requirements.txt
```

### Step 4: Run the Analysis

```bash
python3 analyze_water_quality_sqlite.py
```

Open the PNG files with Preview or your favorite image viewer!

---

## Linux Installation

### Step 1: Install Python

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora/RHEL**:
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux**:
```bash
sudo pacman -S python python-pip
```

**Verify installation**:
```bash
python3 --version
```

### Step 2: Extract the Package

```bash
cd ~/Downloads
tar -xzf washington_water_data.tar.gz
mv washington_water_data ~/
cd ~/washington_water_data
```

### Step 3: Install Python Packages

**Option A: System-wide (requires sudo)**
```bash
pip3 install -r requirements.txt
```

**Option B: Virtual Environment (Recommended)**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# When done, deactivate with:
# deactivate
```

### Step 4: Run the Analysis

```bash
python3 analyze_water_quality_sqlite.py
```

---

## Understanding requirements.txt

The `requirements.txt` file lists Python packages needed for the analysis scripts:
- **pandas** - Data manipulation and analysis (like Excel but more powerful)
- **matplotlib** - Creating graphs and charts
- **seaborn** - Statistical visualizations with better styling

### Commented Lines - What Do They Mean?

You may see lines in `requirements.txt` that start with `#`:

```txt
# psycopg2-binary>=2.9.0    # PostgreSQL database adapter
# sqlalchemy>=1.4.0         # Database toolkit
```

**These are commented out intentionally.**

### ⚠️ DO NOT Uncomment These Lines!

**Why they're commented:**
- They're only needed for advanced PostgreSQL mode
- The SQLite package you have doesn't need them
- `psycopg2-binary` can fail to install on systems without PostgreSQL
- Students should use the default SQLite mode

**What to do:**
- Run `pip install -r requirements.txt` **WITHOUT** editing the file
- The commented lines will be ignored (exactly what we want!)
- Only pandas, matplotlib, and seaborn will install

### When Would You Uncomment Them?

Only if you:
1. Have a PostgreSQL database server running
2. Want to use `analyze_water_quality_dual.py` in `--postgres` mode
3. Are comfortable with advanced database setup

**For interview prep and learning:** Stick with the default SQLite mode!

---

## Verifying Installation

### Check Python Version

```bash
python3 --version  # or just: python --version on Windows
```
Should show Python 3.7 or higher.

### Check Packages

```bash
pip list | grep -E "pandas|matplotlib|seaborn"
```

Should show:
```
matplotlib    3.x.x
pandas        1.x.x
seaborn       0.x.x
```

### Check Database File

```bash
ls -lh washington_water.db  # Mac/Linux
dir washington_water.db     # Windows
```

Should show a file around 371 MB.

### Test Database

**Using SQLite command-line tool**:

```bash
# Install sqlite3 if needed (usually pre-installed)
sqlite3 washington_water.db "SELECT COUNT(*) FROM results;"
```

Should output: `3178425`

---

## Running the Analysis

### Basic Usage

```bash
python3 analyze_water_quality_sqlite.py
```

This creates three PNG files:
1. `water_quality_analysis.png` - Parameter trends over time
2. `county_comparison.png` - Geographic distribution
3. `temporal_coverage.png` - Monitoring activity timeline

### Learning Version

To study the code with extensive comments:

```bash
python3 analyze_water_quality_annotated.py
```

Same output, but the code has line-by-line explanations!

### Exploring with SQL

**Interactive mode**:
```bash
sqlite3 washington_water.db
sqlite> SELECT * FROM parameters LIMIT 5;
sqlite> SELECT COUNT(*) FROM stations;
sqlite> .quit
```

**One-line queries**:
```bash
sqlite3 washington_water.db "SELECT county, COUNT(*) FROM stations GROUP BY county;"
```

---

## Troubleshooting

### Issue: "Command not found: python3"

**Windows**: Use `python` instead of `python3`
```cmd
python analyze_water_quality_sqlite.py
```

**macOS/Linux**: Install Python 3 (see installation sections above)

### Issue: "No module named 'pandas'"

**Solution**: Install requirements
```bash
pip install -r requirements.txt

# Or if pip3 is separate:
pip3 install -r requirements.txt

# Or with sudo (Linux):
sudo pip3 install -r requirements.txt
```

### Issue: "Unable to open database file"

**Solution 1**: Make sure you're in the correct directory
```bash
# Should show washington_water.db
ls  # Mac/Linux
dir # Windows
```

**Solution 2**: Copy database to script directory
```bash
cp washington_water.db .
```

### Issue: "Permission denied"

**Mac/Linux**: Make script executable
```bash
chmod +x analyze_water_quality_sqlite.py
./analyze_water_quality_sqlite.py
```

### Issue: Plots are empty or show no data

**Check database integrity**:
```bash
sqlite3 washington_water.db "SELECT COUNT(*) FROM results;"
```

Should return: `3178425`

If different, the database may be corrupted. Re-extract from the archive.

### Issue: "SSL: CERTIFICATE_VERIFY_FAILED" (macOS)

This happens when installing packages on macOS.

**Solution**:
```bash
# Run the certificate install command
/Applications/Python\ 3.x/Install\ Certificates.command
```

Replace `3.x` with your Python version.

### Issue: Graphs won't display (Linux)

**Install matplotlib backend**:
```bash
sudo apt install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

### Issue: "tar: command not found" (Windows)

**Solution**: Use 7-Zip or WinRAR
1. Download 7-Zip: https://www.7-zip.org/
2. Right-click the .tar.gz file
3. Select "7-Zip → Extract Here"

### Issue: Slow performance

The database has 3.1M rows, so queries take time.

**Expected times**:
- Loading database: 1-2 seconds
- Generating plots: 30-60 seconds
- Total runtime: ~1-2 minutes

**Speed tips**:
- Use an SSD if available
- Close other programs to free RAM
- Don't run on a network drive

---

## Advanced: Using Virtual Environments

Virtual environments keep project dependencies isolated.

### Create Virtual Environment

**Windows**:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Deactivate When Done

```bash
deactivate
```

---

## Alternative: Using Jupyter Notebook

If you prefer an interactive environment:

### Install Jupyter

```bash
pip install jupyter
```

### Create a Notebook

```bash
jupyter notebook
```

### In the notebook:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('washington_water.db')
df = pd.read_sql_query("SELECT * FROM parameters LIMIT 10", conn)
print(df)
conn.close()
```

---

## Getting More Help

### Documentation Files

- **WATER_DATA.md** - Comprehensive guide to SQL and the database
- **WATER_DATA.html** - HTML version (open in browser)
- **TIME_CODES.md** - Understanding time codes in data

### Online Resources

**Python**:
- Official Tutorial: https://docs.python.org/3/tutorial/
- Real Python: https://realpython.com/

**SQL & SQLite**:
- SQLite Tutorial: https://www.sqlitetutorial.net/
- SQL Basics: https://www.sqltutorial.org/

**Data Analysis**:
- pandas docs: https://pandas.pydata.org/docs/
- matplotlib tutorial: https://matplotlib.org/stable/tutorials/

**Water Quality**:
- EPA Water Data: https://www.epa.gov/waterdata
- USGS Water Science: https://www.usgs.gov/mission-areas/water-resources

---

## ✓ Installation Complete!

**Congratulations!** You're ready to analyze water quality data.

### Next Steps

1. ✅ **Return to [README.md](README.md)** for an overview
2. 🚀 **Run your first analysis:**
   - Windows: `python .\Python_Scripts\analyze_water_quality_sqlite.py`
   - macOS/Linux: `python3 Python_Scripts/analyze_water_quality_sqlite.py`
3. 📊 **View the PNG visualizations** created in your folder
4. 📖 **Read [WATER_DATA.html](Documentation/WATER_DATA.html)** to learn SQL queries
5. 💼 **Preparing for an interview?** See [INTERVIEW_PREP.md](INTERVIEW_PREP.md) for practice questions

### Learning Path

**Beginner:**
- Run the analysis script and explore PNG outputs
- Read the statistics printed to terminal
- Practice explaining what you see in the graphs

**Intermediate:**
- Open the database with `sqlite3 washington_water.db`
- Try simple SQL queries from WATER_DATA.md
- Modify the analysis script to explore different parameters

**Advanced:**
- Create custom visualizations
- Analyze specific counties or time periods
- Try the exercises in `analyze_water_quality_annotated.py`

**Happy analyzing! 📊🌊**
