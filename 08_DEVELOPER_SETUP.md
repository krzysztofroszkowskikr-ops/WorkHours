# DEVELOPER SETUP GUIDE
## WorkHours Purple v1.0 - Local Development Environment

---

## 1. SYSTEM REQUIREMENTS

### Windows 10/11

```
OS: Windows 10 Pro or newer (or Windows 11)
RAM: 8GB minimum (16GB recommended for smooth Buildozer)
Disk: 25GB free (for SDK, NDK, tools)
Internet: Fast connection (initial setup downloads ~2GB)
```

**Required Software:**
- Python 3.11+ (https://python.org)
- Java JDK 11+ (https://adoptopenjdk.net)
- Android SDK (installed by buildozer)
- Git (for version control)

---

## 2. STEP 1: ENVIRONMENT SETUP

### 2.1 Clone Repository

```bash
# Navigate to your projects folder
cd D:\Projects  # Or your preferred location

# Clone the repository
git clone https://github.com/yourusername/workhours-app.git
cd workhours-app
```

### 2.2 Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Verify
python --version  # Should show 3.11+
```

### 2.3 Install Python Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "kivy|reportlab"
```

---

## 3. STEP 2: DATABASE SETUP

### 3.1 Create Database Directory

```bash
# From project root
mkdir -p user_data

# The app will create workhours.db here automatically
```

### 3.2 Initialize Database

```bash
# Run Python script to initialize
python -c "
from src.db.database import Database
db = Database('user_data/workhours.db')
db.initialize()
print('✓ Database initialized successfully')
"
```

---

## 4. STEP 3: PROJECT STRUCTURE

### 4.1 Create Folder Structure

```bash
# From project root - run once
mkdir -p src/db/migrations
mkdir -p src/models
mkdir -p src/repository
mkdir -p src/services
mkdir -p src/utils
mkdir -p src/ui/screens
mkdir -p src/ui/components
mkdir -p src/ui/themes
mkdir -p src/assets/icons
mkdir -p src/assets/fonts
mkdir -p tests/fixtures
mkdir -p docs
mkdir -p android/buildozer
mkdir -p .github/workflows
```

### 4.2 Verify Structure

```bash
# Check structure (from project root)
tree /F  # Windows
tree     # Linux/Mac

# Should show organized structure with all __init__.py files
```

---

## 5. STEP 4: RUNNING THE APP (Desktop)

### 5.1 Run Development Server

```bash
# From project root with venv activated
python main.py
```

**Expected Output:**
```
[INFO   ] Kivy version: 2.3.0
[INFO   ] Platform: windows
[INFO   ] OpenGL version: 4.6
[INFO   ] WorkHours Purple initialized
[INFO   ] Loading theme #1 (Dark Purple Neon)
[INFO   ] App started successfully
```

### 5.2 Troubleshooting Desktop Run

**Issue: "ModuleNotFoundError: No module named 'kivy'"**
```bash
# Solution: Ensure venv is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

**Issue: "Error: SDL2 not found"**
```bash
# Solution: Use pre-built wheels (usually handled by pip)
pip install kivy --upgrade --force-reinstall
```

**Issue: "OpenGL error"**
```bash
# Solution: Update GPU drivers or use software rendering
export KIVY_WINDOW=pygame  # Linux
set KIVY_WINDOW=pygame  # Windows
python main.py
```

---

## 6. STEP 5: ANDROID DEVELOPMENT (Optional)

### 6.1 Install Java JDK

**Windows:**
1. Download JDK 11+ from https://adoptopenjdk.net
2. Install to C:\Program Files\jdk-11
3. Set environment variable:
   - Right-click This PC → Properties
   - Advanced system settings
   - Environment Variables
   - New: `JAVA_HOME` = `C:\Program Files\jdk-11`

**Verify:**
```bash
java -version
javac -version
```

### 6.2 Install Buildozer

```bash
pip install buildozer cython
```

### 6.3 First APK Build (Debug)

```bash
# From project root
buildozer android debug

# First build takes 10-15 minutes (downloads SDK/NDK)
# Subsequent builds are faster
```

**Output:**
```
[INFO   ] Build done. Build file: bin/workhours-1.0.0-debug.apk
[INFO   ] Zip created: bin/workhours-1.0.0-debug.apk
```

### 6.4 Deploy to Device

**Option 1: USB Connection**
```bash
# Enable USB Debugging on device:
# Settings → About Phone → Build Number (tap 7 times)
# Settings → Developer Options → USB Debugging (ON)

# Connect device via USB
buildozer android debug deploy run
```

**Option 2: Android Emulator**
```bash
# Install Android Studio & setup emulator
# Run emulator first
buildozer android debug deploy run
```

---

## 7. STEP 6: TESTING

### 7.1 Install Test Dependencies

```bash
pip install pytest pytest-cov pytest-mock
```

### 7.2 Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calc_service.py

# Run with coverage report
pytest --cov=src --cov-report=html

# View coverage in browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
```

### 7.3 Code Quality

```bash
# Install tools
pip install black flake8 mypy

# Format code
black src/

# Check style
flake8 src/

# Type checking
mypy src/
```

---

## 8. IDE SETUP (VS Code)

### 8.1 Recommended Extensions

Install in VS Code:
- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Kivy** (BattleRoyalVS.kivy) - optional
- **Git History** (donjayamanne.githistory)
- **Python Docstring Generator** (njpwerner.autodocstring)

### 8.2 VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  },
  "python.analysis.typeCheckingMode": "strict",
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

### 8.3 Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: main.py",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "Python: pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "tests/",
        "-v"
      ],
      "console": "integratedTerminal"
    }
  ]
}
```

---

## 9. GIT WORKFLOW

### 9.1 Initial Setup

```bash
# Configure git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# From project root
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/workhours-app.git
git push -u origin main
```

### 9.2 Daily Development

```bash
# Before starting work
git pull origin main

