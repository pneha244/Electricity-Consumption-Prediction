import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None

st.set_page_config(page_title="Electricity Consumption Prediction", layout="wide")

MODEL_OPTIONS = {
    "Linear Regression": LinearRegression,
    "Random Forest": RandomForestRegressor,
    "Gradient Boosting": GradientBoostingRegressor,
}

if XGBRegressor is not None:
    MODEL_OPTIONS["XGBoost"] = XGBRegressor

DEFAULT_DATA_PATH = "household_power_consumption.txt/household_power_consumption.txt"

@st.cache_data
def load_default_data():
    df = pd.read_csv(DEFAULT_DATA_PATH, sep=';', na_values=['?'], low_memory=False)
    return df

@st.cache_data
def preprocess_data(df):
    data = df.copy()

    data = data.replace('?', np.nan)
    data = data.replace([np.inf, -np.inf], np.nan)

    if "Date" in data.columns and "Time" in data.columns:
        data["DateTime"] = pd.to_datetime(
            data["Date"] + " " + data["Time"],
            dayfirst=True,
            errors="coerce"
        )
        data = data.drop(columns=[col for col in ["Date", "Time"] if col in data.columns])
        data = data.set_index("DateTime")

    for col in data.columns:
        if data[col].dtype == object:
            data[col] = data[col].astype(str).str.replace(',', '.', regex=False)
            data[col] = pd.to_numeric(data[col], errors='coerce')

    data = data.ffill().bfill()
    data = data.dropna()

    if data.empty:
        raise ValueError("Preprocessing produced an empty dataset.")

    if "Global_active_power" in data.columns:
        target_column = "Global_active_power"
    else:
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) < 2:
            raise ValueError("Not enough numeric columns available for training.")
        target_column = numeric_cols[0]

    X = data.drop(columns=[target_column])
    y = data[target_column]

    if X.shape[1] == 0:
        raise ValueError("No input features available after selecting the target column.")

    return X, y, data

def build_model(model_name):
    if model_name == "Linear Regression":
        return LinearRegression()
    if model_name == "Random Forest":
        return RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    if model_name == "Gradient Boosting":
        return GradientBoostingRegressor(n_estimators=100, random_state=42)
    if model_name == "XGBoost":
        return XGBRegressor(objective='reg:squarederror', random_state=42, n_jobs=-1)
    raise ValueError("Unsupported model")

def evaluate_model(_model, X_train, X_test, y_train, y_test):
    _model.fit(X_train, y_train)
    y_pred = _model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return {
        "MAE": mean_absolute_error(y_test, y_pred),
        "RMSE": mse ** 0.5,
        "R2": r2_score(y_test, y_pred),
        "y_pred": y_pred,
    }

st.title("⚡ Electricity Consumption Prediction")
st.write("A simple regression app with minimal features for stable operation.")

data_source = st.sidebar.radio("Data source", ["Default dataset", "Upload CSV"])
model_name = st.sidebar.selectbox("Choose model", list(MODEL_OPTIONS.keys()), index=1)
test_size = st.sidebar.slider("Test size (%)", 10, 40, 20)
random_state = st.sidebar.number_input("Random seed", value=42, step=1)
max_rows = st.sidebar.number_input("Max rows to use", value=100000, min_value=10000, max_value=300000, step=10000)

if data_source == "Default dataset":
    try:
        raw_df = load_default_data()
    except FileNotFoundError:
        st.error(f"Default dataset not found at {DEFAULT_DATA_PATH}. Upload a CSV file instead.")
        raw_df = None
else:
    uploaded_file = st.file_uploader("Upload electricity consumption CSV file", type=["csv", "txt"])
    raw_df = None
    if uploaded_file is not None:
        try:
            try:
                raw_df = pd.read_csv(uploaded_file, sep=';', low_memory=False)
            except Exception:
                uploaded_file.seek(0)
                raw_df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Unable to load uploaded file: {e}")
            raw_df = None

if raw_df is not None:
    st.subheader("Dataset preview")
    st.write(raw_df.head())
    st.write(f"Rows: {raw_df.shape[0]} | Columns: {raw_df.shape[1]}")

    try:
        X, y, cleaned = preprocess_data(raw_df)
        if len(cleaned) > max_rows:
            cleaned = cleaned.iloc[:max_rows]
            X = X.iloc[:max_rows]
            y = y.iloc[:max_rows]

        st.subheader("Cleaned data summary")
        st.write(cleaned.describe())

        feature_names = X.columns.tolist()
        feature_defaults = X.median().to_dict()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size / 100.0, random_state=random_state
        )

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        st.subheader("Model training")
        if st.button("Train and evaluate"):
            model = build_model(model_name)
            results = evaluate_model(model, X_train, X_test, y_train, y_test)

            st.session_state["trained_model"] = model
            st.session_state["scaler"] = scaler
            st.session_state["feature_names"] = feature_names
            st.session_state["feature_defaults"] = feature_defaults

            st.success("✅ Training completed")
            st.write("### Evaluation metrics")
            st.metric("MAE", f"{results['MAE']:.4f}")
            st.metric("RMSE", f"{results['RMSE']:.4f}")
            st.metric("R2", f"{results['R2']:.4f}")

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(y_test.values[:200], label="Actual", alpha=0.8)
            ax.plot(results['y_pred'][:200], label="Predicted", alpha=0.8)
            ax.set_title("Actual vs Predicted (first 200 points)")
            ax.legend()
            st.pyplot(fig)

            st.write("### Model details")
            st.write(model)

        if "trained_model" in st.session_state:
            st.subheader("Predict single input")
            input_values = {}
            for feature in st.session_state["feature_names"]:
                input_values[feature] = st.number_input(
                    f"{feature}",
                    value=float(st.session_state["feature_defaults"].get(feature, 0.0)),
                    format="%.4f",
                )

            if st.button("Predict custom input"):
                model = st.session_state["trained_model"]
                scaler = st.session_state["scaler"]
                raw_input = np.array([input_values[feature] for feature in st.session_state["feature_names"]], dtype=float).reshape(1, -1)
                scaled_input = scaler.transform(raw_input)
                prediction = model.predict(scaled_input)[0]
                st.success(f"Predicted Global_active_power: {prediction:.4f}")
    except Exception as exc:
        st.error(f"Preprocessing or training failed: {exc}")
        st.stop()
else:
    st.info("Upload a CSV file or choose the default dataset to continue.")
