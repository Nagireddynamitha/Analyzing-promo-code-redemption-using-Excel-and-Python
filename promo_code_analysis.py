import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

df = pd.read_csv("transaction_data.csv")
print(df.head())
print(df.columns)

analysis = df.groupby("promo_codes")["redeemed"].agg(
     total_targeted="count",
      total_used="sum"
)

analysis["redemption_rate"] = analysis["total_used"] / analysis["total_targeted"]
print("\nSummary Table:")
print(analysis)

# Create contingency table 
contingency_table = [
    [
        analysis.iloc[0]["total_used"],
        analysis.iloc[0]["total_targeted"] - analysis.iloc[0]["total_used"] ],
    [
        analysis.iloc[1]["total_used"],
        analysis.iloc[1]["total_targeted"] - analysis.iloc[1]["total_used"]
    ]]
#  Chi-square test
chi2, p, dof, expected = chi2_contingency(contingency_table)

print("\nChi-square Results:")
print("Chi-square value:", chi2)
print("P-value:", p)
print("Degrees of freedom:", dof)
#bar chart
plt.figure()
plt.bar(analysis.index, analysis["redemption_rate"] * 100)
plt.xlabel("Promo Code")
plt.ylabel("Redemption Rate (%)")
plt.title(f"Promo Code Redemption Rate\np-value = {p:.4f}")
plt.savefig("redemption_rate.png")
plt.show()
