# ⚡ Electricity Consumption Prediction System

A comprehensive Machine Learning and Streamlit-based application for predicting household electricity consumption patterns using advanced algorithms and interactive visualization.

## 🎯 Project Overview

This project implements a complete end-to-end solution for predicting electricity consumption using multiple machine learning algorithms. It features an interactive Streamlit UI with dataset upload, data preprocessing, model training, prediction generation, and comprehensive visualization.

### Key Features

- 📊 **Dataset Upload**: Upload electricity consumption data in CSV format
- 🔧 **Data Preprocessing**: Automatic cleaning, missing value handling, and outlier detection
- 🤖 **Multiple ML Models**:
  - Linear Regression
  - Random Forest Regressor
  - XGBoost Regressor
  - Gradient Boosting Regressor
  - LSTM (Deep Learning)
- 🔮 **Prediction Engine**: Generate forecasts for any date range
- 📈 **Interactive Visualizations**: Real-time charts and trend analysis
- 📥 **Export Functionality**: Download predictions as CSV or detailed reports
- 🎓 **Model Evaluation**: MAE, RMSE, R² Score, and MAPE metrics

## 📋 Acceptance Criteria

- ✅ **AC1**: Dataset upload in CSV format
- ✅ **AC2**: Automatic data cleaning and preprocessing
- ✅ **AC3**: Multiple algorithm selection
- ✅ **AC4**: Forecast generation from historical data
- ✅ **AC5**: Date-based prediction range
- ✅ **AC6**: Multiple visualization types
- ✅ **AC7**: Comprehensive model evaluation metrics
- ✅ **AC8**: Export results functionality
- ✅ **AC9**: Error handling and validation

## 📁 Project Structure

```
electricity_consumption_prediction/
├── app.py                              # Main Streamlit application
├── config.py                           # Configuration settings
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
├── QUICKSTART.md                       # Quick start guide
├── IMPLEMENTATION.md                   # Implementation details
├── household_power_consumption.txt/    # Dataset directory
│   └── household_power_consumption.txt # Raw dataset
├── utils/                              # Utility modules
│   ├── __init__.py
│   ├── logger.py                       # Logging configuration
│   ├── data_processor.py               # Data preprocessing
│   ├── model_trainer.py                # Model training
│   └── model_evaluator.py              # Model evaluation
├── logs/                               # Application logs
├── models/                             # Trained model storage
└── reports/                            # Generated reports
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

1. **Clone/Extract the project**
   ```bash
   cd electricity_consumption_prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   ```
   http://localhost:8501
   ```

## 📖 Usage Guide

### Step 1: Upload Dataset
- Navigate to "📤 Data Upload & Preview"
- Click on file uploader
- Select your electricity consumption CSV file
- View dataset statistics and preview

### Step 2: Preprocess Data
- Go to "🔧 Data Preprocessing"
- Configure preprocessing parameters:
  - Missing values strategy (forward fill, mean, interpolate)
  - Outlier detection
  - Scaling method (standard, minmax, robust)
- Click "🔄 Start Preprocessing"

### Step 3: Train Models
- Navigate to "🤖 Model Training"
- Select models to train (multiple selection)
- Configure training parameters
- Click "🚀 Train Selected Models"

### Step 4: Generate Predictions
- Go to "🔮 Predictions"
- Select trained model
- Set forecast period (days)
- Choose date range
- Click "🔮 Generate Predictions"

### Step 5: View Results
- Navigate to "📈 Results & Visualization"
- View forecast charts
- Compare model performance
- Analyze consumption trends
- Download results

## 🎓 Algorithms Explained

### Linear Regression
- **Use Case**: Quick baseline predictions
- **Pros**: Fast, interpretable
- **Cons**: Assumes linear relationship
- **Best For**: Trending data

### Random Forest
- **Use Case**: General-purpose predictions
- **Pros**: Handles non-linear patterns, robust
- **Cons**: Slower training
- **Best For**: Complex patterns

### XGBoost
- **Use Case**: High-performance predictions
- **Pros**: State-of-the-art performance
- **Cons**: Hyperparameter tuning needed
- **Best For**: Kaggle competitions

### Gradient Boosting
- **Use Case**: Sequential error correction
- **Pros**: Excellent accuracy
- **Cons**: Risk of overfitting
- **Best For**: Production systems

### LSTM
- **Use Case**: Temporal dependency modeling
- **Pros**: Captures long-term patterns
- **Cons**: Requires more data
- **Best For**: Time series with patterns

## 📊 Evaluation Metrics

### MAE (Mean Absolute Error)
- Average absolute difference between predicted and actual
- **Interpretation**: Lower is better
- **Units**: Same as target variable

