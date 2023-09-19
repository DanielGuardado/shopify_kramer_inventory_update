from shopify_api import get_variants_by_vendor, update_inventory
from ftp_data import FTPDataLoader
from config import FTP_USER
import pandas as pd
import traceback
from email_helper import send_email


def main():
    vendor_name = "Smartliner USA"
    sku_data = get_variants_by_vendor(vendor_name)
    loader = FTPDataLoader(FTP_USER)
    df_csv = loader.get_ftp_file_as_dataframe()
    df_shopify = pd.DataFrame(sku_data)
    df_merged = pd.merge(df_shopify, df_csv, left_on="sku", right_on="SKU", how="left")

    df_inv_available = df_merged[["sku", "inventory_item_id", "Qty"]]

    for _, row in df_inv_available.iterrows():
        print(f"Updating {row['sku']} to {row['Qty']}")
        update_inventory(row["inventory_item_id"], row["Qty"])


if __name__ == "__main__":
    try:
        main()
    except:
        send_email("Error updating kramer america inventory", traceback.format_exc())
