"""
Setup Validation Script
Verifies that all dependencies are installed and the system is ready
"""

import sys
import importlib
import os
from pathlib import Path

class SetupValidator:
    """Validate project setup and dependencies"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🔍 Checking Python version...", end=" ")
        
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
            self.success_count += 1
        else:
            error = f"❌ Python {version.major}.{version.minor} - Need 3.8+"
            print(error)
            self.errors.append(error)
    
    def check_package(self, package_name, import_name=None):
        """Check if a package is installed"""
        if import_name is None:
            import_name = package_name
        
        print(f"🔍 Checking {package_name}...", end=" ")
        
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {version}")
            self.success_count += 1
            return True
        except ImportError:
            error = f"❌ {package_name} not found"
            print(error)
            self.errors.append(error)
            return False
    
    def check_packages(self):
        """Check all required packages"""
        print("\n📦 Checking Required Packages:")
        print("=" * 50)
        
        required = {
            'streamlit': 'streamlit',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'scikit-learn': 'sklearn',
            'xgboost': 'xgboost',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'plotly': 'plotly',
        }
        optional = {
            'tensorflow': 'tensorflow',
        }
        
        for package, import_name in required.items():
            self.check_package(package, import_name)
        
        for package, import_name in optional.items():
            self.check_optional_package(package, import_name)
    
    def check_file_structure(self):
        """Check if required files exist"""
        print("\n📁 Checking File Structure:")
        print("=" * 50)
        
        required_files = {
            'app.py': 'Main Streamlit application',
            'config.py': 'Configuration file',
            'requirements.txt': 'Dependencies file',
            'README.md': 'README documentation',
            'QUICKSTART.md': 'Quick start guide',
            'IMPLEMENTATION.md': 'Implementation details',
            'PROJECT_CHECKLIST.md': 'Project checklist',
            'utils/__init__.py': 'Utils package',
            'utils/logger.py': 'Logger module',
            'utils/data_processor.py': 'Data processor module',
            'utils/model_trainer.py': 'Model trainer module',
            'utils/model_evaluator.py': 'Model evaluator module',
            'examples/__init__.py': 'Examples package',
            'examples/example_1_basic_usage.py': 'Example 1',
            'examples/example_2_preprocessing_strategies.py': 'Example 2',
            'examples/example_3_all_models_comparison.py': 'Example 3',
            'examples/example_4_advanced_usage.py': 'Example 4',
            'examples/README.md': 'Examples documentation',
        }
        
        for file_path, description in required_files.items():
            print(f"🔍 Checking {description}...", end=" ")
            
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ ({size} bytes)")
                self.success_count += 1
            else:
                error = f"❌ {file_path} not found"
                print(error)
                self.errors.append(error)
    
    def check_data_file(self):
        """Check if dataset exists"""
        print("\n📊 Checking Data Files:")
        print("=" * 50)
        
        data_path = 'household_power_consumption.txt/household_power_consumption.txt'
        print(f"🔍 Checking dataset...", end=" ")
        
        if os.path.exists(data_path):
            size = os.path.getsize(data_path)
            size_mb = size / (1024 * 1024)
            print(f"✅ ({size_mb:.1f} MB)")
            self.success_count += 1
        else:
            warning = f"⚠️  Dataset not found at {data_path}"
            print(warning)
            self.warnings.append(warning)
    
    def check_directories(self):
        """Check if required directories exist"""
        print("\n📂 Checking Directories:")
        print("=" * 50)
        
        required_dirs = {
            'utils': 'Utilities',
            'examples': 'Examples',
        }
        
        for dir_name, description in required_dirs.items():
            print(f"🔍 Checking {description} directory...", end=" ")
            
            if os.path.isdir(dir_name):
                print(f"✅")
                self.success_count += 1
            else:
                error = f"❌ {dir_name}/ directory not found"
                print(error)
                self.errors.append(error)
    
    def check_optional_package(self, package_name, import_name=None):
        """Check if an optional package is installed"""
        if import_name is None:
            import_name = package_name
        
        print(f"🔍 Checking optional {package_name}...", end=" ")
        
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {version}")
            self.success_count += 1
            return True
        except ImportError:
            warning = f"⚠️ Optional package {package_name} not found. LSTM will be disabled."
            print(warning)
            self.warnings.append(warning)
            return False
    
    def test_imports(self):
        """Test if modules can be imported"""
        print("\n🔧 Testing Module Imports:")
        print("=" * 50)
        
        modules_to_test = [
            ('config', 'Configuration module'),
            ('utils.logger', 'Logger module'),
            ('utils.data_processor', 'Data processor'),
            ('utils.model_trainer', 'Model trainer'),
            ('utils.model_evaluator', 'Model evaluator'),
        ]
        
        for module_name, description in modules_to_test:
            print(f"🔍 Importing {description}...", end=" ")
            
            try:
                importlib.import_module(module_name)
                print(f"✅")
                self.success_count += 1
            except Exception as e:
                error = f"❌ Error: {str(e)[:50]}"
                print(error)
                self.errors.append(f"{module_name}: {str(e)}")
    
    def test_streamlit(self):
        """Test if Streamlit can be run"""
        print("\n🌐 Testing Streamlit:")
        print("=" * 50)
        
        print("🔍 Checking Streamlit installation...", end=" ")
        
        try:
            import streamlit
            print(f"✅")
            self.success_count += 1
            
            print("🔍 Testing Streamlit app file...", end=" ")
            if os.path.exists('app.py'):
                print(f"✅")
                self.success_count += 1
            else:
                print(f"❌")
                self.errors.append("app.py not found")
        
        except Exception as e:
            error = f"❌ {str(e)}"
            print(error)
            self.errors.append(error)
    
    def run_all_checks(self):
        """Run all validation checks"""
        print("\n" + "=" * 60)
        print("⚡ ELECTRICITY CONSUMPTION PREDICTION - SETUP VALIDATION")
        print("=" * 60)
        
        self.check_python_version()
        self.check_packages()
        self.check_file_structure()
        self.check_data_file()
        self.check_directories()
        self.test_imports()
        self.test_streamlit()
        
        self.print_summary()
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 60)
        print("📋 VALIDATION SUMMARY")
        print("=" * 60)
        
        print(f"\n✅ Successful checks: {self.success_count}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        print("\n" + "=" * 60)
        
        if not self.errors:
            print("🎉 All checks passed! System is ready to use.")
            print("\n📖 Next steps:")
            print("   1. Run: streamlit run app.py")
            print("   2. Visit: http://localhost:8501")
            print("   3. Upload your electricity consumption data")
            print("\n📚 For examples, run:")
            print("   python examples/example_1_basic_usage.py")
            print("   python examples/example_2_preprocessing_strategies.py")
            print("   python examples/example_3_all_models_comparison.py")
            print("   python examples/example_4_advanced_usage.py")
        else:
            print("❌ Setup validation failed. Please fix the errors above.")
            print("\n💡 Common fixes:")
            print("   1. Install dependencies: pip install -r requirements.txt")
            print("   2. Update pip: pip install --upgrade pip")
            print("   3. Check Python version: python --version (need 3.8+)")
        
        print("\n" + "=" * 60)
        
        return len(self.errors) == 0

def main():
    """Main validation entry point"""
    validator = SetupValidator()
    success = validator.run_all_checks()
    
    # Exit with proper code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
