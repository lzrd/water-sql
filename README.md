# Water Quality Data Analysis

Real EPA water quality data for students, with complete automation for teachers, built by the open source community.

---

## 👋 Choose Your Path

### 🎓 **I'm a Student**
You want to analyze water quality data using SQL and Python.

→ **[for-students/](for-students/)** - Start here for tutorials and documentation

**Quick links:**
- [QUICKSTART.md](for-students/QUICKSTART.md) - 15-minute introduction
- [WATER_DATA.md](for-students/WATER_DATA.md) - Complete SQL tutorial
- [SPATIAL_ANALYSIS.md](for-students/SPATIAL_ANALYSIS.md) - Geographic analysis

---

### 👩‍🏫 **I'm a Teacher**
You want to create water quality packages for your students.

→ **[for-teachers/](for-teachers/)** - Guides, curriculum alignment, and automation

**Quick links:**
- [QUICKSTART.md](for-teachers/QUICKSTART.md) - Create a package with one command
- [CURRICULUM_ALIGNMENT.md](for-teachers/CURRICULUM_ALIGNMENT.md) - OSPI, NGSS, Common Core standards
- [DETAILED_GUIDE.md](for-teachers/DETAILED_GUIDE.md) - Complete walkthrough

---

### 👨‍💻 **I'm a Developer**
You want to contribute to this project.

→ **[for-developers/](for-developers/)** - Technical documentation and contribution guides

**Quick links:**
- [ARCHITECTURE.md](for-developers/ARCHITECTURE.md) - System design and data pipeline
- [AUTOMATION.md](for-developers/AUTOMATION.md) - Build system and GitHub Actions
- [CONTRIBUTING.md](for-developers/CONTRIBUTING.md) - How to contribute

---

## What Is This Project?

This project provides **ready-to-use water quality data packages** for education. Each package contains:

- **Real EPA STORET data** - Millions of water quality measurements from monitoring stations
- **SQLite database** - Professional tool, no server setup required
- **Complete tutorials** - SQL, Python, statistics, geographic analysis
- **Analysis scripts** - Ready to run, easy to modify
- **Standards-aligned** - NGSS, OSPI, Common Core, CSTA Computer Science

### Available States

Any U.S. state with EPA STORET data:
- Washington, Oregon, California
- Illinois, Ohio, Pennsylvania
- Texas, Florida, New York
- And many more...

### What You Can Do

**Students learn:**
- SQL queries on large datasets (3+ million rows)
- Python data analysis (pandas, matplotlib)
- Statistics and pattern recognition
- Geographic analysis and mapping
- Real-world data science skills

**Teachers create:**
- Custom packages for any U.S. state
- Standards-aligned lesson plans
- Environmental science projects
- Computer science modules
- Integrated STEM investigations

**Developers contribute:**
- New states and regions
- Analysis features
- Documentation improvements
- Automation enhancements

---

## Quick Start by Audience

### Students: Get Started in 15 Minutes
1. Extract the package you received
2. Open `QUICKSTART.html` or `QUICKSTART.md`
3. Follow the tutorial

→ [Full student documentation](for-students/)

### Teachers: Create a Package
One command creates a complete distribution:
```bash
./scripts/build_state_package.sh Oregon OR 1.0
```

→ [Full teacher documentation](for-teachers/)

### Developers: Set Up Development
```bash
git clone https://github.com/yourusername/water-sql.git
cd water-sql
pip install -r requirements.txt
./scripts/build_state_package.sh Washington WA 1.0
```

→ [Full developer documentation](for-developers/)

---

## Example Questions Students Can Answer

- How has water temperature changed over the last 20 years?
- Which rivers have the best water quality?
- Are there seasonal patterns in dissolved oxygen?
- How does elevation affect water temperature?
- Where are the coldest/warmest monitoring stations?
- Can we predict water quality based on location?

---

## Technology Stack

- **SQLite** - File-based database (no server needed)
- **Python** - pandas, matplotlib, seaborn for analysis
- **EPA STORET** - Official U.S. water quality monitoring data
- **Open Source** - Free for educational use

---

## Sample Data

**Washington State** (example):
- **3.1+ million measurements** from 6,892 monitoring stations
- **1,587 parameters** (temperature, dissolved oxygen, pH, turbidity, etc.)
- **Decades of data** (1950s to present)
- **Statewide coverage** (all counties)

Other states have similar comprehensive datasets.

---

## Standards Alignment

Aligns with multiple learning standards:
- **NGSS** (Next Generation Science Standards)
- **OSPI** (Washington State standards)
- **Common Core** (Mathematics)
- **CSTA** (Computer Science Teachers Association)

See [CURRICULUM_ALIGNMENT.md](for-teachers/CURRICULUM_ALIGNMENT.md) for complete mapping.

---

## Project Status

✅ **Active** - Currently used in classrooms
✅ **Multi-state** - Washington, Illinois, easily add more
✅ **Automated** - GitHub Actions for releases
✅ **Well-documented** - Tutorials for all skill levels

---

## Support and Community

- **Documentation**: Organized by audience (students, teachers, developers)
- **Issues**: Report bugs or request features on GitHub
- **Contributions**: See [CONTRIBUTING.md](for-developers/CONTRIBUTING.md)

---

## License

This project is open source and available for educational use.

EPA STORET data is public domain (U.S. government data).

---

## Acknowledgments

- **EPA STORET** - Water quality monitoring data
- **Contributors** - Everyone who has improved this project
- **Teachers** - Who use this in their classrooms
- **Students** - Who explore and learn with this data

---

## Navigation

* [Student Documentation](for-students/) - Tutorials and analysis guides
* [Teacher Documentation](for-teachers/) - Create packages and lesson plans
* [Developer Documentation](for-developers/) - Technical architecture and contributing

---

**Questions?** Start with the documentation for your audience (students, teachers, or developers).
