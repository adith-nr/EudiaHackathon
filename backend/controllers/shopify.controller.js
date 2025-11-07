import shopifyService from '../services/shopify.service.js';
import fastapiService from '../services/fastapi.service.js';
import dotenv from "dotenv";
dotenv.config()


export async function createProduct(req,res,next) {
  try {
    const url = `https://${process.env.SHOPIFY_STORE}/admin/api/2024-10/products.json`;
    const title = req.title
    const body_html= req.body_html
    const vendor= req.vendor
    const product_type= req.product_type
    const price= req.price
    const sku= req.sku

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
      `https://${SHOPIFY_STORE}/admin/api/2024-10/locations.json`,
      { headers: { "X-Shopify-Access-Token": ACCESS_TOKEN } }
    );

    const location_id = locRes.data.locations[0].id;

    
    const url = `https://${SHOPIFY_STORE}/admin/api/2024-10/inventory_levels/set.json`;
    const payload = {
      location_id,
      inventory_item_id,
      available: quantity
    };

    const response = await axios.post(url, payload, {
      headers: {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
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

