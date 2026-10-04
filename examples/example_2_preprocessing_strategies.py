"""
Example 2: Comparing Preprocessing Strategies
Shows how different preprocessing approaches affect model performance
"""

import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.model_trainer import ModelTrainer
from utils.model_evaluator import ModelEvaluator
from utils.logger import setup_logger

logger = setup_logger(__name__)

# ============================================
# CONFIGURATION
# ============================================

# Data file path
DATA_FILE = 'household_power_consumption.txt/household_power_consumption.txt'
MAX_ROWS = 500  # Use first 500 rows for demo

# Preprocessing strategies to compare
STRATEGIES = {
    'forward_fill': {
        'missing_strategy': 'forward_fill',
        'outlier_detection': False,
        'scaling_method': 'standard'
    },
    'interpolate': {
        'missing_strategy': 'interpolate',
        'outlier_detection': False,
        'scaling_method': 'standard'
    },
    'with_outliers': {
        'missing_strategy': 'forward_fill',
        'outlier_detection': True,
        'scaling_method': 'standard'
    },
    'robust_scaling': {
        'missing_strategy': 'interpolate',
        'outlier_detection': True,
        'scaling_method': 'robust'
    }
}

# Model to use for comparison
MODEL_NAME = "Random Forest"

# ============================================
# 1. LOAD DATA
# ============================================

logger.info("Loading data...")
try:
    data = pd.read_csv(DATA_FILE, delimiter=';', nrows=MAX_ROWS)
except Exception as e:
    logger.error(f"Error loading data: {e}")
    exit(1)

print(f"Original data shape: {data.shape}")

# ============================================
# 2. COMPARE STRATEGIES
# ============================================

print("\n" + "="*70)
print("PREPROCESSING STRATEGY COMPARISON")
print("="*70)

results = {}

for strategy_name, strategy_config in STRATEGIES.items():
    print(f"\nTesting: {strategy_name}")
    print("-" * 70)
    
    try:
        # Preprocess with current strategy
        processor = DataProcessor(**strategy_config)
        processed_data, report = processor.process(data.copy())
        
        print(f"  Data shape after preprocessing: {processed_data.shape}")
        print(f"  Outliers detected: {report.get('outliers_detected', 0)}")
        print(f"  Scaling method: {strategy_config['scaling_method']}")
        
        # Train model
        trainer = ModelTrainer(test_size=0.2, random_state=42)
        model, y_test, y_pred = trainer.train_model(processed_data, MODEL_NAME)
        
        if model is not None:
            # Evaluate
            evaluator = ModelEvaluator()
            metrics = evaluator.evaluate(y_test, y_pred)
            results[strategy_name] = metrics
            
            print(f"  Model Performance:")
            print(f"    MAE:  {metrics['MAE']:.4f}")
            print(f"    RMSE: {metrics['RMSE']:.4f}")
            print(f"    R²:   {metrics['R2']:.4f}")
            print(f"    MAPE: {metrics['MAPE']:.4f}")
        else:
            print(f"  ⚠ Failed to train model")
            
    except Exception as e:
        logger.error(f"Error with {strategy_name}: {e}")
        print(f"  ✗ Error: {e}")

# ============================================
# 3. COMPARE RESULTS
# ============================================

print("\n" + "="*70)
print("SUMMARY COMPARISON")
print("="*70)

# Find best strategy for each metric
metrics_to_compare = ['MAE', 'RMSE', 'R2', 'MAPE']

for metric in metrics_to_compare:
    best_strategy = min(results, key=lambda x: results[x][metric])
    best_value = results[best_strategy][metric]
    
    print(f"\nBest {metric}: {best_strategy} ({best_value:.4f})")
    
    for strategy_name, metrics in results.items():
        print(f"  {strategy_name}: {metrics[metric]:.4f}")

# ============================================
# 4. RECOMMENDATION
# ============================================

print("\n" + "="*70)
print("RECOMMENDATIONS")
print("="*70)

# Calculate average rank for each strategy
ranks = {strategy: 0 for strategy in results.keys()}

for metric in metrics_to_compare:
    # Create ranking (lower is better for MAE, RMSE, MAPE; higher for R2)
    if metric == 'R2':
        sorted_strategies = sorted(results.items(), 
                                 key=lambda x: x[1][metric], 
                                 reverse=True)
    else:
        sorted_strategies = sorted(results.items(), 
                                 key=lambda x: x[1][metric])
    
    for rank, (strategy, _) in enumerate(sorted_strategies):
        ranks[strategy] += rank

# Find best overall strategy
best_overall = min(ranks, key=ranks.get)

print(f"\nBest Overall Strategy: {best_overall}")
print("\nRanking by Average Performance:")
for strategy, score in sorted(ranks.items(), key=lambda x: x[1]):
    print(f"  {strategy}: score {score}")

logger.info("Comparison completed successfully!")
