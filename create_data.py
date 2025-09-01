import pandas as pd
import statsmodels.api as sm
import numpy as np
import argparse

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Run regression analysis with various specifications')
    parser.add_argument('--file', type=str, default='classfn_4064_final.csv',
                        help='Path to the CSV file (default: classfn_4064_final.csv)')
    parser.add_argument('--industry-dummies', action='store_true',
                        help='Include industry dummies in regression')
    parser.add_argument('--employment-control', action='store_true',
                        help='Include log of employment as control variable')
    parser.add_argument('--output', type=str, default='regression_results.csv',
                        help='Path to save regression results (default: regression_results.csv)')
    return parser.parse_args()

def run_regression(df, columns, include_industry_dummies=False, include_employment=False):
    """Runs regressions for specified columns and specifications."""
    results_summary = {}

    # If employment is included as control, create log employment variable
    if include_employment:
        df['log_employment'] = np.log(df['Current_Total_Employment'].replace({0: np.nan}).fillna(1e-10))
        # Remove employment from dependent variables if it's being used as control
        columns = [col for col in columns if col != "Current_Total_Employment"]

    for col in columns:
        print(f"\nProcessing column: {col}")
        try:
            # Convert column to numeric and handle missing values
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Add small constant before taking log to handle zeros
            df[f"log_{col}"] = np.log(df[col].replace({0: np.nan}).fillna(1e-10))

            # Dependent variable
            y = df[f"log_{col}"].astype(float)

            # Initialize X with Export_Dummy
            if "Export_Dummy" in df.columns:
                df["Export_Dummy"] = pd.to_numeric(df["Export_Dummy"], errors='coerce').fillna(0).astype(float)
                X = df[["Export_Dummy"]]
            else:
                raise ValueError("Export_Dummy column is missing.")

            # Add employment control if requested
            if include_employment:
                X = pd.concat([X, df[['log_employment']]], axis=1)

            # Add industry dummies if requested
            if include_industry_dummies:
                if "NIC Classification Code" in df.columns:
                    df["NIC Classification Code"] = df["NIC Classification Code"].astype(str)
                    industry_dummies = pd.get_dummies(df["NIC Classification Code"], prefix="Industry", drop_first=True)
                    X = pd.concat([X, industry_dummies], axis=1)
                else:
                    raise ValueError("NIC Classification Code column is missing.")

            # Add intercept
            X = sm.add_constant(X)
            X = X.astype(float)

            # Drop rows with NaN values
            valid_mask = ~(X.isna().any(axis=1) | y.isna())
            X = X[valid_mask]
            y = y[valid_mask]

            print(f"Number of valid observations: {len(y)}")
            print(f"Number of independent variables: {X.shape[1]}")
            
            # Perform regression
            model = sm.OLS(y, X)
            results = model.fit()

            # Store results
            result_dict = {
                "Dependent_Variable": col,
                "Constant_(Intercept)": results.params['const'],
                "Exporter_Dummy_Coefficient": results.params.get('Export_Dummy', np.nan),
                "Exporter_Dummy_P_Value": results.pvalues.get('Export_Dummy', np.nan),
                "R_squared": results.rsquared,
                "Adjusted_R_squared": results.rsquared_adj,
                "Number_of_observations": len(y),
                "Number_of_variables": X.shape[1],
                "F_statistic": results.fvalue,
                "F_pvalue": results.f_pvalue
            }

            if include_employment:
                result_dict["Log_Employment_Coefficient"] = results.params.get('log_employment', np.nan)
                result_dict["Log_Employment_P_Value"] = results.pvalues.get('log_employment', np.nan)

            if include_industry_dummies:
                industry_cols = [col for col in X.columns if col.startswith('Industry_')]
                for ind_col in industry_cols:
                    result_dict[f"{ind_col}_Coefficient"] = results.params.get(ind_col, np.nan)
                    result_dict[f"{ind_col}_P_Value"] = results.pvalues.get(ind_col, np.nan)
            
            results_summary[col] = result_dict

        except Exception as e:
            print(f"Error in regression for {col}: {str(e)}")
            continue
            
    return results_summary

def save_results(results_summary, output_file):
    """Saves the regression results to a CSV file."""
    results_df = pd.DataFrame.from_dict(results_summary, orient='index')
    results_df.to_csv(output_file)
    print(f"\nResults saved to {output_file}")

def main():
    """Main function to run the analysis."""
    args = parse_arguments()

    columns = [
        "Current_Total_Employment", "Current_Total_Annual_Sales", "Value_Added_per_Worker",
        "tfp_lp", "Wage per Worker", "Capital_per_Worker", "Skill_Per_Worker",
        "min_distance_to_GQ", "distance_to_Delhi_Meerut", "distance_to_WDFC", "distance_to_EDFC"
    ]

    print(f"Loading data from {args.file}")
    try:
        df = pd.read_csv(args.file)
    except FileNotFoundError:
        print(f"Error: Could not find file '{args.file}'")
        return
    except Exception as e:
        print(f"Error loading file: {str(e)}")
        return

    print("Running regressions with specifications:")
    print(f"- Industry dummies: {'Yes' if args.industry_dummies else 'No'}")
    print(f"- Log employment control: {'Yes' if args.employment_control else 'No'}")

    results = run_regression(df, columns,
                             include_industry_dummies=args.industry_dummies,
                             include_employment=args.employment_control)

    for col, summary in results.items():
        print(f"\nRegression Results for {col}:")
        print(f"Constant (Intercept): {summary['Constant_(Intercept)']:.4f}")
        print(f"Exporter Dummy Coefficient: {summary['Exporter_Dummy_Coefficient']:.4f}")
        print(f"Exporter Dummy P-Value: {summary['Exporter_Dummy_P_Value']:.4f}")
        if args.employment_control:
            print(f"Log Employment Coefficient: {summary['Log_Employment_Coefficient']:.4f}")
            print(f"Log Employment P-Value: {summary['Log_Employment_P_Value']:.4f}")
        print(f"R-squared: {summary['R_squared']:.4f}")
        print(f"Adjusted R-squared: {summary['Adjusted_R_squared']:.4f}")
        print(f"Number of observations: {summary['Number_of_observations']}")
        print(f"F-statistic: {summary['F_statistic']:.4f}")
        print(f"F-statistic p-value: {summary['F_pvalue']:.4f}")
        print("="*80)

    save_results(results, args.output)

if __name__ == "__main__":
    main()
