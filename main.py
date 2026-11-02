from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Any

app = FastAPI(
    title="MIRRORVERSE Future Engine",
    description="A decision simulation API for individuals and businesses.",
    version="1.0.0"
)


class BusinessInput(BaseModel):
    investment: float = Field(ge=0)
    monthly_expenses: float = Field(ge=0)
    expected_monthly_sales: float = Field(ge=0)
    gross_margin_percent: float = Field(ge=0, le=100)


def simulate_scenario(
    sales: float,
    expenses: float,
    margin_percent: float,
    investment: float
) -> Dict[str, Any]:

    margin = margin_percent / 100

    gross_profit = sales * margin
    monthly_profit = gross_profit - expenses

    break_even_sales = (
        expenses / margin if margin > 0 else None
    )

    profit_margin = (
        (monthly_profit / sales) * 100 if sales > 0 else 0
    )

    monthly_roi = (
        (monthly_profit / investment) * 100
        if investment > 0 else None
    )

    recovery_months = (
        investment / monthly_profit
        if monthly_profit > 0 and investment > 0
        else None
    )

    return {
        "monthly_sales": round(sales, 2),
        "gross_profit": round(gross_profit, 2),
        "monthly_expenses": round(expenses, 2),
        "estimated_monthly_profit": round(monthly_profit, 2),
        "profit_margin_percent": round(profit_margin, 2),
        "monthly_roi_percent": (
            round(monthly_roi, 2)
            if monthly_roi is not None else None
        ),
        "break_even_sales": (
            round(break_even_sales, 2)
            if break_even_sales is not None else None
        ),
        "investment_recovery_months": (
            round(recovery_months, 2)
            if recovery_months is not None else None
        ),
        "status": (
            "Profitable"
            if monthly_profit > 0
            else "Loss"
            if monthly_profit < 0
            else "Break-even"
        )
    }


@app.get("/")
def home():
    return {
        "project": "MIRRORVERSE",
        "product": "Future Engine",
        "version": "1.0.0",
        "message": "Imagine. Simulate. Decide.",
        "status": "online"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/v1/simulate/business")
def simulate_business(data: BusinessInput):

    sales = data.expected_monthly_sales

    scenarios = {
        "worst_case": simulate_scenario(
            sales * 0.70,
            data.monthly_expenses,
            data.gross_margin_percent,
            data.investment
        ),

        "normal_case": simulate_scenario(
            sales,
            data.monthly_expenses,
            data.gross_margin_percent,
            data.investment
        ),

        "best_case": simulate_scenario(
            sales * 1.30,
            data.monthly_expenses,
            data.gross_margin_percent,
            data.investment
        )
    }

    return {
        "engine": "MIRRORVERSE Future Engine",
        "version": "1.0.0",
        "input": data.model_dump(),
        "currency": "INR",
        "period": "Monthly",
        "scenarios": scenarios,
        "assumptions": [
            "Worst case assumes sales are 30% below expected sales.",
            "Normal case uses the expected sales value.",
            "Best case assumes sales are 30% above expected sales.",
            "Gross margin and monthly expenses remain constant.",
            "Taxes, loan interest, depreciation and unexpected costs are excluded."
        ],
        "disclaimer": (
            "These are illustrative financial scenarios, "
            "not guaranteed predictions or financial advice."
        )
    }