# Curriculum Alignment

## Washington State Learning Standards (OSPI)

This project aligns with multiple Washington State K-12 Learning Standards from the Office of Superintendent of Public Instruction (OSPI).

### Computer Science Standards

**Data and Analysis (Grades 9-12)**
- **CS.DA.9-12.01**: Create interactive data visualizations using software tools to help others better understand real-world phenomena
  - *Project alignment*: Students create visualizations of water quality data using Python (matplotlib, seaborn)

- **CS.DA.9-12.02**: Select data collection tools and techniques to generate datasets that support a claim or communicate information
  - *Project alignment*: Students query SQLite databases to collect specific water quality measurements for analysis

- **CS.DA.9-12.03**: Evaluate the ability of models and simulations to test and support the refinement of hypotheses
  - *Project alignment*: Students test hypotheses about water quality patterns (seasonal, geographic, temporal)

**Algorithms and Programming (Grades 9-12)**
- **CS.AP.9-12.01**: Create prototypes that use algorithms to solve computational problems
  - *Project alignment*: Students write SQL queries and Python scripts to analyze water quality data

- **CS.AP.9-12.04**: Systematically design and develop programs for broad audiences by incorporating feedback from users
  - *Project alignment*: Students modify and extend provided analysis scripts for their research questions

### Mathematics Standards

**Statistics and Probability (High School)**
- **S-ID.A.1**: Represent data with plots on the real number line
  - *Project alignment*: Timeline visualizations of water quality measurements

- **S-ID.A.2**: Use statistics appropriate to the shape of the data distribution to compare center and spread
  - *Project alignment*: Calculate mean, median, standard deviation for water quality parameters

- **S-ID.B.6**: Represent data on two quantitative variables on a scatter plot, and describe how the variables are related
  - *Project alignment*: Correlation between temperature and dissolved oxygen, turbidity and season

**Functions (High School)**
- **F-IF.B.4**: For a function that models a relationship between two quantities, interpret key features of graphs and tables
  - *Project alignment*: Interpret trends in water quality over time

### Science Standards (NGSS-aligned)

**Life Science (High School)**
- **HS-LS2-6**: Evaluate the claims, evidence, and reasoning that the complex interactions in ecosystems maintain relatively consistent numbers and types of organisms
  - *Project alignment*: Analyze water quality data to understand aquatic ecosystem health

- **HS-LS2-7**: Design, evaluate, and refine a solution for reducing the impacts of human activities on the environment
  - *Project alignment*: Identify pollution sources and patterns in water quality data

**Earth and Space Science (High School)**
- **HS-ESS3-1**: Construct an explanation based on evidence for how the availability of natural resources has guided human activity
  - *Project alignment*: Analyze water quality data in context of human water use

- **HS-ESS3-4**: Evaluate or refine a technological solution that reduces impacts of human activities on natural systems
  - *Project alignment*: Use data to evaluate effectiveness of water quality management

**Science and Engineering Practices**
- **Analyzing and Interpreting Data**: Use tools to analyze large datasets
  - *Project alignment*: SQL and Python analysis of 3+ million water quality measurements

- **Using Mathematics and Computational Thinking**: Use digital tools to analyze, model, and/or predict phenomena
  - *Project alignment*: Statistical analysis, spatial analysis, time series analysis

### English Language Arts Standards

**Reading Standards for Literacy in Science and Technical Subjects (Grades 11-12)**
- **RST.11-12.7**: Integrate and evaluate multiple sources of information presented in diverse formats and media
  - *Project alignment*: Students read technical documentation, interpret database schemas, analyze data visualizations

**Writing Standards for Literacy in Science and Technical Subjects (Grades 11-12)**
- **WHST.11-12.2**: Write informative/explanatory texts, including scientific procedures/experiments
  - *Project alignment*: Document analysis procedures, explain findings, write reports on water quality investigations

---

## National Standards

### Next Generation Science Standards (NGSS)

**Crosscutting Concepts**
- **Patterns**: Students observe patterns of water quality across geographic regions, seasons, and time
- **Cause and Effect**: Investigate relationships between environmental factors and water quality measurements
- **Scale, Proportion, and Quantity**: Work with large datasets (millions of measurements), understand spatial and temporal scales
- **Systems and System Models**: Understand water monitoring systems and aquatic ecosystems as complex systems

**Science and Engineering Practices**
- **Asking Questions**: Students formulate research questions based on water quality data
- **Analyzing and Interpreting Data**: Primary focus of the project
- **Using Mathematics and Computational Thinking**: SQL queries, statistical analysis, spatial calculations
- **Constructing Explanations**: Draw conclusions from data analysis
- **Obtaining, Evaluating, and Communicating Information**: Work with real EPA data, communicate findings

### Common Core State Standards for Mathematics

**High School: Statistics and Probability**
- **CCSS.MATH.CONTENT.HSS.ID.A.1**: Represent data with plots
- **CCSS.MATH.CONTENT.HSS.ID.A.2**: Use statistics to compare center and spread
- **CCSS.MATH.CONTENT.HSS.ID.A.3**: Interpret differences in shape, center, and spread
- **CCSS.MATH.CONTENT.HSS.ID.B.6**: Represent data on scatter plots, fit functions to data

### CSTA K-12 Computer Science Standards

**Data & Analysis (Level 3A: Grades 9-10)**
- **3A-DA-09**: Translate between different bit representations of real-world phenomena
  - *Project alignment*: Understand how water quality measurements are encoded in databases

- **3A-DA-10**: Evaluate the tradeoffs in how data elements are organized and where data is stored
  - *Project alignment*: Understand database normalization, indexes, query performance

