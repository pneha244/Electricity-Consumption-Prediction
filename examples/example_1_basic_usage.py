"""
Example 1: Basic Usage
Training a single model and making predictions
"""

import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.model_trainer import ModelTrainer
from utils.model_evaluator import ModelEvaluator
from utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

# ============================================
# 1. LOAD DATA
# ============================================

# Load the electricity consumption dataset
logger.info("Loading data...")
try:
    data = pd.read_csv('household_power_consumption.txt/household_power_consumption.txt', 
                       delimiter=';', nrows=1000)  # Using first 1000 rows for demo
except Exception as e:
    logger.error(f"Error loading data: {e}")
    exit(1)

print(f"Data shape: {data.shape}")
print(f"Columns: {list(data.columns)}")
print(f"\nFirst 5 rows:")
print(data.head())

# ============================================
# 2. PREPROCESS DATA
# ============================================

logger.info("Preprocessing data...")

processor = DataProcessor(
    missing_strategy='forward_fill',
    outlier_detection=True,
    scaling_method='standard'
)

processed_data, report = processor.process(data)

print(f"\nPreprocessing Report:")
print(f"- Original shape: {report['original_shape']}")
print(f"- Final shape: {report['final_shape']}")
print(f"- Missing values removed: {report['original_missing']} -> {report['after_missing_handling']}")
print(f"- Outliers detected: {report.get('outliers_detected', 0)}")
print(f"- Numerical features: {len(report['numerical_features'])}")

# ============================================
# 3. TRAIN MODELS
# ============================================

logger.info("Training models...")

trainer = ModelTrainer(test_size=0.2, random_state=42)
evaluator = ModelEvaluator()

models_dict = {}
metrics_dict = {}

models_to_train = [
    "Linear Regression",
    "Random Forest",
    "XGBoost",
    "Gradient Boosting"
]

for model_name in models_to_train:
    logger.info(f"Training {model_name}...")
    
    model, y_test, y_pred = trainer.train_model(processed_data, model_name)
    
    if model is not None:
        models_dict[model_name] = model
        
        # Evaluate model
        metrics = evaluator.evaluate(y_test, y_pred)
        metrics_dict[model_name] = metrics
        
        logger.info(f"{model_name} trained successfully!")

# ============================================
# 4. DISPLAY RESULTS
# ============================================

print("\n" + "="*60)
print("MODEL EVALUATION RESULTS")
print("="*60)

for model_name, metrics in metrics_dict.items():
    print(f"\n{model_name}:")
    print(f"  MAE:  {metrics['MAE']:.4f}")
    print(f"  RMSE: {metrics['RMSE']:.4f}")
    print(f"  R²:   {metrics['R2']:.4f}")
    print(f"  MAPE: {metrics['MAPE']:.4f}")

# ============================================
# 5. FIND BEST MODEL
# ============================================

best_model_name = evaluator.get_best_model(metrics_dict)
print(f"\n{'='*60}")
print(f"Best Model: {best_model_name}")
print(f"{'='*60}")

# ============================================
# 6. MAKE PREDICTIONS (example)
# ============================================

logger.info("Making predictions with best model...")

best_model = models_dict[best_model_name]

# Note: In actual usage, you would use the last portion of test data
# or new data for predictions
print(f"\nExample predictions from {best_model_name}:")
print("(Using test data samples)")

# Show first 10 predictions
evaluator.print_summary(metrics_dict)

logger.info("Example completed successfully!")
