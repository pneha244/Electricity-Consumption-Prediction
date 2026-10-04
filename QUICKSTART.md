# 🚀 Quick Start Guide

Get up and running with Electricity Consumption Prediction in 5 minutes!

## ⚡ 1-Minute Setup

### Step 1: Install Dependencies
```bash
cd electricity_consumption_prediction
pip install -r requirements.txt
```

**What it does**: Installs all required Python packages (Streamlit, ML libraries, visualization tools)

### Step 2: Run the App
```bash
streamlit run app.py
```

**What it does**: Starts the web application on `http://localhost:8501`

### Step 3: Open in Browser
Navigate to: `http://localhost:8501`

**Result**: You should see the Electricity Consumption Prediction dashboard

---

## 📊 5-Minute Demo

### Scenario: Predict electricity consumption for next 30 days

#### Step 1: Upload Dataset (30 seconds)
1. Click "📤 Data Upload & Preview" in sidebar
2. Click "Browse files" button
3. Select `household_power_consumption.txt`
4. Wait for upload confirmation ✅

**Expected**: Dataset preview with statistics

#### Step 2: Preprocess Data (1 minute)
1. Navigate to "🔧 Data Preprocessing"
2. Keep default settings:
   - Missing Values: `forward_fill`
   - Outlier Detection: ✓
   - Scaling Method: `standard`
3. Click "🔄 Start Preprocessing"
4. Wait for completion

**Expected**: Green checkmark ✅ and preprocessing report

#### Step 3: Train Model (1.5 minutes)
1. Go to "🤖 Model Training"
2. Select models (default: Random Forest, XGBoost)
3. Click "🚀 Train Selected Models"
4. Wait for training to complete

**Expected**: Model metrics for each trained model

#### Step 4: Make Predictions (30 seconds)
1. Navigate to "🔮 Predictions"
2. Keep default settings:
   - Model: Select any trained model
   - Forecast Days: 30
   - Date Range: Auto-populated
3. Click "🔮 Generate Predictions"

**Expected**: Table with predicted consumption values

#### Step 5: View Results (1 minute)
1. Go to "📈 Results & Visualization"
2. Check tabs:
   - **Forecast Chart**: Line graph of predictions
   - **Model Comparison**: Bar chart of metrics
   - **Trend Analysis**: Consumption trend over time
   - **Export**: Download as CSV

**Expected**: Interactive charts and download options

---

## 🎯 Common Tasks

### Task 1: Compare Different Models

```
1. Train Tab → Select 5 models → Train
2. Predictions Tab → Try each model → Compare metrics
3. Results Tab → View comparison chart
```

### Task 2: Export Forecast Data

```
1. Predictions Tab → Generate predictions
2. Results Tab → Export Tab
3. Click "📥 Download Forecast as CSV"
```

### Task 3: Change Preprocessing Strategy

```
1. Data Preprocessing Tab
2. Change settings:
   - Missing Values: interpolate
   - Outlier Detection: toggle
   - Scaling: minmax or robust
3. Click "🔄 Start Preprocessing"
```

---

## 💡 Tips & Tricks

### Tip 1: Best Model for Quick Results
```
Fastest: Linear Regression
Best Accuracy: XGBoost or LSTM
Balanced: Random Forest
```

### Tip 2: Date Range Selection
- **Short term (7-14 days)**: All models work well
- **Medium term (30-90 days)**: Random Forest, XGBoost
- **Long term (180+ days)**: LSTM, Gradient Boosting

### Tip 3: Improving Model Performance
```
1. Check data preprocessing (remove noise)
2. Try different algorithms
3. Adjust date range
4. Consider seasonal patterns
```

### Tip 4: File Format Issues
If you get an error uploading:
- Ensure CSV file with comma or semicolon delimiter
- Check for missing date/time columns
- Verify numeric values (no text in data)

---

## 📚 Understanding the UI

### Dashboard (📊)
- **Overview**: Project status and progress
- **AC Status**: Acceptance criteria checklist
- **Quick Start**: Navigation guide

