import pandas as pd

# Assuming the input file is named 'classified_classfn.csv'
# df = pd.read_csv('classified_classfn.csv')
# For demonstration, let's assume 'df' is a pre-existing DataFrame with a column 'Main Manufacturing Activity'

# Define the classification dictionary based on the list
classification_dict = {
    "10": "Manufacture of food products",
    "11": "Manufacture of beverages",
    "12": "Manufacture of tobacco products",
    "13": "Manufacture of textiles",
    "14": "Manufacture of wearing apparel",
    "15": "Manufacture of leather and related products",
    "16": "Manufacture of wood and products of wood and cork",
    "17": "Manufacture of paper and paper products",
    "18": "Printing and reproduction of recorded media",
    "19": "Manufacture of coke and refined petroleum products",
    "20": "Manufacture of chemicals and chemical products",
    "21": "Manufacture of pharmaceuticals, medicinal chemical, and botanical products",
    "22": "Manufacture of rubber and plastics products",
    "23": "Manufacture of other non-metallic mineral products",
    "24": "Manufacture of basic metal",
    "25": "Manufacture of fabricated metal products, except machinery and equipment",
    "26": "Manufacture of computer, electronic and optical products",
    "27": "Manufacture of electrical equipment",
    "28": "Manufacture of machinery and equipment n.e.c",
    "29": "Manufacture of motor vehicles, trailers, and semi-trailers",
    "30": "Manufacture of other transport equipment",
    "31": "Manufacture of furniture",
    "32": "Other manufacturing",
    "33": "Repair and installation of machinery and equipment"
}

# Function to classify each entry based on keywords in the activity description
def classify_activity(activity):
    if not isinstance(activity, str):
        return "Unclassified"
    activity = activity.lower()
    if "food" in activity or "bakery" in activity:
        return "10"
    elif "beverage" in activity or "brewery" in activity:
        return "11"
    elif "tobacco" in activity:
        return "12"
    elif "textile" in activity or "cotton" in activity or "garment" in activity:
        return "13"
    elif "wearing apparel" in activity or "clothing" in activity or "suit" in activity:
        return "14"
    elif "leather" in activity or "footwear" in activity:
        return "15"
    elif "wood" in activity or "timber" in activity:
        return "16"
    elif "paper" in activity or "print" in activity:
        return "17"
    elif "recorded media" in activity:
        return "18"
    elif "coke" in activity or "petroleum" in activity:
        return "19"
    elif "chemical" in activity:
        return "20"
    elif "pharmaceutical" in activity or "medicine" in activity:
        return "21"
    elif "plastic" in activity or "rubber" in activity:
        return "22"
    elif "non-metallic mineral" in activity:
        return "23"
    elif "metal" in activity and "basic" in activity:
        return "24"
    elif "fabricated metal" in activity:
        return "25"
    elif "computer" in activity or "electronic" in activity:
        return "26"
    elif "electrical equipment" in activity:
        return "27"
    elif "machinery" in activity or "equipment" in activity:
        return "28"
    elif "motor vehicle" in activity or "trailer" in activity:
        return "29"
    elif "transport equipment" in activity:
        return "30"
    elif "furniture" in activity:
        return "31"
    elif "manufacturing" in activity:
        return "32"
    elif "repair" in activity or "installation" in activity:
        return "33"
    else:
        return "Unclassified"

# Apply classification to each entry in the dataframe
# df['Classification Code'] = df['Main Manufacturing Activity'].apply(classify_activity)

# Map classification code to description
# df['Classification Description'] = df['Classification Code'].map(classification_dict)

# Save the classified data to a new CSV file
# classified_file_path = 'classified_classfn.csv'
# df.to_csv(classified_file_path, index=False)
