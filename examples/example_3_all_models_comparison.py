"""
Example 3: Training and Comparing All Models
Demonstrates how to train all 5 ML algorithms and compare performance
"""

import pandas as pd
import numpy as np
import time
from utils.data_processor import DataProcessor
from utils.model_trainer import ModelTrainer
from utils.model_evaluator import ModelEvaluator
from utils.logger import setup_logger

logger = setup_logger(__name__)

# ============================================
# CONFIGURATION
# ============================================

DATA_FILE = 'household_power_consumption.txt/household_power_consumption.txt'
MAX_ROWS = 500
ALL_MODELS = [
    "Linear Regression",
    "Random Forest",
    "XGBoost",
    "Gradient Boosting",
    "LSTM"
]

# ============================================
# 1. LOAD AND PREPROCESS DATA
# ============================================

logger.info("Loading and preprocessing data...")
print("Loading data...")

try:
    data = pd.read_csv(DATA_FILE, delimiter=';', nrows=MAX_ROWS)
except Exception as e:
    logger.error(f"Error loading data: {e}")
    exit(1)

print(f"Raw data shape: {data.shape}\n")

# Preprocess
processor = DataProcessor(
    missing_strategy='interpolate',
    outlier_detection=True,
    scaling_method='standard'
)

processed_data, report = processor.process(data)
print(f"Processed data shape: {processed_data.shape}")
print(f"Outliers detected: {report.get('outliers_detected', 0)}\n")

# ============================================
# 2. TRAIN ALL MODELS
# ============================================

print("="*70)
print("TRAINING ALL MODELS")
print("="*70)

trainer = ModelTrainer(test_size=0.2, random_state=42)
evaluator = ModelEvaluator()

models_dict = {}
metrics_dict = {}
training_times = {}

for model_name in ALL_MODELS:
    print(f"\nTraining {model_name}...", end=" ", flush=True)
    
    start_time = time.time()
    
    try:
        model, y_test, y_pred = trainer.train_model(processed_data, model_name)
        
        training_time = time.time() - start_time
        training_times[model_name] = training_time
        
        if model is not None:
            models_dict[model_name] = model
            metrics = evaluator.evaluate(y_test, y_pred)
            metrics_dict[model_name] = metrics
            
            print(f"✓ ({training_time:.2f}s)")
        else:
            print("✗ Failed")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error(f"Error training {model_name}: {e}")

# ============================================
# 3. DISPLAY RESULTS
# ============================================

print("\n" + "="*70)
print("MODEL PERFORMANCE COMPARISON")
print("="*70)

# Create results dataframe
results_df = pd.DataFrame({
    model: metrics for model, metrics in metrics_dict.items()
}).T

print("\nMetrics by Model:")
print(results_df.to_string())

print("\nTraining Time:")
for model, time_taken in sorted(training_times.items(), key=lambda x: x[1]):
    print(f"  {model}: {time_taken:.2f}s")

# ============================================
# 4. RANKING
# ============================================

print("\n" + "="*70)
print("RANKING BY METRIC")
print("="*70)

metrics_to_rank = ['MAE', 'RMSE', 'R2', 'MAPE']

for metric in metrics_to_rank:
    print(f"\nRanking by {metric}:")
    
    # For R2, higher is better; for others, lower is better
    if metric == 'R2':
        sorted_models = sorted(metrics_dict.items(), 
                             key=lambda x: x[1][metric], 
                             reverse=True)
    else:
        sorted_models = sorted(metrics_dict.items(), 
                             key=lambda x: x[1][metric])
    
    for rank, (model, metrics) in enumerate(sorted_models, 1):
        print(f"  {rank}. {model}: {metrics[metric]:.4f}")

# ============================================
# 5. BEST MODEL SELECTION
# ============================================

print("\n" + "="*70)
print("BEST MODEL RECOMMENDATIONS")
print("="*70)

best_r2_model = max(metrics_dict.items(), key=lambda x: x[1]['R2'])
best_mae_model = min(metrics_dict.items(), key=lambda x: x[1]['MAE'])
best_rmse_model = min(metrics_dict.items(), key=lambda x: x[1]['RMSE'])
fastest_model = min(training_times.items(), key=lambda x: x[1])

print(f"\n📊 Best R² Score: {best_r2_model[0]} ({best_r2_model[1]['R2']:.4f})")
print(f"📊 Best MAE: {best_mae_model[0]} ({best_mae_model[1]['MAE']:.4f})")
print(f"📊 Best RMSE: {best_rmse_model[0]} ({best_rmse_model[1]['RMSE']:.4f})")
print(f"⚡ Fastest: {fastest_model[0]} ({fastest_model[1]:.2f}s)")

# ============================================
# 6. DETAILED ANALYSIS
# ============================================

print("\n" + "="*70)
print("DETAILED ANALYSIS")
print("="*70)

for model_name in sorted(metrics_dict.keys()):
    metrics = metrics_dict[model_name]
    train_time = training_times.get(model_name, 'N/A')
    
    print(f"\n{model_name}:")
    print(f"  Accuracy (R²):      {metrics['R2']:.4f}")
    print(f"  Mean Error (MAE):   {metrics['MAE']:.4f}")
    print(f"  RMSE:               {metrics['RMSE']:.4f}")
    print(f"  Percentage Error:   {metrics['MAPE']:.4f}%")
    print(f"  Training Time:      {train_time:.2f}s" if train_time != 'N/A' else f"  Training Time:      {train_time}")

# ============================================
# 7. RECOMMENDATIONS FOR USE CASES
# ============================================

print("\n" + "="*70)
print("USE CASE RECOMMENDATIONS")
print("="*70)

print("""
🎯 Quick Predictions (Speed Priority):
   Use: Linear Regression or fastest model
   Pros: Fast training, immediate results
   
📊 High Accuracy (Accuracy Priority):
   Use: XGBoost, Gradient Boosting, or best R² model
   Pros: Best predictions, handles complexity
   
⚖️  Balanced (Speed vs Accuracy):
   Use: Random Forest
   Pros: Good accuracy with reasonable speed
   
🔬 Advanced Analysis (Complex Patterns):
   Use: LSTM (if sufficient data available)
   Pros: Captures temporal dependencies
""")

# ============================================
# 8. SUMMARY STATISTICS
# ============================================

print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)

avg_r2 = np.mean([m['R2'] for m in metrics_dict.values()])
avg_mae = np.mean([m['MAE'] for m in metrics_dict.values()])
avg_rmse = np.mean([m['RMSE'] for m in metrics_dict.values()])
avg_time = np.mean(list(training_times.values()))

print(f"\nAverage Performance Across All Models:")
print(f"  Average R²:         {avg_r2:.4f}")
print(f"  Average MAE:        {avg_mae:.4f}")
print(f"  Average RMSE:       {avg_rmse:.4f}")
print(f"  Average Train Time: {avg_time:.2f}s")

total_time = sum(training_times.values())
print(f"\nTotal Training Time: {total_time:.2f}s for {len(ALL_MODELS)} models")

logger.info("All models trained and compared successfully!")
print("\n✅ Comparison completed successfully!")
