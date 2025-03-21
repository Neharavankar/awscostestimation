import boto3
import json
from botocore.exceptions import BotoCoreError, ClientError

# 🔹 Change the service name here (AmazonEC2, AmazonS3, AmazonRDS, etc.)
SERVICE_CODE = 'AmazonDynamoDB'  
REGION = 'Asia Pacific (Mumbai)'  # Change the AWS region if needed

def get_pricing(service_code, region):
    try:
        # Initialize AWS Pricing API Client
        pricing_client = boto3.client('pricing', region_name='us-east-1')

        # Define filters for region
        filters = [{'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region}]

        # Retrieve pricing information
        response = pricing_client.get_products(ServiceCode=service_code, Filters=filters)

        # Parse and display pricing details
        for price_item in response['PriceList']:
            product = json.loads(price_item)
            attributes = product['product']['attributes']
            sku = product['product']['sku']
            instance_type = attributes.get('instanceType', 'N/A')
            location = attributes.get('location', 'N/A')
            storage_class = attributes.get('storageClass', 'N/A')

            price_dimensions = list(product['terms']['OnDemand'].values())[0]['priceDimensions']
            price_per_unit = list(price_dimensions.values())[0]['pricePerUnit'].get('USD', 'N/A')

            # Convert price per unit to hourly if applicable
            if price_per_unit != 'N/A':
                price_per_hour = float(price_per_unit)
                price_per_hour = f"{price_per_hour:.8f}"
            else:
                price_per_hour = 'N/A'

            print(f"Service: {service_code}")
            print(f"SKU: {sku}")
            print(f"Instance Type: {instance_type}")
            print(f"Storage Class: {storage_class}")
            print(f"Region: {location}")
            print(f"Price per Unit (USD): ${price_per_unit}")
            print(f"Price per Hour (USD): ${price_per_hour}")
            print("-" * 40)

    except (BotoCoreError, ClientError) as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    print(f"Fetching AWS Pricing Data for {SERVICE_CODE} in {REGION}...\n")
    get_pricing(SERVICE_CODE, REGION)
