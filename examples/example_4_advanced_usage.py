"""
Example 4: Advanced Usage with Custom Configuration
Shows how to customize models and configuration for specific use cases
"""

import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.model_trainer import ModelTrainer
from utils.model_evaluator import ModelEvaluator
from utils.logger import setup_logger
from config import CONFIG
import copy

logger = setup_logger(__name__)

# ============================================
# CUSTOM CONFIGURATIONS
# ============================================

"""
Different configurations for different objectives
"""

CONFIGS = {
    'conservative': {
        'description': 'Conservative model - minimize overfitting risk',
        'modifications': {
            'random_forest': {
                'n_estimators': 50,
                'max_depth': 10,
            },
            'xgboost': {
                'n_estimators': 50,
                'max_depth': 3,
                'learning_rate': 0.05,
            }
        }
    },
    'aggressive': {
        'description': 'Aggressive model - maximize accuracy',
        'modifications': {
            'random_forest': {
                'n_estimators': 200,
                'max_depth': 30,
            },
            'xgboost': {
                'n_estimators': 200,
                'max_depth': 8,
                'learning_rate': 0.1,
            }
        }
    },
    'production': {
        'description': 'Production model - balance speed and accuracy',
        'modifications': {
            'random_forest': {
                'n_estimators': 100,
                'max_depth': 15,
            },
            'xgboost': {
                'n_estimators': 100,
                'max_depth': 6,
                'learning_rate': 0.1,
            }
        }
    }
}

# ============================================
# UTILITY FUNCTIONS
# ============================================

def create_custom_config(base_config, modifications):
    """Create a custom config by modifying base config"""
    custom_config = copy.deepcopy(base_config)
    
    for model_key, params in modifications.items():
        if model_key in custom_config['models']:
            custom_config['models'][model_key]['params'].update(params)
    
    return custom_config

def train_with_config(data, config, models_list):
    """Train models with custom configuration"""
    trainer = ModelTrainer(test_size=0.2, random_state=42)
    evaluator = ModelEvaluator()
    
    results = {}
    
    for model_name in models_list:
        try:
            model, y_test, y_pred = trainer.train_model(data, model_name)
            
            if model is not None:
                metrics = evaluator.evaluate(y_test, y_pred)
                results[model_name] = metrics
        
        except Exception as e:
            logger.error(f"Error training {model_name}: {e}")
    
    return results

# ============================================
# 1. LOAD AND PREPROCESS DATA
# ============================================

print("Loading and preprocessing data...")

try:
    data = pd.read_csv(
        'household_power_consumption.txt/household_power_consumption.txt',
        delimiter=';',
        nrows=500
    )
except Exception as e:
    logger.error(f"Error loading data: {e}")
    exit(1)

# Preprocess
processor = DataProcessor(
    missing_strategy='interpolate',
    outlier_detection=True,
    scaling_method='standard'
)

processed_data, _ = processor.process(data)
print(f"Data prepared: shape {processed_data.shape}\n")

# ============================================
# 2. TRAIN WITH DIFFERENT CONFIGURATIONS
# ============================================

print("="*70)
print("TRAINING WITH DIFFERENT CONFIGURATIONS")
print("="*70)

models_to_train = ["Random Forest", "XGBoost"]
config_results = {}

for config_name, config_info in CONFIGS.items():
    print(f"\n{config_name.upper()}")
    print(f"Description: {config_info['description']}")
    print("-" * 70)
    
    # Create custom config
    custom_config = create_custom_config(CONFIG, config_info['modifications'])
    
    # Train with custom config
    results = train_with_config(processed_data, custom_config, models_to_train)
    config_results[config_name] = results
    
    # Display results
    for model_name, metrics in results.items():
        print(f"\n  {model_name}:")
        print(f"    R²:   {metrics['R2']:.4f}")
        print(f"    MAE:  {metrics['MAE']:.4f}")
        print(f"    RMSE: {metrics['RMSE']:.4f}")

# ============================================
# 3. COMPARE CONFIGURATIONS
# ============================================

print("\n" + "="*70)
print("CONFIGURATION COMPARISON")
print("="*70)

