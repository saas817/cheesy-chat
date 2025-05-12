# Identity
Hello. Now I am developing ChatGPT project that provides brief information about cheese based on RAG. RAG engine is pinecone and it uses data from web scraping. ChatGPT framework is openai.
As you know, to upsert data into pinecone, it is necessary to embed chunk text. But because the data is coming from web scraping, I have only json data, not raw text at all.
So I want you to create effective text from json data I give so that my project, i.e. pinecone works well.

# Some examples of json data.

### Example 1
    {
        "showImage": "https://d3tlizm80tjdt4.cloudfront.net/remote_images/image/2114/small/b41784f854f03efedc29d73d0a248d0dac389d704b7101205d.jpg",
        "name": "Cheese, Mozzarella, Wmlm, Feather Shred, Nb, 4/5 Lb - 124254",
        "brand": "North Beach",
        "department": "Specialty Cheese",
        "itemCounts": {
            "EACH": "1 Item"
        },
        "dimensions": {
            "EACH": "L 1\" x W 1\" x H 1\""
        },
        "weights": {
            "EACH": "20 lbs"
        },
        "images": [
            "https://d3tlizm80tjdt4.cloudfront.net/remote_images/image/2114/small/b41784f854f03efedc29d73d0a248d0dac389d704b7101205d.jpg"
        ],
        "relateds": [],
        "prices": {
            "Each": "53.98"
        },
        "pricePer": "$2.70/lb",
        "sku": "124254",
        "discount": "",
        "empty": false,
        "href": "https://shop.kimelo.com/sku/cheese-mozzarella-wmlm-feather-shred-nb-45-lb-124254/124254",
        "priceOrder": 38,
        "porpularityOrder": 1
    }

### Example 2
    {
        "showImage": "https://d3tlizm80tjdt4.cloudfront.net/image/10347/image/sm-e678c1718263a65a402310e22e32ac8a.jpg",
        "name": "Cheese, Cheddar, Sharp, Slcd, Interleaf, 0.75 Oz, (8)  103603",
        "brand": "California Select Farms",
        "department": "Sliced Cheese",
        "itemCounts": {
            "CASE": "8 Eaches",
            "EACH": "1 Item"
        },
        "dimensions": {
            "CASE": "L 1\" x W 1\" x H 1\"",
            "EACH": "L 1\" x W 1\" x H 1\""
        },
        "weights": {
            "CASE": "1.5 lbs",
            "EACH": "0.1875 lbs"
        },
        "images": [
            "https://d3tlizm80tjdt4.cloudfront.net/image/10347/image/sm-e678c1718263a65a402310e22e32ac8a.jpg"
        ],
        "relateds": [
            "103600",
            "106815"
        ],
        "prices": {
            "Case": "76.48",
            "Each": "9.56"
        },
        "pricePer": "$6.37/lb",
        "sku": "103603",
        "discount": "",
        "empty": false,
        "href": "https://shop.kimelo.com/sku/cheese-cheddar-sharp-slcd-interleaf-075-oz-8-103603/103603",
        "priceOrder": 91,
        "porpularityOrder": 52
    }

### Example 3
    {
        "showImage": "https://d3tlizm80tjdt4.cloudfront.net/image/13860/image/sm-1505a5e7aa7570e69e7ca77cf4c49a97.png",
        "name": "Cheese, Blend, Mozz, Wm & Ps, Premio Shred, 6/5 Lb - 112492",
        "brand": "Galbani Premio",
        "department": "Shredded Cheese",
        "itemCounts": {
            "EACH": "1 Item"
        },
        "dimensions": {
            "EACH": "L 1\" x W 1\" x H 1\""
        },
        "weights": {
            "EACH": "30 lbs"
        },
        "images": [
            "https://d3tlizm80tjdt4.cloudfront.net/image/13860/image/sm-1505a5e7aa7570e69e7ca77cf4c49a97.png"
        ],
        "relateds": [],
        "prices": {
            "Each": "101.51"
        },
        "pricePer": "$3.38/lb",
        "sku": "112492",
        "discount": "Buy 10+ pay $98.46",
        "empty": false,
        "href": "https://shop.kimelo.com/sku/cheese-blend-mozz-wm-ps-premio-shred-65-lb-112492/112492",
        "priceOrder": 18,
        "porpularityOrder": 60
    }

# Description

I will give you description about the fields of json data.
### showImage
This is url of preview image.
### name
This is full name of cheese.
### brand
This is brand of cheese.
### department
This is category of cheese.
### itemCounts
This is a number of items per unit. The unit is "EACH" or "CASE", and "CASE" is optional.
"EACH" means each item, i.e, the value of it is almost-always 1.  For example,  {"CASE": "4 Eaches", "EACH": "1 Item"} means one "CASE" has 4 * 1 = 4 items.
### dimensions
This is dimensions of one unit. The unit is the same as itemCount.
### weights
This is weight of one unit. The unit is the same as itemCount.
### images
This is an array of reference images of cheese.
### relateds
This is an array of skus of other cheeses that has relation to this cheese.
### prices
This is prices per unit. The unit is the same as itemCount. When user normally say about price, it means the first value, the price of "EACH".
### pricePer
This is price per weight unit. The weight unit can be one of lb, ct and so on.
### sku
This is Stock Keeping Unit of cheese.
### discount
This is a discount anounce. If there is no discount, this value will be empty string.
### empty
This is a boolean value that refers if there is no this kind of cheese at shop at all.
### href
This is a link of cheese.
### priceOrder
This is the order of cheese in Price Highest First sort.
### popularityOrder
This is the order of cheese in Popularity sort.

# Instructions
- The result text must contain all information of json.
- The result text must not be too long or too short. About 7~8 sentences.
- The result text must be embedding-friendly, i.e, the embedding vector of it must be semantic-clear. The embedding model is "text-embedding-3-small" of OpenAI.

Now I will give you one json data. Give me only perfect description text, not any other text at all.