### RMSE (Root Mean Squared Error)
- Square root of average squared errors
- **Interpretation**: Penalizes larger errors more
- **Units**: Same as target variable

### R² Score
- Coefficient of determination (0-1)
- **Interpretation**: 1 is perfect fit, 0 is poor fit
- **Formula**: 1 - (SS_res / SS_tot)

### MAPE (Mean Absolute Percentage Error)
- Percentage error between predicted and actual
- **Interpretation**: Lower percentage is better
- **Formula**: (1/n) × Σ(|actual - predicted| / |actual|) × 100

## 🔧 Configuration

Edit `config.py` to customize:

```python
CONFIG = {
    'models': {
        'random_forest': {
            'n_estimators': 100,
            'max_depth': 20,
            # ... other parameters
        },
        # ... other models
    },
    'preprocessing': {
        'missing_value_threshold': 0.5,
        'outlier_threshold': 3,
    },
    'paths': {
        'data': 'household_power_consumption.txt',
        'logs': 'logs/',
        'models': 'models/',
    }
}
```

## 📝 Data Format

Expected CSV format with columns like:
- `Date`: YYYY-MM-DD format
- `Time`: HH:MM:SS format
- `Global_active_power`: Watt-hour (numeric)
- `Global_reactive_power`: Watt-hour (numeric)
- Other consumption metrics (numeric)

## 🛠️ Advanced Features

### Custom Preprocessing
Modify `utils/data_processor.py` for custom preprocessing logic:
```python
processor = DataProcessor(
    missing_strategy='interpolate',
    outlier_detection=True,
    scaling_method='robust'
)
```

### Model Hyperparameters
Adjust model parameters in `config.py`:
```python
'xgboost': {
    'n_estimators': 200,
    'max_depth': 8,
    'learning_rate': 0.05,
}
```

### Custom Metrics
Add new evaluation metrics in `utils/model_evaluator.py`:
```python
def _calculate_custom_metric(self, y_true, y_pred):
    # Your metric calculation
    return metric_value
```

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web UI framework |
| pandas | 2.0.3 | Data manipulation |
| scikit-learn | 1.3.0 | ML algorithms |
| xgboost | 2.0.0 | XGBoost model |
| tensorflow | 2.13.0 | LSTM model |
| plotly | 5.16.1 | Interactive charts |
| numpy | 1.24.3 | Numerical computing |

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution**: Install missing packages
```bash
pip install -r requirements.txt --upgrade
```

### Issue: File too large error
**Solution**: The dataset file is >50MB
- This is normal for large datasets
- The application handles it automatically

### Issue: Memory error during training
**Solution**: 
- Reduce dataset size
- Lower batch size in config
- Use sampling for preprocessing

### Issue: Poor model performance
**Solution**:
- Check data quality and preprocessing
- Try different models
- Adjust hyperparameters
- Ensure sufficient data

## 📊 Example Results

### Sample Model Performance
```
Random Forest:
  MAE:  120.45
  RMSE: 180.32
  R²:   0.8534
  MAPE: 5.23%

XGBoost:
  MAE:  115.23
  RMSE: 172.10
  R²:   0.8712
  MAPE: 4.89%

LSTM:
  MAE:  110.50
  RMSE: 165.40
  R²:   0.8890
  MAPE: 4.45%
```

## 🎯 Best Practices

1. **Data Quality**: Ensure clean, consistent data before uploading
2. **Preprocessing**: Always preprocess before training
3. **Model Selection**: Start with simple models, move to complex
4. **Evaluation**: Use multiple metrics for comprehensive evaluation
5. **Hyperparameter Tuning**: Fine-tune parameters for better results
6. **Cross-validation**: Use train-test split to avoid overfitting

## 🔒 Data Privacy

- All data processing happens locally
- No data is stored permanently
- Files are processed in-memory
- No external API calls

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional algorithms (SVR, neural networks)
- Real-time data integration
- Model persistence and loading
- API integration
- Mobile app

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review IMPLEMENTATION.md for technical details
3. Check logs in `logs/` directory

## 🎓 Learning Resources

- [Scikit-learn Documentation](https://scikit-learn.org)
- [XGBoost Documentation](https://xgboost.readthedocs.io)
- [Streamlit Documentation](https://docs.streamlit.io)
- [TensorFlow/Keras Guide](https://www.tensorflow.org/guide)
- [Time Series Forecasting](https://en.wikipedia.org/wiki/Time_series)

## 📝 Changelog

### Version 1.0.0 (Initial Release)
- Core Streamlit application
- 5 ML algorithms
- Data preprocessing pipeline
- Model evaluation
- Interactive visualization
- Export functionality

---

**Last Updated**: 2024
**Version**: 1.0.0
