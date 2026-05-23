import pandas as pd


def calculate_nopat(
    valuation_df: pd.DataFrame,
    tax_rate: float
):
    valuation_df = valuation_df.copy()

    valuation_df["Tax Rate"] = tax_rate

    valuation_df["Taxes"] = (
        valuation_df["EBIT"]
        * valuation_df["Tax Rate"]
    )

    valuation_df["NOPAT"] = (
        valuation_df["EBIT"]
        - valuation_df["Taxes"]
    )

    return valuation_df

def calculate_fcff(
    valuation_df: pd.DataFrame,
    base_capex: float,
    base_depreciation: float,
    base_nwc: float,
    base_net_capital_assets: float
):
    """
    Calculates FCFF using linked reinvestment logic.
    """

    valuation_df = valuation_df.copy()

    # ---------------------------------------------------
    # Base Metrics
    # ---------------------------------------------------

    base_revenue = valuation_df.loc[0, "Revenue"]

    capex_rate = base_capex / base_revenue

    nwc_rate = base_nwc / base_revenue

    depreciation_rate = (
        base_depreciation
        / base_net_capital_assets
    )

    # Store assumptions
    valuation_df["CapEx Rate"] = capex_rate
    valuation_df["NWC Rate"] = nwc_rate
    valuation_df["Depreciation Rate"] = depreciation_rate

    # ---------------------------------------------------
    # Forecast CapEx
    # ---------------------------------------------------

    valuation_df["CapEx"] = (
        valuation_df["Revenue"]
        * capex_rate
    )

    # ---------------------------------------------------
    # Forecast NWC
    # ---------------------------------------------------

    valuation_df["NWC"] = (
        valuation_df["Revenue"]
        * nwc_rate
    )

    valuation_df["Change in NWC"] = (
        valuation_df["NWC"].diff()
    )

    valuation_df.loc[0, "Change in NWC"] = 0

    # ---------------------------------------------------
    # Sequential Forecasting
    # ---------------------------------------------------

    net_capital_assets_list = []
    depreciation_list = []

    current_nca = base_net_capital_assets

    for i in range(len(valuation_df)):

        # Base year
        if i == 0:

            current_depreciation = base_depreciation

            net_capital_assets_list.append(current_nca)

            depreciation_list.append(current_depreciation)

            continue

        # ---------------------------------------------
        # Depreciation based on previous year's NCA
        # ---------------------------------------------

        current_depreciation = (
            current_nca
            * depreciation_rate
        )

        current_depreciation = max(
            current_depreciation,
            0
        )

        # ---------------------------------------------
        # Update Net Capital Assets
        # ---------------------------------------------

        current_nca = (
            current_nca
            + valuation_df.loc[i, "CapEx"]
            - current_depreciation
        )

        net_capital_assets_list.append(current_nca)

        depreciation_list.append(current_depreciation)

    valuation_df["Net Capital Assets"] = (
        net_capital_assets_list
    )

    valuation_df["Depreciation"] = (
        depreciation_list
    )

    # ---------------------------------------------------
    # FCFF
    # ---------------------------------------------------

    valuation_df["FCFF"] = (
        valuation_df["NOPAT"]
        + valuation_df["Depreciation"]
        - valuation_df["CapEx"]
        - valuation_df["Change in NWC"]
    )

    return valuation_df

def discount_cash_flows(
    valuation_df: pd.DataFrame,
    wacc: float
):
    valuation_df = valuation_df.copy()

    # ---------------------------------------------
    # Discount Factor
    # ---------------------------------------------

    valuation_df["Discount Factor"] = (
        1 / ((1 + wacc) ** valuation_df["Year"])
    )

    # ---------------------------------------------
    # Present Value of FCFF
    # ---------------------------------------------

    valuation_df["PV of FCFF"] = (
        valuation_df["FCFF"]
        * valuation_df["Discount Factor"]
    )

    return valuation_df

def calculate_terminal_value(
    valuation_df: pd.DataFrame,
    wacc: float,
    terminal_growth_rate: float
):
    """
    Calculates terminal value using Gordon Growth Model.
    """

    valuation_df = valuation_df.copy()

    if terminal_growth_rate >= wacc:
        raise ValueError(
            "Terminal growth rate must be less than WACC."
        )

    # ---------------------------------------------------
    # Final Forecast Year FCFF
    # ---------------------------------------------------

    final_fcff = valuation_df.loc[
        valuation_df.index[-1],
        "FCFF"
    ]

    # ---------------------------------------------------
    # Next Year's FCFF
    # ---------------------------------------------------

    terminal_fcff = (
        final_fcff
        * (1 + terminal_growth_rate)
    )

    # ---------------------------------------------------
    # Terminal Value
    # ---------------------------------------------------

    terminal_value = (
        terminal_fcff
        / (wacc - terminal_growth_rate)
    )

    # ---------------------------------------------------
    # Present Value of Terminal Value
    # ---------------------------------------------------

    final_year_discount_factor = valuation_df.loc[
        valuation_df.index[-1],
        "Discount Factor"
    ]

    pv_terminal_value = (
        terminal_value
        * final_year_discount_factor
    )

    return {
        "Terminal FCFF": terminal_fcff,
        "Terminal Value": terminal_value,
        "PV of Terminal Value": pv_terminal_value
    }

def calculate_enterprise_value(
    valuation_df: pd.DataFrame,
    pv_terminal_value: float,
    cash: float,
    debt: float,
    shares_outstanding: float
):
    """
    Calculates enterprise value, equity value,
    and intrinsic value per share.
    """

    # ---------------------------------------------------
    # Present Value of Forecast FCFF
    # ---------------------------------------------------

    pv_fcff = valuation_df["PV of FCFF"].sum()

    # ---------------------------------------------------
    # Enterprise Value
    # ---------------------------------------------------

    enterprise_value = (
        pv_fcff
        + pv_terminal_value
    )

    # ---------------------------------------------------
    # Equity Value
    # ---------------------------------------------------

    equity_value = (
        enterprise_value
        + cash
        - debt
    )

    # ---------------------------------------------------
    # Intrinsic Value Per Share
    # ---------------------------------------------------

    intrinsic_value_per_share = (
        equity_value
        / shares_outstanding
    )

    return {
        "PV of Forecast FCFF": pv_fcff,
        "Enterprise Value": enterprise_value,
        "Equity Value": equity_value,
        "Intrinsic Value Per Share":
            intrinsic_value_per_share
    }