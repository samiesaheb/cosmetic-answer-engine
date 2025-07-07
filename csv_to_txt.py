import pandas as pd
from pathlib import Path

# Load CSV
df = pd.read_csv("formulations_cleaned.csv")

# Group by product
grouped = df.groupby("product_name")

# Create documents folder if it doesn't exist
Path("documents").mkdir(parents=True, exist_ok=True)

# Output file
with open("documents/formulations.txt", "w", encoding="utf-8") as f:
    for product, group in grouped:
        f.write(f"Product: {product}\n")
        f.write("Ingredients:\n")
        for _, row in group.iterrows():
            ingredient = row['ingredient']
            inci = row['inci']
            percent = row['percent']
            part = row['part']
            f.write(f"- {ingredient} ({inci}) – {percent}% [Part {part}]\n")
        f.write("\n" + "="*60 + "\n\n")

print("✅ formulations.txt generated successfully in /documents/")
