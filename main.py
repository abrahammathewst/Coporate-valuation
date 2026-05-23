from app.dcf.projections import (
    project_revenue,
    project_ebit
)

from app.dcf.valuation import (
    calculate_nopat,
    calculate_fcff,
    discount_cash_flows,
    calculate_terminal_value,
    calculate_enterprise_value
)


growth_rates = [0.10, 0.09, 0.08, 0.07, 0.06]

revenue_df = project_revenue(
    base_revenue=1000000,
    growth_rates=growth_rates
)

ebit_margins = [0.20, 0.20, 0.21, 0.22, 0.23, 0.24]

valuation_df = project_ebit(
    revenue_df=revenue_df,
    ebit_margins=ebit_margins
)

valuation_df = calculate_nopat(
    valuation_df=valuation_df,
    tax_rate=0.25
)

valuation_df = calculate_fcff(
    valuation_df=valuation_df,
    base_capex=50000,
    base_depreciation=30000,
    base_nwc=20000,
    base_net_capital_assets=250000
)

valuation_df = discount_cash_flows(
    valuation_df=valuation_df,
    wacc=0.10
)

terminal_results = calculate_terminal_value(
    valuation_df=valuation_df,
    wacc=0.10,
    terminal_growth_rate=0.03
)

valuation_results = calculate_enterprise_value(
    valuation_df=valuation_df,
    pv_terminal_value=terminal_results[
        "PV of Terminal Value"
    ],
    cash=300000,
    debt=500000,
    shares_outstanding=100000
)

print("\nFinal Valuation Results")
print(valuation_results)
# valuation_df.T.to_csv("valuation_output.csv", index=True)