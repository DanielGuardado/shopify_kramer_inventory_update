import requests
from config import API_KEY, LOCATION_ID

# Define your store and authentication details
store_url = "https://xtremematsunder.myshopify.com"
headers = {
    "X-Shopify-Access-Token": API_KEY,
}


def get_variants_by_vendor(vendor_name):
    """Retrieve all the variant_ids and inventory item ids for a given vendor."""
    endpoint = f"{store_url}/admin/api/2023-07/products.json?vendor={vendor_name}&fields=variants"
    sku_data = []

    while endpoint:
        response = requests.get(endpoint, headers=headers)
        data = response.json()

        if not data.get("products"):
            break  # Exit the loop if no more products are returned

        for product in data["products"]:
            for variant in product["variants"]:
                sku = {
                    "sku": variant["sku"],
                    "variant_id": variant["id"],
                    "inventory_item_id": variant["inventory_item_id"],
                }
                sku_data.append(sku)

        # If the vendor's products weren't fully retrieved in the current batch, continue to the next page
        link_header = response.headers.get("Link")
        if link_header and 'rel="next"' in link_header:
            # Extract the next page URL from the Link header
            next_link = link_header.split(";")[0].strip("<>")
            endpoint = next_link
        else:
            endpoint = None  # No more pages to process

    return sku_data


def update_inventory(inventory_item_id, available):
    """Update the inventory for an item."""
    endpoint = f"{store_url}/admin/api/2023-07/inventory_levels/set.json"
    data = {
        "location_id": LOCATION_ID,
        "inventory_item_id": inventory_item_id,
        "available": available,
    }
    response = requests.post(endpoint, headers=headers, json=data)
    return response.json()
