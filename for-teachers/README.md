# Water Quality Data Analysis - For Teachers

Create water quality data packages for your students using real EPA data from any U.S. state.

## Quick Start

**Want to create a package for your state?**

→ **[QUICKSTART.md](QUICKSTART.md)** - One-page guide with one command

**Need more details?**

→ **[DETAILED_GUIDE.md](DETAILED_GUIDE.md)** - Complete walkthrough with troubleshooting

## What This Project Provides

### For Your Students
- **Real-world data**: EPA STORET water quality measurements (millions of data points)
- **Professional tools**: SQLite database, SQL queries, Python analysis
- **Immediate start**: No server setup, works on any platform
- **Complete documentation**: Step-by-step tutorials included

### For Your Classroom
- **Standards-aligned**: NGSS, OSPI, Common Core Math, CSTA Computer Science
- **Multiple disciplines**: Environmental Science, Computer Science, Statistics, Integrated STEM
- **Flexible duration**: 1 week to full semester project
- **Local data**: Use data from your state for more student engagement

## Available States

Any U.S. state with EPA STORET data (most states available):
- Washington, Oregon, California
- Illinois, Ohio, Pennsylvania
- Texas, Florida, New York
- And many more...

Browse available states: https://gaftp.epa.gov/Storet/exports/

## Curriculum Alignment

**See [CURRICULUM_ALIGNMENT.md](CURRICULUM_ALIGNMENT.md) for complete mapping to:**
- Washington State (OSPI) standards
- Next Generation Science Standards (NGSS)
- Common Core State Standards for Math
- CSTA K-12 Computer Science Standards

**Example alignments:**
- **Science**: HS-LS2-6 (ecosystem interactions), HS-ESS3-1 (natural resources)
- **Math**: S-ID.A.1 (represent data), S-ID.B.6 (scatter plots and correlation)
- **Computer Science**: CS.DA.9-12.01 (data visualizations), CS.AP.9-12.01 (algorithms)
- **ELA**: WHST.11-12.2 (technical writing)

## Creating a Package

### Option 1: Use Existing State
If a compressed database already exists (`.db.xz` file), you can rebuild in < 1 minute:

```bash
./build.sh washington 1.0
```

### Option 2: Create New State
Download and process EPA data for any state (10-30 minutes):

```bash
./scripts/build_state_package.sh Oregon OR 1.0
```

See **[QUICKSTART.md](QUICKSTART.md)** for complete instructions.

## Distribution Options

**Option 1: Direct Distribution**
- Share the generated zip file via email, cloud storage, or USB drive
- Students extract and start working immediately

**Option 2: GitHub Releases (Automatic)**
- Commit the compressed database to your repository
- GitHub Actions automatically creates releases
- Students download from GitHub

See **[DETAILED_GUIDE.md](DETAILED_GUIDE.md)** for setup instructions.

## Technical Requirements

### For You (Creating Packages)
- Bash shell (Linux, macOS, Git Bash on Windows, WSL)
- Python 3.7+ with pandas
- ~1 GB disk space per state
- 10-30 minutes for initial build

### For Students
- No programming experience required (tutorials included)
- Works on Windows, macOS, Linux
- ~400 MB disk space
- SQLite (pre-installed on most systems) or Python

## Sample Lesson Plans

### 1-Week Environmental Science Unit
- Day 1: Introduction to water quality and database exploration
- Day 2-3: SQL queries and data collection
- Day 4: Python analysis and visualizations
- Day 5: Present findings

### 2-Week Computer Science Module
- Week 1: SQL and database fundamentals
- Week 2: Python data analysis and visualization

### 6-8 Week Independent Investigation
- Students formulate research questions
- Design and execute data analysis
- Write scientific reports
- Present findings

See **[CURRICULUM_ALIGNMENT.md](CURRICULUM_ALIGNMENT.md)** for detailed integration examples.

## Student Materials Included

Every package contains:
- **QUICKSTART.md**: 15-minute guided introduction
- **INSTALL.md**: Platform-specific setup guide
- **WATER_DATA.md**: Complete SQL tutorial and database reference
- **SPATIAL_ANALYSIS.md**: Geographic analysis and mapping
- **INTERVIEW_PREP.md**: Career readiness and technical interview prep
- **example_queries.sql**: Sample queries to modify and extend
- **Python_Scripts/**: Analysis scripts with detailed comments

## Assessment Opportunities

- SQL query accuracy and efficiency
- Statistical analysis correctness
- Data visualization quality
- Written reports (scientific writing)
- Presentations (data storytelling)
- Independent investigation projects

## Support and Questions

**Documentation:**
- **QUICKSTART.md**: Quick start (start here!)
- **DETAILED_GUIDE.md**: Complete guide with troubleshooting
- **ADDING_STATES.md**: Technical details for new states
- **QUICK_REFERENCE.md**: One-page command reference

**Need help?**
- Check the detailed guide for troubleshooting
- Review the automation documentation
- Contact project maintainers

## Example Student Questions

These are all answerable with the provided data:

- How has water quality changed over time in my region?
- What's the relationship between elevation and water temperature?
- Are there seasonal patterns in dissolved oxygen?
- How do urban and rural water quality compare?
- Where are the warmest/coldest monitoring stations?
- Can we predict water quality based on location?

## Success Stories

Students using this project have:
- Presented findings at science fairs
- Used analyses in college applications
- Gained SQL and Python skills for internships
- Developed data science portfolios
- Connected with environmental careers

## Getting Started

1. **Read [QUICKSTART.md](QUICKSTART.md)** - One command to create a package
2. **Review [CURRICULUM_ALIGNMENT.md](CURRICULUM_ALIGNMENT.md)** - Map to your standards
3. **Build a test package** - Try it yourself first
4. **Distribute to students** - Via zip file or GitHub release

---

**Ready to create a package?** → [QUICKSTART.md](QUICKSTART.md)

**Need curriculum mapping?** → [CURRICULUM_ALIGNMENT.md](CURRICULUM_ALIGNMENT.md)
