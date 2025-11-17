# Contributing to Water Quality Data Packages

Thank you for your interest in contributing! This project builds educational packages containing EPA water quality data for students learning data analysis.

## Quick Links

- **Project Overview:** [README.md](../README.md)
- **Adding New States:** [ADDING_STATES.md](ADDING_STATES.md)
- **Quick Reference:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

## Ways to Contribute

### 1. Add Support for New States

The most valuable contribution is adding new state data packages. See [ADDING_STATES.md](ADDING_STATES.md) for complete instructions.

**Quick version:**
1. Download EPA STORET data for your state
2. Run the parser: `python3 src/parse_state_data.py data/YourState -s XX -n StateName`
3. Import to SQLite using the auto-generated script
4. Build the package: `./build.sh yourstate 1.0`
5. Test the package with a student
6. Submit a pull request with documentation

### 2. Improve Student Documentation

Help make the project more accessible to beginners:

- **Test with real students** and report usability issues
- **Improve installation instructions** for different platforms
- **Add examples and exercises** to documentation
- **Create video tutorials** showing setup and analysis
- **Translate documentation** to other languages

### 3. Enhance Analysis Scripts

Improve the Python analysis tools:

- Add new visualization types
- Improve performance for large datasets
- Add statistical analysis features
- Create Jupyter notebook examples
- Add data quality checks

### 4. Report Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/your-repo/issues) with:

- **Clear description** of the problem or suggestion
- **Steps to reproduce** (for bugs)
- **Expected vs actual behavior**
- **Your environment** (OS, Python version)

## Development Setup

### Prerequisites

- Python 3.7+
- Git
- sqlite3 command-line tool
- For building: bash, tar, gzip

### Clone and Setup

```bash
git clone https://github.com/your-repo/water-sql.git
cd water-sql

# Install Python dependencies
pip install -r src/Python_Scripts/requirements.txt

# Test the build system (requires existing database)
./build.sh washington 1.2.1
```

### Project Structure

```
water-sql/
├── src/                          # Source files
│   ├── templates/                # Student documentation templates
│   ├── Python_Scripts/           # Analysis scripts
│   ├── parse_state_data.py       # Universal state parser
│   └── convert_md_to_html.py     # Documentation converter
├── data/                         # Raw EPA STORET data (not in git)
├── build/                        # Build artifacts (not in git)
├── dist/                         # Distribution packages
├── docs/                         # Developer documentation
└── build.sh                      # Main build script
```

## Coding Standards

### Python Code

- **Follow PEP 8** style guidelines
- **Use descriptive variable names** (students will read this code)
- **Add docstrings** to functions and classes
- **Comment complex logic** - remember, this is educational
- **Handle errors gracefully** with helpful messages
- **Test on Windows, macOS, and Linux** when possible

### Documentation

- **Write for beginners** - assume no prior database knowledge
- **Use clear examples** with real data from the project
- **Include screenshots** or command output where helpful
- **Test all commands** before documenting them
- **Use markdown** for all documentation
- **Cross-reference** related documents

### Student-Facing Changes

When modifying student documentation or scripts:

- **Test with a real beginner** if possible
- **Emphasize SQLite** (not PostgreSQL) for student packages
- **Avoid jargon** or explain it clearly
- **Provide platform-specific** instructions (Windows/macOS/Linux)
- **Include error troubleshooting** for common issues

## Submission Guidelines

### Pull Request Process

1. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/add-california-support
   ```

2. **Make your changes** following coding standards

3. **Test thoroughly:**
   - Build the package if applicable
   - Test installation on a fresh system
   - Verify documentation accuracy
   - Check for personal paths or references

4. **Commit with clear messages:**
   ```
   Add California water quality data support

   - Add CA data parser configuration
   - Create CA-specific documentation
   - Test with San Francisco Bay Area data
   - Verify 2.1M measurements import correctly
   ```

5. **Push and create pull request:**
   ```bash
   git push origin feature/add-california-support
   ```

6. **Describe your changes** in the PR:
   - What does this add/fix?
   - How was it tested?
   - Any breaking changes?
   - Screenshots/examples if applicable

### Commit Message Format

Use descriptive commit messages:

```
Add feature: Brief description

- Detailed point 1
- Detailed point 2
- Testing notes
```

Good examples:
- `Fix Windows path syntax in INSTALL.md`
- `Add Illinois data support with 1.8M measurements`
- `Improve beginner guidance based on student testing`

Bad examples:
- `fix bug`
- `update docs`
- `changes`

## Code Review Process

All submissions require review. Reviewers will check:

- **Functionality:** Does it work as intended?
- **Documentation:** Is it clear for students?
- **Code quality:** Is it readable and maintainable?
- **Testing:** Has it been tested adequately?
- **Student impact:** Will this help learners?

## Testing

### Manual Testing Checklist

For package changes:
- [ ] Build completes without errors
- [ ] Package extracts correctly
- [ ] README.html opens in browser
- [ ] Python script runs and creates visualizations
- [ ] Database queries work in sqlite3
- [ ] File sizes are reasonable (~200-500 MB)

For documentation changes:
- [ ] All links work
- [ ] Code examples run correctly
- [ ] Instructions tested on target platform
- [ ] HTML conversion looks good

For script changes:
- [ ] Runs on Windows, macOS, and Linux
- [ ] Error messages are helpful
- [ ] Performance is acceptable
- [ ] No hardcoded paths or personal references

## License

By contributing, you agree that your contributions will be licensed under the Mozilla Public License 2.0 (MPL-2.0). See [LICENSE](../LICENSE) for details.

## Questions?

- **General questions:** Open a discussion on GitHub
- **Bug reports:** [Open an issue](https://github.com/your-repo/issues)
- **Feature requests:** [Open an issue](https://github.com/your-repo/issues) with the `enhancement` label
- **Security concerns:** Email (add contact email here)

## Recognition

Contributors will be acknowledged in:
- Git commit history
- Release notes
- Project README (for significant contributions)

Thank you for helping make water quality data more accessible to students!
