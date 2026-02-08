import httpx
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ShopifyIntegration:
    """Integration with Shopify API"""
    
    def __init__(self, api_key: str, api_secret: str, shop_domain: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.shop_domain = shop_domain
        self.base_url = f"https://{shop_domain}/admin/api/2024-01"
    
    async def get_customers(self, limit: int = 250) -> List[Dict]:
        """Fetch customers from Shopify"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/customers.json",
                    params={"limit": limit},
                    auth=(self.api_key, self.api_secret)
                )
                response.raise_for_status()
                data = response.json()
                return data.get("customers", [])
        except Exception as e:
            logger.error(f"Error fetching Shopify customers: {str(e)}")
            return []
    
    async def get_orders(self, customer_id: str, limit: int = 250) -> List[Dict]:
        """Fetch orders for a customer from Shopify"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/orders.json",
                    params={"customer_id": customer_id, "limit": limit, "status": "any"},
                    auth=(self.api_key, self.api_secret)
                )
                response.raise_for_status()
                data = response.json()
                return data.get("orders", [])
        except Exception as e:
            logger.error(f"Error fetching Shopify orders: {str(e)}")
            return []
    
    def transform_customer_data(self, shopify_customer: Dict) -> Dict:
        """Transform Shopify customer data to ChurnGuard format"""
        return {
            'external_id': str(shopify_customer.get('id')),
            'email': shopify_customer.get('email', ''),
            'name': f"{shopify_customer.get('first_name', '')} {shopify_customer.get('last_name', '')}".strip(),
            'total_orders': shopify_customer.get('orders_count', 0),
            'total_spent': float(shopify_customer.get('total_spent', 0))
        }
    
    def transform_order_data(self, shopify_order: Dict) -> Dict:
        """Transform Shopify order data to ChurnGuard format"""
        return {
            'external_id': str(shopify_order.get('id')),
            'customer_id': str(shopify_order.get('customer', {}).get('id')),
            'amount': float(shopify_order.get('total_price', 0)),
            'items_count': len(shopify_order.get('line_items', [])),
            'discount_amount': float(shopify_order.get('total_discounts', 0)),
            'transaction_date': datetime.fromisoformat(shopify_order.get('created_at', '').replace('Z', '+00:00')),
            'status': shopify_order.get('financial_status', 'pending')
        }


class WooCommerceIntegration:
    """Integration with WooCommerce API"""
    
    def __init__(self, api_key: str, api_secret: str, store_url: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.store_url = store_url.rstrip('/')
        self.base_url = f"{self.store_url}/wp-json/wc/v3"
    
    async def get_customers(self, per_page: int = 100) -> List[Dict]:
        """Fetch customers from WooCommerce"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/customers",
                    params={"per_page": per_page},
                    auth=(self.api_key, self.api_secret)
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching WooCommerce customers: {str(e)}")
            return []
    
    async def get_orders(self, customer_id: str, per_page: int = 100) -> List[Dict]:
        """Fetch orders for a customer from WooCommerce"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/orders",
                    params={"customer": customer_id, "per_page": per_page},
                    auth=(self.api_key, self.api_secret)
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching WooCommerce orders: {str(e)}")
            return []
    
    def transform_customer_data(self, woo_customer: Dict) -> Dict:
        """Transform WooCommerce customer data to ChurnGuard format"""
        return {
            'external_id': str(woo_customer.get('id')),
            'email': woo_customer.get('email', ''),
            'name': f"{woo_customer.get('first_name', '')} {woo_customer.get('last_name', '')}".strip(),
            'total_orders': woo_customer.get('orders_count', 0),
            'total_spent': float(woo_customer.get('total_spent', 0))
        }
    
    def transform_order_data(self, woo_order: Dict) -> Dict:
        """Transform WooCommerce order data to ChurnGuard format"""
        return {
            'external_id': str(woo_order.get('id')),
            'customer_id': str(woo_order.get('customer_id')),
            'amount': float(woo_order.get('total', 0)),
            'items_count': len(woo_order.get('line_items', [])),
            'discount_amount': float(woo_order.get('discount_total', 0)),
            'transaction_date': datetime.fromisoformat(woo_order.get('date_created', '').replace('Z', '+00:00')),
            'status': woo_order.get('status', 'pending')
        }
