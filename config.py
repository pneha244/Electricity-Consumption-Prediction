"""
Configuration settings for Electricity Consumption Prediction
"""

CONFIG = {
    # Model Parameters
    'models': {
        'linear_regression': {
            'name': 'Linear Regression',
            'params': {}
        },
        'random_forest': {
            'name': 'Random Forest',
            'params': {
                'n_estimators': 100,
                'max_depth': 20,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'random_state': 42,
                'n_jobs': -1
            }
        },
        'xgboost': {
            'name': 'XGBoost',
            'params': {
                'n_estimators': 100,
                'max_depth': 6,
                'learning_rate': 0.1,
                'random_state': 42,
                'n_jobs': -1,
                'verbosity': 0
            }
        },
        'gradient_boosting': {
            'name': 'Gradient Boosting',
            'params': {
                'n_estimators': 100,
                'max_depth': 5,
                'learning_rate': 0.1,
                'random_state': 42
            }
        },
        'lstm': {
            'name': 'LSTM',
            'params': {
                'epochs': 50,
                'batch_size': 32,
                'validation_split': 0.2,
                'verbose': 0,
                'sequence_length': 10
            }
        }
    },
    
    # Data Preprocessing
    'preprocessing': {
        'missing_value_threshold': 0.5,  # 50%
        'outlier_threshold': 3,  # 3 sigma
        'scaling_methods': ['standard', 'minmax', 'robust']
    },
    
    # File Paths
    'paths': {
        'data': 'household_power_consumption.txt',
        'logs': 'logs/',
        'models': 'models/',
        'reports': 'reports/'
    },
    
    # Logging
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'logs/app.log'
    },
    
    # Evaluation Metrics
    'metrics': ['MAE', 'RMSE', 'R2', 'MAPE']
}