# Create feature branch
git checkout -b feature/theme-system

# Make changes, commit frequently
git add src/ui/themes/
git commit -m "feat: add theme generator (Opcja B)"

# Push to GitHub
git push origin feature/theme-system

# Create Pull Request on GitHub
# After review and tests, merge to main
```

### 9.3 Useful Commands

```bash
# See changes
git status
git diff

# Undo changes
git restore <file>

# See history
git log --oneline
git log --graph --all

# Stash work in progress
git stash
git stash pop
```

---

## 10. DEVELOPMENT WORKFLOW

### 10.1 Daily Routine

```bash
# Morning: start work
venv\Scripts\activate
git pull origin main
git checkout -b feature/your-feature

# Develop
python main.py  # Test app locally

# Test
pytest

# Code quality
black src/
flake8 src/

# Commit
git add .
git commit -m "feat: description"
git push origin feature/your-feature

# Evening: create PR on GitHub
# (or merge if working alone)
```

### 10.2 Debugging Tips

```python
# Use print debugging
print(f"DEBUG: variable = {variable}")

# Use Python debugger
import pdb
pdb.set_trace()  # Code will pause here

# Or use breakpoints in VS Code
# Click left margin to set breakpoint
# Run with F5
```

### 10.3 Database Debugging

```bash
# Access SQLite directly
sqlite3 user_data/workhours.db

# Inside sqlite3 prompt
sqlite> .tables
sqlite> SELECT * FROM profiles;
sqlite> SELECT * FROM work_entries LIMIT 5;
sqlite> .exit
```

---

## 11. DOCUMENTATION

### 11.1 Generate API Docs

```bash
# Install pdoc
pip install pdoc

# Generate docs
pdoc -o docs/ src/

# Open in browser
start docs/index.html
```

### 11.2 Writing Code Comments

```python
# Good docstring example
def calculate_work_time(start: str, end: str, break_minutes: int) -> dict:
    """
    Calculate work time for a single day.
    
    Handles edge cases like midnight crossing and validates inputs.
    
    Args:
        start: Start time in HH:MM format (e.g., "08:30")
        end: End time in HH:MM format (e.g., "17:00")
        break_minutes: Break duration in minutes (e.g., 60)
    
    Returns:
        Dictionary with gross_minutes, net_minutes, is_valid, and errors.
    
    Example:
        >>> calculate_work_time('08:00', '17:00', 60)
        {'gross_minutes': 540, 'net_minutes': 480, 'is_valid': True}
    """
    pass
```

---

## 12. COMMON ISSUES & SOLUTIONS

| Issue | Solution |
|-------|----------|
| **venv not activated** | Run `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux) |
| **Module not found** | Ensure venv is activated and pip install completed |
| **Port 8000 in use** | Change port: `python main.py --port 8001` |
| **Database locked** | Check if app is running; kill process and restart |
| **Build fails** | Run `buildozer android clean` then `buildozer android debug` |
| **Tests fail** | Run `pytest -v` to see detailed error messages |
| **Git conflicts** | Use `git mergetool` or manually resolve in editor |

---

## 13. PERFORMANCE PROFILING

### 13.1 Profile Python Code

```python
# Use cProfile to find bottlenecks
import cProfile
import pstats

cProfile.run('calculate_month_summary(entries)', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(10)  # Top 10 functions
```

### 13.2 Memory Profiling

```bash
# Install memory_profiler
pip install memory-profiler

# Decorate functions
@profile
def my_function():
    pass

# Run
python -m memory_profiler script.py
```

---

## 14. CONTINUOUS LEARNING

### Resources:

- **Kivy Documentation**: https://kivy.org/doc/stable/
- **KivyMD Documentation**: https://kivymd.readthedocs.io/
- **Python Best Practices**: https://pep8.org/
- **Testing Guide**: https://docs.pytest.org/
- **Android Development**: https://developer.android.com/

### Community:

- **Kivy Discord**: https://discord.gg/kivy
- **Stack Overflow**: Tag `kivy`
- **Reddit**: r/kivy

---

## 15. CHECKLIST - NEW DEVELOPER SETUP

```bash
□ Clone repository
□ Create virtual environment
□ Install Python dependencies
□ Setup Java JDK (for Android)
□ Initialize database
□ Create project structure
□ Run app locally (python main.py)
□ Run tests (pytest)
□ Configure IDE (VS Code)
□ Test Android build (buildozer)
□ Setup Git & create first feature branch
□ Read documentation files (03_PROJECT_STRUCTURE.md, etc)
□ Ask questions in team chat!
```

---

## 16. ONBOARDING CHECKLIST (First Day)

1. **Setup complete?** → Run `python main.py` successfully
2. **Tests pass?** → Run `pytest` with all green ✅
3. **First PR?** → Create small feature branch (e.g., `docs/readme`)
4. **Code review?** → Have another dev review your code
5. **Merge main?** → First feature merged to main!

**Congratulations! 🎉 You're ready to develop!**

---

**NEXT & FINAL:** Summary & Implementation Roadmap