for model_name in models_to_train:
    print(f"\n{model_name} Performance Across Configurations:")
    print("-" * 50)
    
    for config_name, results in config_results.items():
        if model_name in results:
            metrics = results[model_name]
            print(f"  {config_name:15s}: R²={metrics['R2']:.4f}, MAE={metrics['MAE']:.4f}")

# ============================================
# 4. CUSTOM PREPROCESSING PIPELINE
# ============================================

print("\n" + "="*70)
print("CUSTOM PREPROCESSING PIPELINES")
print("="*70)

# Pipeline 1: Aggressive cleaning (for noisy data)
print("\nPipeline 1: Aggressive Cleaning (for noisy data)")
print("-" * 50)

aggressive_processor = DataProcessor(
    missing_strategy='interpolate',
    outlier_detection=True,
    scaling_method='robust'
)

aggressive_processed, report = aggressive_processor.process(data.copy())
print(f"  Result: {aggressive_processed.shape}")
print(f"  Outliers removed: {report.get('outliers_detected', 0)}")

# Pipeline 2: Conservative cleaning (for clean data)
print("\nPipeline 2: Conservative Cleaning (for clean data)")
print("-" * 50)

conservative_processor = DataProcessor(
    missing_strategy='forward_fill',
    outlier_detection=False,
    scaling_method='standard'
)

conservative_processed, report = conservative_processor.process(data.copy())
print(f"  Result: {conservative_processed.shape}")
print(f"  Outliers removed: {report.get('outliers_detected', 0)}")

# ============================================
# 5. CUSTOM HYPERPARAMETER TUNING
# ============================================

print("\n" + "="*70)
print("HYPERPARAMETER TUNING EXAMPLE")
print("="*70)

"""
Example: Tuning XGBoost learning rate
"""

learning_rates = [0.01, 0.05, 0.1, 0.2]
xgb_results = {}

print("\nTuning XGBoost Learning Rate:")
print("-" * 50)

trainer = ModelTrainer(test_size=0.2, random_state=42)
evaluator = ModelEvaluator()

for lr in learning_rates:
    try:
        # Modify config for this iteration
        custom_config = copy.deepcopy(CONFIG)
        custom_config['models']['xgboost']['params']['learning_rate'] = lr
        
        model, y_test, y_pred = trainer.train_model(processed_data, "XGBoost")
        
        if model is not None:
            metrics = evaluator.evaluate(y_test, y_pred)
            xgb_results[lr] = metrics['R2']
            print(f"  Learning Rate {lr:0.2f}: R² = {metrics['R2']:.4f}")
    
    except Exception as e:
        logger.error(f"Error with lr={lr}: {e}")

# Find best learning rate
best_lr = max(xgb_results, key=xgb_results.get)
print(f"\n  Best Learning Rate: {best_lr:0.2f}")

# ============================================
# 6. RECOMMENDATIONS
# ============================================

print("\n" + "="*70)
print("RECOMMENDATIONS FOR YOUR USE CASE")
print("="*70)

print("""
SCENARIO 1: Production System (24/7 accuracy required)
  ✓ Configuration: production
  ✓ Models: XGBoost, Gradient Boosting
  ✓ Preprocessing: interpolate + outlier detection
  ✓ Update frequency: Daily or weekly retraining
  
SCENARIO 2: Research/Analysis (Maximum accuracy needed)
  ✓ Configuration: aggressive
  ✓ Models: XGBoost with tuning, LSTM
  ✓ Preprocessing: robust scaling + aggressive cleaning
  ✓ Update frequency: As needed
  
SCENARIO 3: Quick Estimates (Speed important)
  ✓ Configuration: conservative
  ✓ Models: Linear Regression, Random Forest
  ✓ Preprocessing: forward_fill, standard scaling
  ✓ Update frequency: Batch updates ok
  
SCENARIO 4: Real-time Predictions (Latency critical)
  ✓ Configuration: conservative
  ✓ Models: Linear Regression (fastest)
  ✓ Preprocessing: minimal
  ✓ Update frequency: Periodic batch
""")

logger.info("Advanced example completed successfully!")
print("\n✅ Advanced usage example completed!")
