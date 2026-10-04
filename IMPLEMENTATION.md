# 📖 Implementation Details

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                          │
│                      (app.py)                                │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐    ┌──────────────┐  ┌──────────────┐
   │  Data   │    │    Model     │  │   Results   │
   │Processor│    │   Trainer    │  │  Evaluator  │
   └────┬────┘    └──────┬───────┘  └──────┬───────┘
        │                │                │
        │                └────────┬────────┘
        │                         │
        └────────────────┬────────┘
                         │
               ┌─────────▼────────┐
               │  Trained Models  │
               │  (in Memory)     │
               └──────────────────┘
```

---

## Core Modules

### 1. app.py - Main Streamlit Application

**Purpose**: Web interface and user interaction

**Key Features**:
- Session state management
- Multi-page navigation
- Interactive forms
- Real-time visualizations
- File upload handling

**Flow**:
```
1. Initialize session state
2. Load page configuration
3. Display navigation sidebar
4. Render selected page
5. Handle user interactions
6. Update visualizations
```

**Session State Variables**:
```python
st.session_state = {
    'data': None,                    # Uploaded raw data
    'processed_data': None,          # Preprocessed data
    'trained_models': {},            # Trained model objects
    'predictions': None,             # Generated predictions
    'model_metrics': {}              # Model evaluation metrics
}
```

---

### 2. config.py - Configuration Management

**Purpose**: Centralized configuration for all models and parameters

**Structure**:
```python
CONFIG = {
    'models': {
        'linear_regression': {...},
        'random_forest': {...},
        'xgboost': {...},
        'gradient_boosting': {...},
        'lstm': {...}
    },
    'preprocessing': {...},
    'paths': {...},
    'logging': {...},
    'metrics': [...]
}
```

**Model Configuration Example**:
```python
'random_forest': {
    'n_estimators': 100,          # Number of trees
    'max_depth': 20,              # Tree depth
    'min_samples_split': 5,       # Min samples to split
    'min_samples_leaf': 2,        # Min samples in leaf
    'random_state': 42,           # Reproducibility
    'n_jobs': -1                  # Parallel processing
}
```

**Customization**:
Modify values to tune model performance:
- Increase `n_estimators` for better accuracy (slower)
- Decrease `max_depth` to prevent overfitting
- Adjust learning_rate for gradient-based models

---

### 3. utils/data_processor.py - Data Preprocessing

**Purpose**: Clean and prepare data for ML models

**Pipeline**:

#### Step 1: Parse DateTime
```python
def _parse_datetime(self, data):
    # Combine Date and Time columns
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    # Set as index for time series operations
    data.set_index('DateTime', inplace=True)
```

#### Step 2: Handle Missing Values

**Strategies**:

1. **Forward Fill**: Repeat last known value
```python
data.fillna(method='ffill')
# Good for: Stable measurements
```

2. **Backward Fill**: Use next known value
```python
data.fillna(method='bfill')
# Good for: Recent data estimation
```

3. **Mean Imputation**: Fill with column mean
```python
SimpleImputer(strategy='mean').fit_transform(data)
# Good for: Random missingness
```

4. **Interpolation**: Linear interpolation
```python
data.interpolate(method='linear')
# Good for: Trending data
```

#### Step 3: Outlier Detection

**Method**: Interquartile Range (IQR)

```python
Q1 = data[col].quantile(0.25)      # 25th percentile
Q3 = data[col].quantile(0.75)      # 75th percentile
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Values outside bounds are outliers
outliers = (data[col] < lower_bound) | (data[col] > upper_bound)
```

**Action**: Replace with median value

#### Step 4: Feature Selection

```python
# Keep only numerical columns
data = data.select_dtypes(include=[np.number])
```

**Why**: ML models need numerical inputs

#### Step 5: Feature Scaling

**Methods**:

1. **StandardScaler**: (X - mean) / std
```python
# Centers at 0, std of 1
# Good for: Normal distribution
# Range: -infinity to +infinity
```

2. **MinMaxScaler**: (X - min) / (max - min)
```python
# Centers at 0.5, range 0-1
# Good for: Bounded features
# Range: 0 to 1
```

3. **RobustScaler**: (X - median) / IQR
```python
# Robust to outliers
# Good for: Data with outliers
# Range: -infinity to +infinity
```

**Output**: Normalized data ready for ML

---

### 4. utils/model_trainer.py - Model Training

**Purpose**: Train ML models and generate predictions

**Data Preparation**:

```python
def _create_lagged_features(self, data, lag=5):
    """
    Create sequence features for time series
    
    Input: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Lag=5:
    X = [[1,2,3,4,5], [2,3,4,5,6], ...]
    y = [6, 7, 8, ...]
    
    Why: ML models need input-output pairs
    """