- **3A-DA-11**: Create interactive data visualizations using software tools
  - *Project alignment*: Generate charts and maps from water quality data

**Data & Analysis (Level 3B: Grades 11-12)**
- **3B-DA-05**: Use data analysis tools and techniques to identify patterns in data
  - *Project alignment*: SQL queries, Python analysis, statistical methods

- **3B-DA-06**: Select data collection tools and techniques to generate datasets
  - *Project alignment*: Design SQL queries to extract relevant subsets of water quality data

- **3B-DA-07**: Evaluate the ability of models to predict outcomes
  - *Project alignment*: Test hypotheses about water quality patterns

---

## Integration Examples

### 1. Environmental Science Class
**Duration**: 3-4 weeks

**Week 1: Introduction to Water Quality**
- NGSS: HS-LS2-6, HS-ESS3-1
- Students explore database structure, run basic queries
- Identify key water quality parameters (temperature, DO, pH, turbidity)

**Week 2: Data Collection and Analysis**
- NGSS: Analyzing and Interpreting Data
- Math: S-ID.A.1, S-ID.A.2
- Students query specific geographic regions or time periods
- Calculate statistics (mean, median, range)

**Week 3: Pattern Identification**
- NGSS: Crosscutting Concept - Patterns
- Math: S-ID.B.6
- Students investigate seasonal patterns, geographic differences
- Create visualizations with Python

**Week 4: Conclusions and Presentation**
- ELA: WHST.11-12.2
- Students write reports explaining findings
- Present data-driven conclusions about water quality

### 2. Computer Science / Data Science Class
**Duration**: 2-3 weeks

**Week 1: SQL and Database Fundamentals**
- CS.AP.9-12.01
- CSTA 3A-DA-10
- Learn database schema, write SQL queries
- Understand joins, aggregations, filtering

**Week 2: Python Data Analysis**
- CS.DA.9-12.01
- CSTA 3B-DA-05
- Load data with pandas, create visualizations
- Statistical analysis with Python

**Week 3: Advanced Analysis (Optional)**
- CS.DA.9-12.02
- Spatial analysis with Haversine formula
- Time series analysis
- Independent projects

### 3. AP Statistics / Pre-Calculus
**Duration**: 1-2 weeks (data analysis unit)

**Focus**: Real-world data analysis
- Math: S-ID.A.1, S-ID.A.2, S-ID.A.3, S-ID.B.6
- Students use SQL to extract data
- Calculate descriptive statistics
- Create scatter plots, analyze correlations
- Interpret distributions and outliers
- Compare multiple datasets (different counties, years)

### 4. Integrated STEM Project
**Duration**: 6-8 weeks

**Combines**: Science, Math, Computer Science, ELA
- Research question formulation (NGSS practices)
- Database queries and data collection (CS standards)
- Statistical analysis (Math standards)
- Written report and presentation (ELA standards)
- Students conduct independent investigations
- Examples:
  - "Does urbanization affect water quality?"
  - "How has water quality changed over the last 30 years?"
  - "What is the relationship between elevation and water temperature?"

---

## Assessment Opportunities

### Formative Assessment
- SQL query accuracy and efficiency
- Correct interpretation of database schema
- Appropriate use of statistical measures
- Quality of data visualizations

### Summative Assessment
- Complete water quality investigation project
- Written report following scientific writing standards
- Presentation of findings with data visualizations
- Peer review of methodology and conclusions

### Skills Development
- **Technical Skills**: SQL, Python, data visualization, database concepts
- **Analytical Skills**: Pattern recognition, statistical reasoning, hypothesis testing
- **Communication Skills**: Technical writing, data storytelling, scientific presentation
- **Critical Thinking**: Data quality evaluation, source credibility, limitations of analysis

---

## Resources for Teachers

### Lesson Planning
- **QUICKSTART.md**: 15-minute student introduction
- **WATER_DATA.md**: Complete SQL tutorial and database guide
- **SPATIAL_ANALYSIS.md**: Geographic analysis lesson
- **INTERVIEW_PREP.md**: Career readiness and technical interview practice

### Professional Development
- EPA STORET system overview: https://www.epa.gov/waterdata/storage-and-retrieval-and-water-quality-exchange
- Water quality parameter reference: https://www.epa.gov/waterdata/water-quality-data-upload-definitions
- SQL tutorial resources (if needed for teacher background)
- Python data analysis resources (pandas, matplotlib)

### Differentiation Strategies
- **Beginner**: Follow guided examples in QUICKSTART.md
- **Intermediate**: Complete sample queries, modify for different parameters
- **Advanced**: Independent investigations, spatial analysis, custom visualizations
- **Extensions**: Add new states, compare multiple regions, time series forecasting

---

## Administrative Considerations

### Technical Requirements
- No server setup required (SQLite database)
- Works on Windows, macOS, Linux
- Free and open source tools
- Minimal disk space (~400 MB per state)

### Time Commitment
- Initial setup: 15-30 minutes (extract package, install Python)
- Basic queries: 1-2 class periods
- Full investigation project: 3-8 weeks (depending on depth)

### Grading and Assessment
- SQL queries can be saved to files and submitted
- Python scripts can be modified and shared
- Visualizations can be exported as images
- Written reports follow standard scientific writing rubrics

### Scaling to Multiple Classes
- Each student can have their own copy of the database
- Queries run locally (no server load)
- Can be distributed via USB drives or network shares
- Works in computer labs or on student laptops

---

## Questions?

See **DETAILED_GUIDE.md** for technical setup, or contact the project maintainers.

**OSPI Standards Reference**: https://ospi.k12.wa.us/student-success/learning-standards-instructional-materials
