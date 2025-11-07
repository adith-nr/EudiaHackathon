
import fastapiService from '../services/fastapi.service.js';
import dotenv from "dotenv";
dotenv.config()
import axios from 'axios';

export async function createProduct(req,res,next) {
  try {
    const url = `https://${process.env.SHOPIFY_STORE}/admin/api/2024-10/products.json`;
    const {title,body_html,vendor,product_type,price,sku} = req.body;
    

    const productData = {
      product: {
        title: title,
        body_html: body_html,
        vendor: vendor,
        product_type: product_type,
        variants: [
          {
            option1: "Standard",
            price: price,
            sku: sku,
          },
        ],
      },
    };

    const response = await axios.post(url, productData, {
      headers: {
        "X-Shopify-Access-Token": process.env.ACCESS_TOKEN,
        "Content-Type": "application/json",
      },
    });

    console.log(" Product created:", response.data.product);
    res.json({
      message: " Product created successfully!",
      product: response.data.product,
    });
  } catch (error) {
    console.error(" Error creating product:", error.response?.data || error.message);
    res.status(500).json({ error: "Failed to create product." });
}
}

export async function UpdateInventory(req,res,next) {
  try {
    const { variant_id, inventory_item_id, quantity } = req.body;    
    await axios.put(
      `https://${process.env.SHOPIFY_STORE}/admin/api/2024-10/variants/${variant_id}.json`,
      {
        variant: {
          id: variant_id,
          inventory_management: "shopify"
        }
      },
      {
        headers: {
          "X-Shopify-Access-Token": process.env.ACCESS_TOKEN,
          "Content-Type": "application/json"
        }
      }
    );

    console.log("Inventory tracking enabled for variant:", variant_id);

    
    const locRes = await axios.get(
      `https://${process.env.SHOPIFY_STORE}/admin/api/2024-10/locations.json`,
      { headers: { "X-Shopify-Access-Token": process.env.ACCESS_TOKEN } }
    );

    const location_id = locRes.data.locations[0].id;

    
    const url = `https://${process.env.SHOPIFY_STORE}/admin/api/2024-10/inventory_levels/set.json`;
    const payload = {
      location_id,
      inventory_item_id,
      available: quantity
    };

    const response = await axios.post(url, payload, {
      headers: {
        "X-Shopify-Access-Token": process.env.ACCESS_TOKEN,
        "Content-Type": "application/json"
      },
    });

    console.log("📦 Inventory updated:", response.data);
    res.json({
      message: "Inventory tracking enabled and quantity updated!",
      data: response.data,
    });

  } catch (error) {
    console.error(" Error updating inventory:", error.response?.data || error.message);
    res.status(500).json({ error: "Failed to update inventory" });
  }
}

export async function getOrderData(req,res,next) {
  try {
    const url = `https://${process.env.SHOPIFY_STORE}/admin/api/2024-10/orders.json?status=any`;
    
    const response = await axios.get(url, {
      headers: {
        "X-Shopify-Access-Token": process.env.ACCESS_TOKEN,
        "Content-Type": "application/json",
      },
    });

    const orders = response.data.orders;

    const totalSales = orders.reduce(
      (sum, order) => sum + parseFloat(order.total_price),
      0
    );
   
    res.json({
      message: " Orders retrieved successfully",
      count: orders.length,
      totalSales,
      recentOrders: orders.map((order) => ({
        id: order.id,
        name: order.line_items[0].name,
        sku:order.line_items[0].sku,
        createdAt: order.created_at,
        totalPrice: order.total_price,
        currency: order.currency,
        customer: order.customer?.first_name || "Guest",
      })),
    });
  } catch (error) {
    console.error(" Error fetching orders:", error.response?.data || error.message);
    res.status(500).json({ error: "Failed to fetch orders" });
  }
}

export async function createPriceExperiment(req, res, next) {
  try {
    const payload = req.body;
    const validated = fastapiService.validateAgentPayload(payload);
    const job = await fastapiService.dispatchPricingExperiment(validated);
    res.status(202).json({ jobId: job.id, status: 'queued' });
  } catch (error) {
    next(error);
  }
}





export async function getOrdersByProduct(req, res) {
  try {
    const { sku, title } = req.body; // You can query by SKU or product title
    const SHOPIFY_STORE = process.env.SHOPIFY_STORE;
    const ACCESS_TOKEN = process.env.ACCESS_TOKEN;

    if (!sku && !title) {
      return res.status(400).json({ error: "Please provide sku or title as query param" });
    }

    // 🧠 GraphQL query for orders containing a product with this SKU/title
    const query = `
      {
        orders(first: 20, query: "line_items.${sku ? `sku:'${sku}'` : `name:'${title}'`}") {
          edges {
            node {
              id
              name
              createdAt
              financialStatus
              fulfillmentStatus
              currentSubtotalPriceSet {
                shopMoney { amount currencyCode }
              }
              customer {
                firstName
                lastName
                email
              }
              lineItems(first: 10) {
                edges {
                  node {
                    name
                    sku
                    quantity
                    product {
                      id
                      title
                    }
                    variant {
                      id
                      title
                    }
                  }
                }
              }
            }
          }
        }
      }
    `;

    const response = await axios.post(
      `https://${SHOPIFY_STORE}/admin/api/2024-10/graphql.json`,
      { query },
      {
        headers: {
          "X-Shopify-Access-Token": ACCESS_TOKEN,
          "Content-Type": "application/json",
        },
      }
    );
    console.log(response.data)

    const orders = response.data.data.orders.edges.map(edge => edge.node);

    res.json({
      total_orders: orders.length,
      orders,
    });
  } catch (error) {
    console.error("❌ Error fetching orders via GraphQL:", error.response?.data || error.message);
    res.status(500).json({
      error: "Failed to fetch order details for the given product",
      details: error.response?.data || error.message,
    });
  }
}