### Data Upload (📤)
- **Upload**: Select CSV/TXT file
- **Preview**: First 20 rows
- **Info**: Column types and counts
- **Statistics**: Min, max, mean, std
- **Missing Values**: Count and percentage

### Preprocessing (🔧)
- **Configuration**: Choose strategies
- **Missing Strategy**: 
  - `forward_fill`: Repeat previous value
  - `interpolate`: Linear interpolation
  - `mean`: Fill with column mean
- **Outlier Detection**: IQR method
- **Scaling**: Normalize values

### Model Training (🤖)
- **Selection**: Choose algorithms
- **Parameters**: Test size, random state
- **Output**: Metrics (MAE, RMSE, R²)

### Predictions (🔮)
- **Model**: Select trained model
- **Period**: Days to forecast
- **Dates**: Start and end dates
- **Output**: Prediction table

### Results (📈)
- **Charts**: Interactive visualizations
- **Metrics**: Performance comparison
- **Trends**: Consumption patterns
- **Export**: Download options

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't start | Run: `pip install streamlit` |
| Upload fails | Check file format (CSV/TXT) |
| Training error | Ensure data is preprocessed first |
| Slow performance | Use smaller date ranges |
| Missing metrics | Check model training completed |

---

## 📊 Sample Data Format

Your CSV should look like:

```
Date,Time,Global_active_power,Global_reactive_power,Voltage,Global_intensity
16/12/2006,17:24:00,4.216,0.418,234.84,18.4
16/12/2006,17:25:00,5.36,0.436,233.63,23.0
16/12/2006,17:26:00,5.374,0.498,233.29,23.0
```

**Required Columns**: Date, Time, and at least one consumption metric

---

## ⏱️ Typical Execution Times

| Task | Time |
|------|------|
| Upload Data | <5 sec |
| Preprocess | 10-30 sec |
| Train (Single Model) | 5-60 sec |
| Train (All 5 Models) | 2-5 min |
| Generate Predictions | <5 sec |
| Generate Report | <5 sec |

---

## 🎓 What's Happening Behind the Scenes

### Data Preprocessing
```
Raw Data
  ↓ Parse Date/Time
  ↓ Handle Missing Values
  ↓ Detect Outliers
  ↓ Select Numeric Features
  ↓ Scale Values
Clean Data ✓
```

### Model Training
```
Clean Data
  ↓ Create Lagged Features
  ↓ Split Train/Test (80/20)
  ↓ Train Selected Models
  ↓ Generate Predictions
  ↓ Calculate Metrics
Models Ready ✓
```

### Prediction Generation
```
Trained Model
  ↓ Prepare Test Data
  ↓ Generate Forecasts
  ↓ Create Date Range
  ↓ Format Results
Predictions Ready ✓
```

---

## 🎯 Next Steps

After 5-minute demo:

1. **Explore**: Try different models and settings
2. **Analyze**: Study the generated metrics
3. **Customize**: Read IMPLEMENTATION.md for details
4. **Optimize**: Fine-tune parameters for better results

---

## 📖 Learn More

- **README.md**: Comprehensive documentation
- **IMPLEMENTATION.md**: Technical details
- **config.py**: Configuration options
- **utils/**: Source code for ML models

---

## ✅ Checklist

- [ ] Dependencies installed
- [ ] App runs successfully
- [ ] Data uploaded
- [ ] Preprocessing complete
- [ ] Model trained
- [ ] Predictions generated
- [ ] Results visualized
- [ ] Data exported

**All done? 🎉 You're ready to use Electricity Consumption Prediction!**

---

## 🆘 Need Help?

1. **Check logs**: `logs/app.log`
2. **Review errors**: Error messages in UI
3. **Read docs**: README.md and IMPLEMENTATION.md
4. **Check data**: Ensure proper CSV format
5. **Try again**: Restart app with `streamlit run app.py`

---

**Happy Predicting! ⚡**
