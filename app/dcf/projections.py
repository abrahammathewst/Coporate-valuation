import pandas as pd


def project_revenue(
    base_revenue: float,
    growth_rates: list,
):
    projected_revenues = []

    # Add base year
    projected_revenues.append({
        "Year": 0,
        "Growth Rate": None,
        "Revenue": base_revenue
    })

    current_revenue = base_revenue

    # Forecast future years
    for year, growth_rate in enumerate(growth_rates, start=1):

        projected_revenue = current_revenue * (1 + growth_rate)

        projected_revenues.append({
            "Year": year,
            "Growth Rate": growth_rate,
            "Revenue": projected_revenue
        })

        current_revenue = projected_revenue

    revenue_df = pd.DataFrame(projected_revenues)

    return revenue_df

def project_ebit(
    revenue_df: pd.DataFrame,
    ebit_margins: list
):

    revenue_df = revenue_df.copy()

    if len(ebit_margins) != len(revenue_df):
        raise ValueError(
            "Length of EBIT margins must match revenue projections."
        )

    revenue_df["EBIT Margin"] = ebit_margins

    revenue_df["EBIT"] = (
        revenue_df["Revenue"]
        * revenue_df["EBIT Margin"]
    )

    return revenue_df