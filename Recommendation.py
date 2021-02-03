"""
@author: Linh Vo
@purpose: This program creates recommendations for someone who has just bought a product, based on which items are often bought together with the product.
"""

import numpy as np
import pandas as pd
import os

# Function to create a purchase summary
def fillPeopleProducts(purchasedf):
    """
    Parameters:
    purchasedf - a data frame storing the purchasing data.
    Returns a new data frame summarizing which products were bought by which customer.
    """
    # Create a new data frame with the purchase count for each user
    purchaseSummary = pd.DataFrame(
        purchasedf.groupby(["USER_ID", "PRODUCT_ID"]).count()["PURCHASE"]
    )
    # Format data frame to have users as rows and products as columns
    peopleProducts = pd.pivot_table(
        purchaseSummary,
        values="PURCHASE",
        index=["USER_ID"],
        columns=["PRODUCT_ID"],
        fill_value=0,
    )
    # Remove column and row labels strings from data frame
    peopleProducts = peopleProducts.rename_axis(None).rename_axis(None, axis=1)
    return peopleProducts


# Function to create co-purchasing matrix
def fillProductCoPurchase(purchasedf):
    """
    Parameters:
    purchasedf - a data frame storing the purchasing data.
    Returns a tuple consisting of the co-purchasing matrix dataframe and the peopleProducts data frame.
    """
    # Get a list of unique product IDs
    prodCols = sorted(list(set(purchasedf["PRODUCT_ID"])))
    # Create a new data frame for co-purchasing matrix with product IDs as both columns and rows
    # and fill values with zeros
    coPurchaseMatrix = pd.DataFrame(data=0, columns=prodCols, index=prodCols)
    # Call function to create purchase summary
    peopleProducts = fillPeopleProducts(purchasedf)

    for product_i in coPurchaseMatrix.columns:
        for product_j in coPurchaseMatrix.index:
            if product_i != product_j:
                # Calculate co-purchase score for the product pair
                copurchaseValue = np.sum(
                    peopleProducts[product_i] * peopleProducts[product_j]
                )
                # Fill values for co-purchasing matrix from purchase summary
                coPurchaseMatrix.loc[product_i, product_j] = copurchaseValue

    return coPurchaseMatrix, peopleProducts


# Function to find recommended product IDs
def findRecProdIDs(coPurchaseMatrix, purchasedProd):
    """
    Parameters:
    coPurchaseMatrix - a data frame representing the co-purchasing matrix.
    purchasedProd - a string for purchased product ID.
    Returns:
    A list of items that people are most likely to buy with the purchased product.
    An integer for the maximum co-purchasing score.
    """
    maxCoPurchaseScore = coPurchaseMatrix[purchasedProd].max()
    # Filter co-purchase matrix to only product pairs with maximum co-purchase score
    recProdMatrix = coPurchaseMatrix[
        coPurchaseMatrix[purchasedProd] == maxCoPurchaseScore
    ]
    # Get a list of recommended product IDs that have maximum co-purchase score
    recProdList = recProdMatrix.index.to_list()
    return recProdList, maxCoPurchaseScore


# Function to find items that are most bought by users
def findMostBought(peopleProducts):
    """
    Parameters:
    peopleProducts - a data frame summarizing which products were bought by which customer.
    Returns a list of items that have been purchased by more customers than any other item.
    """
    # Get the total number of purchases for each product
    totalPurchase = peopleProducts.sum(axis=0)
    # Filter to get only product with highest number of purchases
    mostBoughtProd = totalPurchase[totalPurchase == totalPurchase.max()]
    # Get a list of most bought product IDs
    mostBoughtProd = mostBoughtProd.index.to_list()
    return mostBoughtProd


# Function to format product data
def reformatProdData(productdf):
    """
    Parameters:
    productdf - a data frame storing the product data.
    Returns no value.
    """
    # Get category data from "DESCRIPTION" column
    productdf["CATEGORY"] = productdf.DESCRIPTION.str.split(pat="(", n=1).str.get(1)
    # Keep only the category text and remove parentheis
    productdf["CATEGORY"] = productdf.CATEGORY.str.rsplit(pat=")", n=1).str.get(0)
    # Remove white spaces and parentheis in "DESCRIPTION" column
    productdf["DESCRIPTION"] = (
        productdf.DESCRIPTION.str.split(pat="(").str.get(0).str.strip()
    )
    # Reformat price column
    productdf["PRICE"] = pd.to_numeric(productdf["PRICE"], errors="coerce")
    productdf["PRICE"].fillna(value=0, inplace=True)


# Function to format printout of recommended products
def printRecProducts(productdf, recProdIDs):
    """
    Parameters:
    productdf - a data frame storing the product data.
    recProdIDs - a list of recommended product ids.
    Returns no value.
    """
    # Filter data frame to keep only recommended product IDs
    recProducts = productdf[productdf["PRODUCT_ID"].isin(recProdIDs)]
    # Sort data frame by categories
    recProducts = recProducts.sort_values(by=["CATEGORY"])
    # Get the maximum length of category strings to help with formatting
    maxLength = recProducts["CATEGORY"].str.len().max()

    for row in recProducts.itertuples():
        # Only display price if price is available
        if row.PRICE != 0:
            print(
                "IN",
                row.CATEGORY.ljust(maxLength).upper(),
                "--",
                row.DESCRIPTION + ",",
                "$" + format(row.PRICE, "10.2f").strip(),
            )
        else:
            print("IN", row.CATEGORY.ljust(maxLength).upper(), "--", row.DESCRIPTION)


def main():
    # Get folder name and import data files
    folderName = input(
        "Please enter the name of folder with product and purchase data files: (prod.csv and purchases.csv): "
    )
    purchasedf = pd.read_csv(os.path.join(os.getcwd(), folderName, "purchases.csv"))
    productdf = pd.read_csv(os.path.join(os.getcwd(), folderName, "prod.csv"))
    # Convert all product IDs to uppercase for consistency
    purchasedf["PRODUCT_ID"] = purchasedf["PRODUCT_ID"].str.upper()
    productdf["PRODUCT_ID"] = productdf["PRODUCT_ID"].str.upper()

    # Get a list of unique product IDs
    allProd = sorted(list(set(productdf["PRODUCT_ID"])))

    # Process data to get neccessary information
    print("\nPreparing the co-purchasing matrix...\n")
    coPurchaseMatrix, peopleProducts = fillProductCoPurchase(purchasedf)
    mostBoughtProd = findMostBought(peopleProducts)
    reformatProdData(productdf)

    # Get bought product ID
    productID = (
        input("Which product was bought? Enter product id or press enter to quit. ")
        .strip()
        .upper()
    )

    # Continue to ask for input if user doesn't press Enter
    while productID != "":
        if productID in allProd:
            # Get co-purchase score and list of recommended product IDs
            likelyToBuyList, maxCoPurchaseScore = findRecProdIDs(
                coPurchaseMatrix, productID
            )
            print(f"[Maximum co-purchasing score {maxCoPurchaseScore}]")

            if maxCoPurchaseScore == 0:
                # Recommend most popular products in general
                recProductList = mostBoughtProd
                recommendType = "Suggest one of our most popular products:\n"
            else:
                # Recommend most likely to buy together products
                recProductList = likelyToBuyList
                recommendType = "People who bought it were most likely to buy:\n"

            print("Recommend with", productID, ":", recProductList)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(recommendType)
            printRecProducts(productdf, recProductList)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        productID = (
            input("Which product was bought? Enter product id or press enter to quit. ")
            .strip()
            .upper()
        )

    # End the program when user presses Enter
    print("Bye!")


main()
