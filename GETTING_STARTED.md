# 🚀 Getting Started Guide

Welcome to the **Electricity Consumption Prediction System**! This guide will help you get set up and running in minutes.

## ⚡ Quick 3-Step Setup

### Step 1: Install Dependencies (1 minute)
```bash
cd electricity_consumption_prediction
pip install -r requirements.txt
```

### Step 2: Validate Setup (30 seconds)
```bash
python setup_validation.py
```

Expected output:
```
✅ Successful checks: 25
🎉 All checks passed! System is ready to use.
```

### Step 3: Run the App (30 seconds)
```bash
streamlit run app.py
```

Then open: `http://localhost:8501`

---

## 📊 First Time Usage (5 minutes)

### Upload Dataset
1. In Streamlit, go to "📤 Data Upload & Preview"
2. Click "Browse files"
3. Select `household_power_consumption.txt`
4. Wait for confirmation ✅

### Preprocess Data
1. Go to "🔧 Data Preprocessing"
2. Keep default settings
3. Click "🔄 Start Preprocessing"
4. Wait for completion

### Train Model
1. Go to "🤖 Model Training"
2. Select "Random Forest" and "XGBoost"
3. Click "🚀 Train Selected Models"
4. View metrics when done

### View Results
1. Go to "🔮 Predictions"
2. Keep defaults and click "🔮 Generate Predictions"
3. Navigate to "📈 Results & Visualization"
4. View charts and download results

---

## 🎯 Common Workflows

### Workflow 1: Quick Evaluation
**Time: 10 minutes**
```
Data Upload → Preprocessing → Train 2 models → View metrics → Done
```

### Workflow 2: Model Comparison
**Time: 20 minutes**
```
Data Upload → Preprocessing → Train 5 models → Compare → Best model
```

### Workflow 3: Custom Configuration
**Time: 15 minutes**
```
Data Upload → Custom Preprocessing → Train with tuning → Export results
```

---

## 🔧 Troubleshooting

### Issue: "pip: command not found"
**Solution**: Install Python 3.8+ from python.org

### Issue: "ModuleNotFoundError"
**Solution**: Run setup_validation.py to check
```bash
python setup_validation.py
```

### Issue: Port 8501 already in use
**Solution**: Use different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: Data file too large
**Solution**: Normal for large datasets, app handles it
- You can sample the data in preprocessing

---

## 📚 Documentation Map

```
START HERE
    ↓
├─ 👋 This file (Getting Started)
│   ↓
├─ 🚀 QUICKSTART.md (5-minute demo)
│   ↓
├─ 📖 README.md (Full documentation)
│   ↓
├─ 🔧 IMPLEMENTATION.md (Technical details)
│   ↓
└─ 📚 examples/README.md (Code examples)
```

---

## 🎓 Learning Paths

### Path 1: Beginner (30 minutes)
1. ✅ This guide
2. ✅ QUICKSTART.md
3. ✅ Run example_1_basic_usage.py
4. ✅ Open Streamlit app

### Path 2: Intermediate (1-2 hours)
1. ✅ All beginner materials
2. ✅ README.md (full)
3. ✅ Run all examples (1-4)
4. ✅ Experiment with parameters

### Path 3: Advanced (3+ hours)
1. ✅ All intermediate materials
2. ✅ IMPLEMENTATION.md
3. ✅ Study source code
4. ✅ Create custom configurations

---

## 🛠️ System Requirements

### Minimum
- Python 3.8
- 2 GB RAM
- 500 MB disk space
- Internet (for initial setup)

### Recommended
- Python 3.9+
- 4 GB RAM
- 1 GB disk space
- Latest pip/conda

### Supported OS
- ✅ Windows
- ✅ macOS
- ✅ Linux

---

## 📦 Installation Options

### Option 1: pip (Recommended)
```bash
pip install -r requirements.txt
```

### Option 2: conda
```bash
conda create -n electricity python=3.9
conda activate electricity
pip install -r requirements.txt
```

