from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="MIRRORVERSE API",
    description="Future Simulation Engine",
    version="1.0.0"
)


class BusinessInput(BaseModel):
    investment: float = Field(gt=0)
    monthly_expenses: float = Field(ge=0)
    expected_monthly_sales: float = Field(ge=0)
    gross_margin_percent: float = Field(gt=0, le=100)


def simulate(sales, expenses, margin, investment):
    gross_profit = sales * margin / 100
    net_profit = gross_profit - expenses

    return {
        "monthly_sales": round(sales, 2),
        "gross_profit": round(gross_profit, 2),
        "monthly_expenses": round(expenses, 2),
        "estimated_monthly_profit": round(net_profit, 2),
        "break_even_sales": round(
            expenses / (margin / 100), 2
        ),
        "estimated_payback_months": (
            round(investment / net_profit, 2)
            if net_profit > 0 else None
        )
    }


@app.get("/")
def home():
    return {
        "project": "MIRRORVERSE",
        "message": "Future Simulation Engine is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/v1/simulate/business")
def business_simulation(data: BusinessInput):

    scenarios = {
        "worst_case": simulate(
            data.expected_monthly_sales * 0.70,
            data.monthly_expenses,
            data.gross_margin_percent,
            data.investment
        ),
        "normal_case": simulate(
            data.expected_monthly_sales,
            data.monthly_expenses,
            data.gross_margin_percent,
            data.investment
        ),
        "best_case": simulate(
            data.expected_monthly_sales * 1.30,
            data.monthly_expenses,
            data.gross_margin_percent,
            data.investment
        )
    }

    return {
        "project": "MIRRORVERSE",
        "simulation_type": "business",
        "currency": "INR",
        "results": scenarios,
        "disclaimer": (
            "These are illustrative scenarios, "
            "not guaranteed financial predictions."
        )
    }