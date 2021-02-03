"""
@author: Linh Vo
@purpose: This program creates a barchart that shows percentage of purchase revenue from buyers in different age groups.
"""

import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt

AGE = "AGE"
PURCHASE = "PURCHASE"
PRODUCT_ID = "PRODUCT_ID"
DESCRIPTION = "DESCRIPTION"
TITLE = "Title"

# Function to set up full display of data frame
def setupDisplay():
    """
    Parameters: None
    Returns no value.
    """
    pd.set_option("display.max_columns", 1000)
    pd.set_option("display.max_rows", 1000)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", 0)


# Function to format product data
def reformatProdData(productdf):
    """
    Parameters:
    productdf - a data frame storing the product data.
    Returns no value.
    """

    # Get product title from DESCRIPTION column
    productdf[TITLE] = (
        productdf[DESCRIPTION].str.split(pat="(", n=1).str.get(0).str.strip()
    )


# Function to handle item selection procedure
def pickItemWithKeyword(keyword, productdf):
    """
    Parameters:
    keyword - a string representing the item keyword that user wants to search for
    productdf - a data frame storing the product data.
    Returns:
    selectedProductID - a string for selected product ID
    selectedProductName - a string for selected product title
    """

    # Filter product data frame to get only products that contain the keyword
    matchProducts = productdf[productdf[TITLE].str.contains(keyword, case=False)][
        [PRODUCT_ID, TITLE]
    ]

    matchCount = len(matchProducts)

    # Change index to 1-based
    matchProducts.index = np.arange(1, matchCount + 1)

    # Default to select the first matched product
    selectedPosition = 1

    # If no match is found, return nothing and stop function
    if matchCount == 0:
        return None, None
    # If there are multiple matched products, ask user to pick item
    elif matchCount > 1:
        print("\nWhich of the following items would you like to pick (enter number)\n")
        print(matchProducts)
        # Update item position to user input
        selectedPosition = eval(input("\nEnter a number: "))

    selectedProductID = matchProducts.loc[selectedPosition][PRODUCT_ID]
    selectedProductName = matchProducts.loc[selectedPosition][TITLE]
    # Print out selected product
    print(f"\n{selectedProductID}: {selectedProductName}\n")

    return selectedProductID, selectedProductName


# Function to calculate purchase percentage by age groups
def calculatePurchaseByAge(selectedProductID, purchasedf):
    """
    Parameters:
    selectedProductID - a string for selected product ID
    purchasedf - a data frame storing the purchase data.
    Returns:
    purchaseByAge - a Series showing total purchases for selected product by age groups.
    purchasePercentage - a data frame containing total purchases and percentage contributed by age groups.
    """

    # Get all age groups in the data
    ageGroup = list(set(purchasedf[AGE]))

    # Calculate the total of all purchases of the selected product by age groups
    purchaseByAge = (
        purchasedf[purchasedf[PRODUCT_ID] == selectedProductID]
        .groupby(by=AGE, dropna=False)[PURCHASE]
        .sum()
    )
    # Display all age groups including the ones with zero purchase and sort based on age groups
    purchaseByAge = purchaseByAge.reindex(ageGroup).fillna(0).sort_index()

    purchasePercentage = pd.DataFrame(data=purchaseByAge)
    # Calculate percentage of all purchases of the selected product each age group contributed
    purchasePercentage["PERCENTAGE"] = (
        purchasePercentage[PURCHASE] / (purchasePercentage[PURCHASE].sum()) * 100
    )
    purchasePercentage["PERCENTAGE"] = purchasePercentage["PERCENTAGE"].round()

    return purchaseByAge, purchasePercentage


# Function to plot bar chart
def plot(purchasePercentage, selectedProductName):
    """
    Parameters:
    purchasePercentage - a data frame containing total purchases and percentage contributed by age groups.
    selectedProductName - a string for selected product title
    Returns no value
    """

    # Set figure size
    plt.figure(figsize=(8, 7))
    chart = plt.bar(
        purchasePercentage.index,
        purchasePercentage.PERCENTAGE,
        color="green",
        align="edge",
    )
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)  # Rotate x axis labels
    plt.xticks(ha="left")  # Align label to the left
    plt.title(
        "Percentage of purchase revenue per age group for\n" + selectedProductName
    )
    plt.ylabel("% of total revenue")
    plt.xlabel("Age group")
    # Display percentage value labels on top of each bar
    for bar in chart.patches:
        plt.annotate(
            text=bar.get_height().astype(str) + "%",
            xy=(bar.get_x(), bar.get_height() + 0.8),
            ha="left",
        )
    plt.savefig("plot.jpg")  # Save figure


def main():
    setupDisplay()

    print("Examine percentage of purchase revenue per age group.\n")

    # Get folder name and import data files
    folderName = input("Please enter the name of the subfolder with the data file: ")
    purchasedf = pd.read_csv(os.path.join(os.getcwd(), folderName, "purchases.csv"))
    productdf = pd.read_csv(os.path.join(os.getcwd(), folderName, "prod.csv"))

    reformatProdData(productdf)

    # Get keyword to look for products
    keyword = input("\nEnter item keyword: ")
    # Find matched products and get selected product ID and title
    selectedProductID, selectedProductName = pickItemWithKeyword(keyword, productdf)

    # Repeat process if no products match with keyword
    while not selectedProductID:
        print(
            "There are no items with",
            "'" + keyword + "'",
            "in the title. Please repeat.",
        )
        keyword = input("\nEnter item keyword: ")
        selectedProductID, selectedProductName = pickItemWithKeyword(keyword, productdf)

    # Calculate purchases and percentages by age groups
    purchaseByAge, purchasePercentage = calculatePurchaseByAge(
        selectedProductID, purchasedf
    )
    # Print out total purchases by age groups
    print(purchaseByAge)

    # Plot bar chart based on purchase percentage
    plot(purchasePercentage, selectedProductName)
    plt.show()


main()