### Option 3: Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Streamlit works: `streamlit --version`
- [ ] Dependencies OK: `python setup_validation.py`
- [ ] App runs: `streamlit run app.py`
- [ ] Browser opens: `http://localhost:8501`
- [ ] Data file exists: `household_power_consumption.txt`

---

## 🚀 Quick Examples

### Run Example 1 (Basic)
```bash
python examples/example_1_basic_usage.py
```
Takes ~3 minutes, shows basic workflow

### Run Example 3 (All Models)
```bash
python examples/example_3_all_models_comparison.py
```
Takes ~15 minutes, compares all 5 models

### Run Validation
```bash
python setup_validation.py
```
Takes ~30 seconds, checks everything

---

## 🎯 What You Can Do

After setup, you can:

✅ **Upload** electricity consumption data (CSV format)  
✅ **Preprocess** data with multiple strategies  
✅ **Train** 5 different ML models  
✅ **Compare** model performance  
✅ **Generate** predictions for future dates  
✅ **Visualize** results with interactive charts  
✅ **Export** predictions as CSV  
✅ **Download** detailed reports  

---

## 📞 Getting Help

### If something doesn't work:

1. **Check validation**
   ```bash
   python setup_validation.py
   ```

2. **Review logs**
   ```bash
   tail -f logs/app.log
   ```

3. **Read documentation**
   - README.md (full guide)
   - IMPLEMENTATION.md (technical)
   - examples/README.md (code examples)

4. **Try example**
   ```bash
   python examples/example_1_basic_usage.py
   ```

---

## 🎉 You're Ready!

```
✅ Setup complete
✅ Dependencies installed
✅ System validated
✅ Ready to use!

Next: Run 'streamlit run app.py'
```

---

## 🔗 Useful Resources

### Official Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [Scikit-learn Guide](https://scikit-learn.org)
- [XGBoost Docs](https://xgboost.readthedocs.io)
- [TensorFlow/Keras](https://tensorflow.org)

### Tutorials
- [Machine Learning Basics](https://scikit-learn.org/stable/tutorial)
- [Time Series Forecasting](https://en.wikipedia.org/wiki/Time_series)
- [Streamlit Tutorial](https://docs.streamlit.io/library/get-started)

### Community
- Stack Overflow (tag: machine-learning)
- GitHub Issues (contribute/report bugs)
- Kaggle (find similar projects)

---

## 🎓 Next Steps

1. **Run the app**: `streamlit run app.py`
2. **Explore examples**: Run example scripts
3. **Read documentation**: Start with README.md
4. **Build projects**: Use the library for your own work
5. **Contribute**: Improve the project

---

## 📝 Tips for Success

1. **Start simple**: Try one model first
2. **Understand data**: Check dataset statistics
3. **Compare results**: Try different approaches
4. **Optimize gradually**: Fine-tune parameters
5. **Save results**: Export and document findings

---

## ⏱️ Timeline

| Step | Time | Action |
|------|------|--------|
| Setup | 1 min | `pip install -r requirements.txt` |
| Validate | 1 min | `python setup_validation.py` |
| Learn | 5 min | Read QUICKSTART.md |
| Run App | 30 sec | `streamlit run app.py` |
| Upload Data | 1 min | Use file uploader |
| Preprocess | 1 min | Click preprocess button |
| Train | 5 min | Train 2-3 models |
| Visualize | 2 min | View results |
| **TOTAL** | **~15 min** | **Ready to use!** |

---

## 💡 Pro Tips

1. **Use keyboard shortcuts in Streamlit**: 'R' to rerun, 'C' to clear cache
2. **Save results**: Download CSV after each prediction
3. **Document settings**: Note which settings work best
4. **Start with small data**: Test with fewer rows first
5. **Compare models**: Always try multiple algorithms

---

**Congratulations! You're all set to use the Electricity Consumption Prediction System! 🎉**

For detailed information, see README.md or QUICKSTART.md.

---

**Questions?** Check troubleshooting section or review documentation files.

**Ready to start?** Run: `streamlit run app.py` 🚀
