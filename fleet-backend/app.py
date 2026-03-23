from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  
# global storage (for demo)
analytics_data = {}

@app.route("/upload", methods=["POST"])
def upload():

    global analytics_data

    file = request.files["file"]

    df = pd.read_excel(file)

    df["date"] = pd.to_datetime(df["date"])

    df["total_expense"] = df["fuel_cost"] + df["other_expense"]
    df["profit"] = df["revenue"] - df["total_expense"]

    df["margin"] = (df["profit"] / df["revenue"]) * 100
    df["fuel_percent"] = (df["fuel_cost"] / df["revenue"]) * 100


    # VEHICLE SUMMARY
    vehicle_summary = df.groupby(
        ["vehicle_number", "vehicle_type"]
    ).agg(
        revenue=("revenue", "sum"),
        fuel_cost=("fuel_cost", "sum"),
        other_expense=("other_expense", "sum"),
        total_expense=("total_expense", "sum"),
        profit=("profit", "sum")
    ).reset_index()

    vehicle_summary["margin"] = (
        vehicle_summary["profit"] /
        vehicle_summary["revenue"] * 100
    )

    vehicle_summary["fuel_percent"] = (
        vehicle_summary["fuel_cost"] /
        vehicle_summary["revenue"] * 100
    )


    # DRIVER SUMMARY
    driver_summary = df.groupby(
        ["driver_name"]
    ).agg(
        revenue=("revenue", "sum"),
        fuel_cost=("fuel_cost", "sum"),
        other_expense=("other_expense", "sum"),
        total_expense=("total_expense", "sum"),
        profit=("profit", "sum")
    ).reset_index()

    driver_summary["margin"] = (
        driver_summary["profit"] /
        driver_summary["revenue"] * 100
    )


    # DAILY REVENUE
    daily_revenue = df.groupby("date").agg(
        revenue=("revenue", "sum")
    ).reset_index()

    daily_revenue["date"] = daily_revenue["date"].astype(str)


    # KPI
    total_revenue = df["revenue"].sum()
    total_expense = df["total_expense"].sum()
    total_profit = df["profit"].sum()
    total_margin = (total_profit / total_revenue) * 100


    analytics_data = {

        "kpi": {
            "revenue": float(total_revenue),
            "expense": float(total_expense),
            "profit": float(total_profit),
            "margin": float(total_margin)
        },

        "vehicle_summary": vehicle_summary.to_dict(orient="records"),

        "driver_summary": driver_summary.to_dict(orient="records"),

        "daily_revenue": daily_revenue.to_dict(orient="records")
    }

    return jsonify({"message": "File processed successfully"})


@app.route("/data", methods=["GET"])    
def get_data():

    global analytics_data

    if not analytics_data:
        return jsonify({"error": "No data uploaded yet"})

    return jsonify(analytics_data)


def convert_numpy(data):
    import numpy as np

    if isinstance(data, dict):
        return {k: convert_numpy(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy(v) for v in data]
    elif isinstance(data, (np.integer)):
        return int(data)
    elif isinstance(data, (np.floating)):
        return float(data)
    else:
        return data
#test route
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)