```

**Train/Test Split**:
```python
X_train (80%) → Training data
X_test (20%)  → Validation data

This prevents data leakage and ensures fair evaluation
```

**Model Training Details**:

#### Linear Regression
```python
model = LinearRegression()
model.fit(X_train, y_train)

# Formula: y = mx + b
# Finds best-fit line through data
```

**Parameters**: None (simple model)

**Pros**:
- Fast training
- Interpretable coefficients
- Good for linear trends

**Cons**:
- Assumes linear relationship
- Poor with complex patterns

---

#### Random Forest
```python
model = RandomForestRegressor(
    n_estimators=100,     # 100 decision trees
    max_depth=20,         # Max tree depth
    min_samples_split=5   # Min samples to split
)
```

**How it works**:
1. Create multiple decision trees
2. Train each on random data samples
3. Average predictions from all trees

**Advantages**:
- Handles non-linear patterns
- Robust to outliers
- Feature importance available

**Disadvantages**:
- Slower than linear regression
- Risk of overfitting if too deep

---

#### XGBoost
```python
model = XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)
```

**How it works**:
1. Train first tree on data
2. Calculate residuals (errors)
3. Train next tree to predict residuals
4. Repeat process
5. Sum all tree predictions

**Key Parameters**:
- `learning_rate`: How much each tree contributes (0.01-0.3)
- `max_depth`: Tree complexity (3-10)
- `n_estimators`: Number of trees

**Advantages**:
- State-of-the-art performance
- Fast training
- Handles missing values

**Disadvantages**:
- Complex hyperparameter tuning
- Risk of overfitting

---

#### Gradient Boosting
```python
model = GradientBoostingRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1
)
```

**How it works**:
- Similar to XGBoost but using gradient descent
- Each tree predicts residuals
- Combines weak learners into strong ensemble

**Key Differences from XGBoost**:
- Uses gradient information
- Slower but more interpretable
- Better for smaller datasets

---

#### LSTM (Long Short-Term Memory)
```python
model = Sequential([
    LSTM(50, activation='relu', input_shape=(lag, 1)),
    Dropout(0.2),
    Dense(25, activation='relu'),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer=Adam(), loss='mse')
model.fit(X_train, y_train, epochs=50, batch_size=32)
```

**Architecture**:
```
Input Layer (sequences)
    ↓
LSTM Layer 50 units
    ↓ (learns temporal patterns)
Dropout (prevents overfitting)
    ↓
Dense Layer 25 units
    ↓ (feature extraction)
Dropout
    ↓
Dense Output 1 unit
    ↓
Prediction
```

**How it works**:
1. LSTM cell learns long-term dependencies
2. Dropout randomly removes neurons
3. Dense layers process features
4. Output single prediction

**Advantages**:
- Captures temporal patterns
- Handles long sequences
- State-of-the-art for time series

**Disadvantages**:
- Needs more data
- Slower training
- Harder to interpret

---

### 5. utils/model_evaluator.py - Model Evaluation

**Purpose**: Measure model performance

**Metrics Calculation**:

#### MAE (Mean Absolute Error)
```python
MAE = (1/n) × Σ|y_true - y_pred|

Example:
Actual:   [100, 150, 200]
Predicted:[95,  160, 190]
Errors:   [5,   10,   10]
MAE = 25/3 = 8.33

Interpretation:
- On average, predictions are off by 8.33 units
- Lower is better
```

#### RMSE (Root Mean Squared Error)
```python
RMSE = √[(1/n) × Σ(y_true - y_pred)²]

Example:
Actual:   [100, 150, 200]
Predicted:[95,  160, 190]
Errors²:  [25,  100, 100]
MSE = 225/3 = 75
RMSE = √75 = 8.66

Interpretation:
- Penalizes large errors more
- Same units as target
- Lower is better
```

#### R² Score
```python
R² = 1 - (SS_res / SS_tot)

Where:
SS_res = Σ(y_true - y_pred)²  (residual sum of squares)
SS_tot = Σ(y_true - mean(y_true))²  (total sum of squares)

Range: 0 to 1 (can be negative)
- 1.0 = Perfect prediction
- 0.5 = Model explains 50% of variance
- 0.0 = Model no better than mean
- <0.0 = Model worse than mean

Interpretation:
"The model explains X% of variance in data"
```

#### MAPE (Mean Absolute Percentage Error)
```python
MAPE = (1/n) × Σ(|y_true - y_pred| / |y_true|) × 100

Example:
Actual:   [100, 150, 200]
Predicted:[95,  160, 190]
Percentages: [5%, 6.67%, 5%]
MAPE = 16.67/3 = 5.56%

Interpretation:
- On average, predictions are off by 5.56%
- Good for comparing across different scales
- Lower is better
```

---

## Data Flow Diagram

```
┌─────────────────┐
│   User Input    │
│ (CSV File)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   app.py                        │
│ - Receive file                  │
│ - Store in session_state.data   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   DataProcessor                 │
│ 1. Parse DateTime               │
│ 2. Handle Missing Values        │
│ 3. Detect Outliers              │
│ 4. Select Numeric Features      │
│ 5. Scale Features               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   ModelTrainer                  │
│ 1. Create Lagged Features       │
│ 2. Train/Test Split             │
│ 3. Train Models                 │
│ 4. Make Predictions             │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   ModelEvaluator                │
│ 1. Calculate MAE                │
│ 2. Calculate RMSE               │
│ 3. Calculate R² Score           │
│ 4. Calculate MAPE               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   app.py Results Tab            │
│ - Display Metrics               │
│ - Interactive Charts            │
│ - Download Options              │
└─────────────────────────────────┘
```

---

## Configuration Examples

### Example 1: Accuracy-Focused
```python
CONFIG = {
    'models': {
        'xgboost': {
            'n_estimators': 500,      # More trees
            'max_depth': 8,           # Deeper trees
            'learning_rate': 0.05,    # Slower learning
        },
        'lstm': {
            'epochs': 100,            # More training
            'batch_size': 16,         # Smaller batches
        }
    },
    'preprocessing': {
        'outlier_threshold': 2,       # Stricter outlier detection
    }
}
```

### Example 2: Speed-Focused
```python
CONFIG = {
    'models': {
        'random_forest': {
            'n_estimators': 50,       # Fewer trees
            'max_depth': 10,          # Shallower trees
        }
    },
    'preprocessing': {
        'outlier_threshold': 4,       # Looser outlier detection
    }
}
```

### Example 3: Production-Ready
```python
CONFIG = {
    'models': {
        'xgboost': {
            'n_estimators': 200,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,         # Use 80% of samples per tree
            'colsample_bytree': 0.8,  # Use 80% of features per tree
        }
    },
    'preprocessing': {
        'outlier_threshold': 3,
        'missing_value_threshold': 0.3,  # Remove columns >30% missing
    }
}
```

---

## Performance Optimization

### 1. Data Level
```python
# Reduce dataset size
data = data.sample(frac=0.5)

# Use only relevant columns
data = data[['Date', 'Global_active_power']]

# Aggregate to daily data
data_daily = data.resample('D').mean()
```

### 2. Model Level
```python
# Reduce tree depth
'max_depth': 5  # Faster training

# Fewer estimators
'n_estimators': 50  # Faster training

# Smaller LSTM
LSTM(20, ...)  # Faster training
```

### 3. Code Level
```python
# Use n_jobs for parallelization
'n_jobs': -1  # Use all CPU cores

# Reduce epochs for LSTM
'epochs': 20  # Faster training

# Batch processing
# Process in batches instead of all at once
```

---

## Error Handling

### Data Validation
```python
try:
    data = pd.read_csv(uploaded_file, delimiter=';')
except:
    uploaded_file.seek(0)
    data = pd.read_csv(uploaded_file)

# Validate columns
required_cols = ['Date', 'Time']
if not all(col in data.columns for col in required_cols):
    raise ValueError("Missing required columns")
```

### Model Validation
```python
if not selected_models:
    raise ValueError("Select at least one model")

if st.session_state.processed_data is None:
    raise ValueError("Preprocess data first")
```

### Prediction Validation
```python
# Check for NaN values
if np.isnan(y_pred).any():
    logger.warning("NaN values in predictions")
    y_pred = np.nan_to_num(y_pred)
```

---

## Logging System

**Log Levels**:
- **INFO**: Normal execution flow
- **WARNING**: Unexpected but handled
- **ERROR**: Serious problems
- **DEBUG**: Detailed debugging info

**Log Format**:
```
2024-01-15 10:30:45,123 - utils.data_processor - INFO - Starting data processing pipeline
```

**Access Logs**:
```bash
# View recent logs
tail -f logs/app.log

# Search for errors
grep "ERROR" logs/app.log

# Clear logs
rm logs/app.log
```

---

## Testing

### Unit Tests for DataProcessor
```python
def test_data_processor():
    processor = DataProcessor()
    data = pd.DataFrame({'A': [1, 2, None, 4, 5]})
    processed, report = processor.process(data)
    assert processed.isnull().sum().sum() == 0  # No missing values
```

### Unit Tests for ModelTrainer
```python
def test_model_trainer():
    trainer = ModelTrainer()
    data = pd.DataFrame({'values': np.random.randn(100)})
    model, y_test, y_pred = trainer.train_model(data, "Linear Regression")
    assert len(y_pred) == len(y_test)  # Output shape matches
```

---

## Deployment Considerations

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment (Heroku)
```bash
# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
git push heroku main
```

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| OOM Error | Dataset too large | Use sampling or aggregation |
| Slow training | Too many estimators | Reduce n_estimators |
| Poor accuracy | Bad preprocessing | Try different strategies |
| NaN predictions | Data issues | Check for inf/null values |
| Import errors | Missing packages | Run `pip install -r requirements.txt` |

---

## Future Enhancements

1. **Real-time Data Integration**
   - Connect to live electricity meter APIs
   - Update predictions automatically

2. **Advanced Models**
   - Prophet (Facebook)
   - AutoML solutions
   - Ensemble methods

3. **Feature Engineering**
   - Temperature correlation
   - Holiday patterns
   - Seasonal decomposition

4. **Model Persistence**
   - Save trained models
   - Load and reuse models
   - Model versioning

5. **API Integration**
   - RESTful API for predictions
   - Mobile app integration
   - Third-party data sources

---

## References

- [Scikit-learn Docs](https://scikit-learn.org/stable/)
- [XGBoost Docs](https://xgboost.readthedocs.io/)
- [Keras/TensorFlow](https://keras.io/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Time Series Analysis](https://en.wikipedia.org/wiki/Time_series)

---

**Version**: 1.0.0  
**Last Updated**: 2024
