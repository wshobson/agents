# Setup Guide for Stock Analysis Scripts

## Quick Start

### 1. Install Python Dependencies

```bash
cd plugins/stock-analysis/scripts
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python fetch_financial_data.py --help
```

## Understanding IDE Warnings

If your IDE (PyCharm, IntelliJ, VS Code) shows warnings about standard library modules like:
- `No module named 'argparse'`
- `No module named 'json'`
- `No module named 'sys'`
- `Unresolved reference 'datetime'`

**These are FALSE POSITIVES** - these modules are built into Python and don't need installation.

### Why This Happens

IDEs sometimes can't detect the Python interpreter correctly, especially if:
- Multiple Python versions are installed
- Virtual environment is not configured
- IDE Python interpreter path is incorrect

### Solutions

#### PyCharm/IntelliJ IDEA
1. Go to **File → Settings → Project → Python Interpreter**
2. Select the correct Python interpreter (Python 3.8+)
3. Click **Apply** and **OK**
4. The warnings should disappear

#### VS Code
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Python: Select Interpreter"
3. Choose the correct Python 3.8+ interpreter
4. Reload the window

#### Command Line Verification

The scripts will work correctly even with IDE warnings. To verify:

```bash
python3 --version  # Should show Python 3.8+
python3 -c "import argparse, json, sys; print('OK')"  # Should print "OK"
```

## Required vs Optional Dependencies

### Built-in (No Installation)
- `argparse` - Command-line argument parsing
- `json` - JSON data handling
- `sys` - System-specific parameters
- `datetime` - Date and time handling
- `typing` - Type hints
- `pathlib` - Path manipulation

### Required (Install with pip)
- `requests` - HTTP library for API calls
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `jinja2` - Template engine

### Optional (Install as needed)
- `yfinance` - Yahoo Finance data (for `fetch_financial_data.py` and `calculate_technical_indicators.py`)
- `alpha-vantage` - Alpha Vantage API (for `fetch_financial_data.py` with Alpha Vantage source)

## Installation Commands

### Minimal Installation
```bash
pip install requests pandas numpy jinja2
```

### Full Installation (with optional packages)
```bash
pip install -r requirements.txt
pip install yfinance alpha-vantage
```

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Troubleshooting

### Import Errors at Runtime

If you get import errors when running scripts:

1. **Check Python version**: `python --version` (must be 3.8+)
2. **Check installation**: `pip list | grep pandas`
3. **Reinstall if needed**: `pip install --upgrade pandas numpy requests jinja2`

### Scripts Don't Run

Make sure scripts are executable:
```bash
chmod +x *.py
```

Or run with Python explicitly:
```bash
python3 fetch_financial_data.py AAPL --source yahoo
```

## Testing Installation

Run this test script to verify all dependencies:

```bash
python3 -c "
import sys
modules = ['argparse', 'json', 'sys', 'datetime', 'typing', 'pathlib', 
           'requests', 'pandas', 'numpy', 'jinja2']
missing = []
for m in modules:
    try:
        __import__(m)
        print(f'✓ {m}')
    except ImportError:
        missing.append(m)
        print(f'✗ {m} - MISSING')

if missing:
    print(f'\nMissing modules: {missing}')
    print('Install with: pip install ' + ' '.join(missing))
    sys.exit(1)
else:
    print('\n✓ All dependencies installed!')
"
```

## Next Steps

After installation, see `README.md` for usage examples and script documentation.
