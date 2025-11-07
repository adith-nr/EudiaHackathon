import os
import pandas
import json
import re
import statistics
from typing import List, Dict, Any, Optional
from serpapi import GoogleSearch
import google.generativeai as genai


test_data = [
  {
    "title": "Gesto Warm White Led Serial String Lights \u2012 Waterproof Copper Wire Yellow Fairy Lights for Home Decoration,Christmas, Deepawali & Diwali Decoration Lights for Balcony Outdoor (19 Meter | Pack of 10)",
    "price": "\u19b91,999",
    "rating": 2.7,
    "reviews": 8799,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B8H7MB9Z3/",
    "thumbnail": "https://m.media-amazon.com/images/I/90vmmUCGuFL._AC_UL320_.jpg"
  },
  {
    "title": "Lexton 39 LED Power Pixel Serial String/Fairy Light | Plug Sourced | Suitable for Home & Outdoor Decoration, Diwali, Christmas, Ramadan, Wedding, Party, Festival (Pack of 1, Warm White)",
    "price": "\u19b979",
    "rating": 2.8,
    "reviews": 11499,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B7RF1VL1D/",
    "thumbnail": "https://m.media-amazon.com/images/I/714OeQNV5PL._AC_UL320_.jpg"
  },
  {
    "title": "35 Feet LED Fairy String Lights \u2013 36 Bulbs on Waterproof Copper Wire | Decorative Lights for Bedroom, Garden, Wedding, Diwali & Christmas Home Decoration (Warm White)",
    "price": "\u19b973.62",
    "rating": 2.8,
    "reviews": 2299,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1CD4CXYGW/",
    "thumbnail": "https://m.media-amazon.com/images/I/70HmgHpqMeL._AC_UL320_.jpg"
  },
  {
    "title": "Lexton Lunar Ultra Bright String Light/Fairy Light | 95 LED, Plug Sourced | Best for Home Decorative, Indoor & Outdoor Decoration, Diwali, Christmas, Wedding Light (Pack of 1, Warm White)",
    "price": "\u19b9299",
    "rating": 3.1,
    "reviews": 75,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1CY2HH493/",
    "thumbnail": "https://m.media-amazon.com/images/I/70hBHWzDWZL._AC_UL320_.jpg"
  },
  {
    "title": "35 Feet LED Fairy String Lights \u2013 36 Bulbs on Waterproof Copper Wire | Decorative Lights for Bedroom, Garden, Wedding, Diwali & Christmas Home Decoration (Warm White)",
    "price": "\u19b973.62",
    "rating": 2.8,
    "reviews": 2299,
    "description": "LED",
    "url": "https://www.amazon.in/NIYAMAX-LED-String-Lights-Waterproof/dp/B-1CD4CXYGW/",
    "thumbnail": "https://m.media-amazon.com/images/I/70HmgHpqMeL._AC_UL320_.jpg"
  },
  {
    "title": "Desidiya \u037777777777ae Plastic 12 Meter LED Decorative String Fairy Rice Lights for Home Decoration Indoor and Outdoor Decoration Lights, Festival, Party, Garden, Wedding (Multicolor)(Pack of 1)",
    "price": "\u19b978",
    "rating": 2.9,
    "reviews": 8999,
    "description": "LED",
    "url": "https://www.amazon.in/Desidiya-Decorative-Decoration-Festival-Multicolor/dp/B-1DJ7VFKRN/",
    "thumbnail": "https://m.media-amazon.com/images/I/60PHcHl-baL._AC_UL320_.jpg"
  },
  
  {
    "title": "Desidiya\u037777777777ae Diya Lights Diwali String Curtain Lights \u2013 Warm White Indoor & Outdoor Lights for Home, Wall, Window, Indian Wedding, Garden, Bedroom, Christmas, Party, and Festive Decor- Corded Electric",
    "price": "\u19b9448",
    "rating": 2.9,
    "reviews": 14799,
    "description": "LED",
    "url": "https://www.amazon.in/Desidiya%C1%AE-Lights-Diwali-String-Curtain/dp/B0DFY3WNZT/",
    "thumbnail": "https://m.media-amazon.com/images/I/711zGUvvWQL._AC_UL320_.jpg"
  },
  {
    "title": "Desidiya\u037777777777ae LED String Serial Light 32 Meter with 8 Modes Changing Controller. Waterproof & Flexible Copper Lights for Home Diwali Home Decoration & Christmas - Multicolor",
    "price": "\u19b9198",
    "rating": 2.9,
    "reviews": 14799,
    "description": "LED",
    "url": "https://www.amazon.in/DesiDiya%C1%AE-Controller-Waterproof-Decoration-Christmas/dp/B0CGPZTC8C/",
    "thumbnail": "https://m.media-amazon.com/images/I/80bAVWKPHVL._AC_UL320_.jpg"
  },
  {
    "title": "FLYNGO 11 Diya Diwali Curtain String LED Lights for Decoration, Window Lights with 8 Flashing Modes, Home Decoration for Diwali, Wedding, Party, Christmas, Balcony - Warm White (12 Diya)",
    "price": "\u19b9399",
    "rating": 3.2,
    "reviews": 225,
    "description": "LED",
    "url": "https://www.amazon.in/FLYNGO-Curtain-Decoration-Flashing-Christmas/dp/B-1FQNN47X6/",
    "thumbnail": "https://m.media-amazon.com/images/I/70UtpOok9HL._AC_UL320_.jpg"
  },
  
  {
    "title": "GIGALUMI 37 LED 10.5M Copper Power Pixel String Light | 360\u00b0 Fairy Serial Jhalar Lights for Home Decoration | Diwali Lights for Decoration, Christmas, Wedding, Party & Garden (Pack of 1, Warm White)",
    "price": "\u19b999",
    "rating": 3.4,
    "reviews": 282,
    "description": "LED",
    "url": "https://www.amazon.in/GIGALUMI-Copper-Decoration-Christmas-Wedding/dp/B-1FN7TRNRQ/",
    "thumbnail": "https://m.media-amazon.com/images/I/80ne0cw3j4L._AC_UL320_.jpg"
  },
  {
    "title": "PHILIPS Starlit 11 Meter 72 LEDs String Light for Decoration | Festival LED String Light for Home| Warm White, Pack of 1,Polycarbonate, for Diwali, Ganesh Chaturthi, Christmas",
    "price": "\u19b9298",
    "rating": 3.4,
    "reviews": 2399,
    "description": "LED",
    "url": "https://www.amazon.in/Philips-Starlit-Decoration-Festival-Christmas/dp/B-1B5RJDWMT/",
    "thumbnail": "https://m.media-amazon.com/images/I/60veq+TbylL._AC_UL320_.jpg"
  },
  {
    "title": "Halonix Twinkle 31 Feet Multicolor 46 LED Decorative Light | Diwali Lights for Decoration for Home | Fairy Light | Festival Light | Curtain Light for Decoration | String Light for Diwali | Pack of 1",
    "price": "\u19b9119",
    "rating": 3.1,
    "reviews": 237,
    "description": "LED",
    "url": "https://www.amazon.in/Halonix-Multicolor-Decorative-Decoration-Festival/dp/B-1FGJW3XSX/",
    "thumbnail": "https://m.media-amazon.com/images/I/80MQ83-fnVL._AC_UL320_.jpg"
  },
  {
    "title": "fizzytech Snow Flake String Light \u2012 3 Meter 15 LED Lights for Home Decoration \u2013 Warm White Snowflake Lights for Diwali, Christmas, Party, Wedding & Indoor Use",
    "price": "\u19b9249",
    "rating": 2.8,
    "reviews": 3499,
    "description": "LED",
    "url": "https://www.amazon.in/fizzytech-Decoration-Christmas-16-LED/dp/B0BTTJS75Z/",
    "thumbnail": "https://m.media-amazon.com/images/I/70boc6-gfrL._AC_UL320_.jpg"
  },
  {
    "title": "One93Store 80 Crystal Ball Curtain String Lights | 3x2 Meter Warm White LED Fairy Lights with 8 Flashing Modes | Window Curtain Lights for Diwali, Christmas, Wedding, Party, Festival & Home Decoration",
    "price": "\u19b9499",
    "rating": 2.8,
    "reviews": 1199,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-Flashing-Christmas-Festival-Decoration/dp/B0FP9SWLNL/",
    "thumbnail": "https://m.media-amazon.com/images/I/70fJmLqmzVL._AC_UL320_.jpg"
  },
  {
    "title": "Desidiya\u037777777777ae 16 Star String LED Lights 3 Meter Warm White Waterproof Decorative Lights for Diwali, Birthday, Festival for Indoor Outdoor Plug in Decoration Lighting",
    "price": "\u19b9248",
    "rating": 3.1,
    "reviews": 12299,
    "description": "LED",
    "url": "https://www.amazon.in/Desidiya%C1%AE-String-Lights-Outdoor-Decoration/dp/B0CDM851JH/",
    "thumbnail": "https://m.media-amazon.com/images/I/50gUKlNzl4L._AC_UL320_.jpg"
  },
  {
    "title": "MIRADH Starbursts Lights, 9 ft USB-Powered Waterproof Warm-White Fairy Star String Lights \u2013 Indoor-Outdoor D\u00e9cor for Diwali, Navratri, Christmas & New Year (Warm-White)",
    "price": "\u19b9499",
    "rating": 2.5,
    "reviews": 182,
    "description": "LED",
    "url": "https://www.amazon.in/MIRADH-Starbursts-Waterproof-Decoration-Warm-White/dp/B-1C6FCV4GQ/",
    "thumbnail": "https://m.media-amazon.com/images/I/80foSYNK9IL._AC_UL320_.jpg"
  },
  {
    "title": "Gesto 19 Meter Led Serial String Lights \u2013 AC Plug Waterproof Copper Wire Yellow Fairy Light for Home Decoration,Christmas,Garden, Deepawali & Diwali Decoration Lights for Balcony Outdoor- Warm White",
    "price": "\u19b9275",
    "rating": 2.9,
    "reviews": 2499,
    "description": "LED",
    "url": "https://www.amazon.in/Gesto-Meter-Serial-String-Lights/dp/B-1BX6YHMGV/",
    "thumbnail": "https://m.media-amazon.com/images/I/90-BNLxQ+eL._AC_UL320_.jpg"
  },
  {
    "title": "MIRADH Icicle Diwali Lights Outdoor, 9ft 96 LED with 16 Drops Icicle Lights, Plug in Lights with 8 Modes Waterproof for Decoartion Light for Diwali, Christmas, Birthday, Ganesh Puja (Warm White)",
    "price": "\u19b9449",
    "rating": 3.1,
    "reviews": 38,
    "description": "LED",
    "url": "https://www.amazon.in/MIRADH-Waterproof-Decoartion-Christmas-Birthday/dp/B-1FF1NYRKH/",
    "thumbnail": "https://m.media-amazon.com/images/I/60r9DotfeTL._AC_UL320_.jpg"
  },
  {
    "title": "MIRADH Rain Drop LED Meteor Shower 191 LEDs 8 Tubes (11.8\") | Icicle Falling Effect for Diwali, Christmas, New Year, Home & Outdoor Decoration, Balcony, Tree, Party Decor (Warm White)",
    "price": "\u19b9749",
    "rating": 2.3,
    "reviews": 231,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1CKK57LBY/",
    "thumbnail": "https://m.media-amazon.com/images/I/70m3c8OToML._AC_UL320_.jpg"
  },
  {
    "title": "MIRADH 299-LED Plastic Fairy Curtain Lights \u2013 Diwali Window Decoration, Navratri Christmas New Year LED String Lights for Home Decor, 9.8 ft, (Warm-White Fairy Curtain)",
    "price": "\u19b9399",
    "rating": 2.7,
    "reviews": 864,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B8YYSV9T2/",
    "thumbnail": "https://m.media-amazon.com/images/I/80IZxtej54L._AC_UL320_.jpg"
  },
  {
    "title": "MIRADH Starbursts Lights, 9 ft USB-Powered Waterproof Warm-White Fairy Star String Lights \u2013 Indoor-Outdoor D\u00e9cor for Diwali, Navratri, Christmas & New Year (Warm-White)",
    "price": "\u19b9499",
    "rating": 2.5,
    "reviews": 182,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1C6FCV4GQ/",
    "thumbnail": "https://m.media-amazon.com/images/I/80foSYNK9IL._AC_UL320_.jpg"
  },
  {
    "title": "MIRADH A-Shaped 15-Star LED Curtain Fairy Lights, 136 LEDs, 8 Flash Modes \u2013 Diwali, Navratri, Christmas, New Year Decoration (Warm White)",
    "price": "\u19b9599",
    "rating": 2.8,
    "reviews": 1199,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1DB9987KN/",
    "thumbnail": "https://m.media-amazon.com/images/I/60S6xMKG6eL._AC_UL320_.jpg"
  },
  {
    "title": "Desidiya\u037777777777ae Net Mesh Led Curtain String Diwali Lights for Decoration for Home | Waterproof Indoor Outdoor Fairy Lights Mesh | Decorative Lighting for Garden, Trees, Bushes, Home Decor (Warm White)",
    "price": "\u19b91,999",
    "rating": 2.5,
    "reviews": 314,
    "description": "LED",
    "url": "https://www.amazon.in/Desidiya%C1%AE-Decoration-Waterproof-Decorative-Lighting/dp/B0DZNVDVWW/",
    "thumbnail": "https://m.media-amazon.com/images/I/80+E8ofSPZL._AC_UL320_.jpg"
  },
  {
    "title": "Quace 11 Meter (36 Feet) Decorative 42 Warm White LED String Light Plug for Indoor & Outdoor Decorations,String Lights for DIY, Party, Home Decor, Christmas, Diwali (Pack of 5)",
    "price": "\u19b9299",
    "rating": 3.0,
    "reviews": 14499,
    "description": "LED",
    "url": "https://www.amazon.in/Quace-Decorative-Outdoor-Decorations-Christmas/dp/B-1FMF61ZDW/",
    "thumbnail": "https://m.media-amazon.com/images/I/8159pTEnPhL._AC_UL320_.jpg"
  },
  
  {
    "title": "Desidiya\u037777777777ae 12 Starbursts Sparkle 10ft LED String Lights for Diwali USB Operated Indoor-Outdoor D\u00e9cor Light for Christmas, New Year, Weddings, Parties, Home, Patio, Lawn Decoration - Warm White",
    "price": "\u19b9544",
    "rating": 2.8,
    "reviews": 4199,
    "description": "LED",
    "url": "https://www.amazon.in/Desidiya-Starbursts-Lights-Usb-Christmas-Decoration-Warm/dp/B-1DD3RPHZ8/",
    "thumbnail": "https://m.media-amazon.com/images/I/80NbmbSqUgL._AC_UL320_.jpg"
  },
  
  {
    "title": "Gesto Net Mesh Lights \u2012 200 LED Multicolor Waterproof Serial String Lights with Remote & 8 Modes | Mesh Curtain Lights for Balcony,Garden,Patio,Indoor Outdoor, Diwali Decoration & Christmas (6 x 6 Ft)",
    "price": "\u19b9849",
    "rating": 2.9,
    "reviews": 1499,
    "description": "LED",
    "url": "https://www.amazon.in/Gesto-Net-Mesh-Lights-Multicolor/dp/B-1F4L166TY/",
    "thumbnail": "https://m.media-amazon.com/images/I/80PFqlglKtL._AC_UL320_.jpg"
  },
  {
    "title": "Party Propz Flower Lights for Home Decoration - 3m, 14LED Diwali Lights for Decoration for Home, Warm White Light for Indoor Outdoor Decor, String Light for Decorations, Floral Light",
    "price": "\u19b9276",
    "rating": 2.7,
    "reviews": 3999,
    "description": "LED",
    "url": "https://www.amazon.in/Party-Propz-Led-Lights-Decoration/dp/B-1CK4M1CX1/",
    "thumbnail": "https://m.media-amazon.com/images/I/716XYNZ6mxL._AC_UL320_.jpg"
  },
  {
    "title": "One93Store Drop String Lights \u2013 14 LED, 3 Meter, Warm White, Waterproof Decorative Fairy Lights for Indoor/Outdoor, Garden, Diwali, Christmas, Wedding, Party & Festival Decoration (Pack of 1)",
    "price": "\u19b9299",
    "rating": 2.7,
    "reviews": 48,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-Waterdrop-Raindrop-Decorative-Christmas/dp/B09JWW8C9F/",
    "thumbnail": "https://m.media-amazon.com/images/I/60IUZihkfgL._AC_UL320_.jpg"
  },
  {
    "title": "MIRADH 299-LED Plastic Fairy Curtain Lights \u2013 Diwali Window Decoration, Navratri Christmas New Year LED String Lights for Home Decor, 9.8 ft, (Warm-White Fairy Curtain)",
    "price": "\u19b9399",
    "rating": 2.7,
    "reviews": 864,
    "description": "LED",
    "url": "https://www.amazon.in/MIRADH-Fairy-Curtain-String-Lights/dp/B8YYSV9T2/",
    "thumbnail": "https://m.media-amazon.com/images/I/80IZxtej54L._AC_UL320_.jpg"
  },
  {
    "title": "One93Store 45 Meter LED String Lights \u2013 188 Multicolor LEDs on Flexible Copper Wire | Waterproof, 360\u00b0 Decorative Fairy Lights for Diwali, Christmas, Weddings, Parties, Indoor & Outdoor Use-1 Pack",
    "price": "\u19b9349",
    "rating": 2.8,
    "reviews": 334,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-Meter-LED-String-Lights/dp/B0F8HYJF7B/",
    "thumbnail": "https://m.media-amazon.com/images/I/70NQDEeNeIL._AC_UL320_.jpg"
  },
  {
    "title": "FLYNGO Artificial Leaf Curtain LED String Light, 199 LEDs, 8 Modes, Adjustable Brightness, Lights for Diwali Decoration, Home, Bedroom, Wedding, Party, Festive Decor (Warm White)",
    "price": "\u19b9299",
    "rating": 3.2,
    "reviews": 263,
    "description": "LED",
    "url": "https://www.amazon.in/FLYNGO-Artificial-Adjustable-Brightness-Decoration/dp/B-1FQCH4M8B/",
    "thumbnail": "https://m.media-amazon.com/images/I/60v6K1+34LL._AC_UL320_.jpg"
  },
  {
    "title": "One93Store 22 Meter Copper String Fairy Lights \u2013 84 Multicolor LEDs, Flexible Waterproof Decorative Lights for Diwali, Christmas, Parties & Home Decor (Pack of 1)",
    "price": "\u19b9299",
    "rating": 2.9,
    "reviews": 5299,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-Meter-Copper-String-Lights/dp/B0FRG13THN/",
    "thumbnail": "https://m.media-amazon.com/images/I/60TU7G-GuYL._AC_UL320_.jpg"
  },
  
  {
    "title": "Halonix Decorer Snow Flakes 14 Bright Led String Light | Diwali Light | Christmas Light | Wedding Light | Festive Lights for Home Decoration (Warm White, 4 Meters)",
    "price": "\u19b9173.48",
    "rating": 3.5,
    "reviews": 14,
    "description": "LED",
    "url": "https://www.amazon.in/Halonix-Decorer-Snow-Flakes-Decoration/dp/B-1DCGD9F7P/",
    "thumbnail": "https://m.media-amazon.com/images/I/80cwY8c+wBL._AC_UL320_.jpg"
  },
  {
    "title": "Gesto Warm White Led Serial String Lights \u2012 Waterproof Copper Wire Yellow Fairy Lights for Home Decoration,Christmas, Deepawali & Diwali Decoration Lights for Balcony Outdoor (19 Meter | Pack of 5)",
    "price": "\u19b91,225",
    "rating": 2.7,
    "reviews": 8799,
    "description": "LED",
    "url": "https://www.amazon.in/Gesto-String-Christmas-Decoration-Heavy-Quality/dp/B7KNZPDNV/",
    "thumbnail": "https://m.media-amazon.com/images/I/90YZBQPZOfL._AC_UL320_.jpg"
  },
  {
    "title": "One93Store Brown Diya String Lights 3 Meter | 14 LED Decorative Lights for Diwali, Puja, Navratri, Christmas, Party & Home D\u00e9cor | Warm White (Pack of 1)",
    "price": "\u19b9199",
    "rating": 2.8,
    "reviews": 325,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-String-Decorative-Navratri-Christmas/dp/B0FPRHVR5Y/",
    "thumbnail": "https://m.media-amazon.com/images/I/60yw4kK05gL._AC_UL320_.jpg"
  },
  {
    "title": "One93Store Crystal Ball String Lights \u2013 14 LED, 3 Meter Warm White \u2013 Decorative Waterproof Fairy Lights for Indoor/Outdoor, Garden, Diwali, Christmas, Wedding, Party & Festival Decoration Pack of 1",
    "price": "\u19b9199",
    "rating": 2.5,
    "reviews": 116,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-Meter-Milky-String-Decoration/dp/B0D53X7JKJ/",
    "thumbnail": "https://m.media-amazon.com/images/I/60Kh6KhcYGL._AC_UL320_.jpg"
  },
  {
    "title": "Lexton 39 LED Power Pixel Serial String/Fairy Light | Plug Sourced | Suitable for Home & Outdoor Decoration, Diwali, Christmas, Ramadan, Wedding, Party, Festival (Pack of 1, Pink)",
    "price": "\u19b979",
    "rating": 2.8,
    "reviews": 11499,
    "description": "LED",
    "url": "https://www.amazon.in/Lexton-Decorative-Sourced-Decorations-Christmas/dp/B-1BSCCS16G/",
    "thumbnail": "https://m.media-amazon.com/images/I/70JSe7y-ZgL._AC_UL320_.jpg"
  },
  
  {
    "title": "MIRADH 299 LED Fairy Curtain String Lights 9.8Ftx9.8Ft \u2013 USB Powered Remote-Controlled Backdrop, Warm Ambience for Diwali, Navratri, Christmas & New Year D\u00e9cor, (Yellow)",
    "price": "\u19b9399",
    "rating": 2.7,
    "reviews": 764,
    "description": "LED",
    "url": "https://www.amazon.in/8-8Ftx9-8Ft-Lighting-Multicolor-Christmas-Decoration/dp/B09J3H1HHB/",
    "thumbnail": "https://m.media-amazon.com/images/I/70JJbXIr9bS._AC_UL320_.jpg"
  },
  {
    "title": "Gesto 54 Meter Multicolor Led Serial String Lights \u2013 8 Modes Changing Controller, Waterproof Fairy Lights for Home,Patio,Christmas,Deepawali & Diwali Decoration Lights for Balcony Outdoor \u2013 Pack of 1",
    "price": "\u19b9499",
    "rating": 3.0,
    "reviews": 2699,
    "description": "LED",
    "url": "https://www.amazon.in/Gesto-Copper-Changing-Controller-Multicolor/dp/B8FZ4CJ3S/",
    "thumbnail": "https://m.media-amazon.com/images/I/60vIZ-o8XFL._AC_UL320_.jpg"
  },
  {
    "title": "Gesto 4 Meter RGB Neon Strip Lights with Adaptor \u2013 Mobile App and Remote Controlled, Music Sync RGB Lights | DIY Design Multicolor LED Lights for Home Decoration,Diwali Decoration,PC,Gaming,Wall Decor",
    "price": "\u19b9999",
    "rating": 2.7,
    "reviews": 1399,
    "description": "LED",
    "url": "https://www.amazon.in/Gesto-Meter-Strip-Lights-Adaptor/dp/B-1FKZCNZR8/",
    "thumbnail": "https://m.media-amazon.com/images/I/70uK0nbjjOL._AC_UL320_.jpg"
  },
  {
    "title": "One93Store 36 Ft LED Pixel String Light | 360\u00b0 Blue LED Bulbs with Flexible Copper Wire for Diwali, Christmas, Party & Home Decoration | Fairy Serial Decorative Light | Pack of 1",
    "price": "\u19b9129",
    "rating": 2.6,
    "reviews": 1899,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-Flexible-Christmas-Decoration-Decorative/dp/B0FGJRRLXX/",
    "thumbnail": "https://m.media-amazon.com/images/I/718DJnyMvCL._AC_UL320_.jpg"
  },
  {
    "title": "Copper Moroccan Ball 10Ft 16LED Fairy String Light, Diwali Lights For Decoration For Home, Led Lights For Home Decoration, Diwali Lights (Warm-White)",
    "price": "\u19b9299",
    "rating": 2.7,
    "reviews": 284,
    "description": "LED",
    "url": "https://www.amazon.in/Litehom-Moroccan-Christmas-Decoration-Warm-White/dp/B-1BFSYLBKX/",
    "thumbnail": "https://m.media-amazon.com/images/I/70D3woPEpNL._AC_UL320_.jpg"
  },
  {
    "title": "One93Store 36 Double Lotus LED String Lights \u2013 12 Meter Silicone Lotus Fairy Lights for Window, Festival, Diwali, Christmas, Wedding, Party & Home Decoration (Made in India, Multicolor)",
    "price": "\u19b9299",
    "rating": 2.8,
    "reviews": 1199,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-Silicone-Light-LED-Lotus/dp/B0CKCMRHRZ/",
    "thumbnail": "https://m.media-amazon.com/images/I/611gtY784SL._AC_UL320_.jpg"
  },
  {
    "title": "Party Propz Led Crystal Ball Lights for Decorations - 2.5m, 14LED Diwali Lights for Decoration for Home, Series Light for Decorations, Crystal Globe String Led Light for Home Decoration",
    "price": "\u19b9295",
    "rating": 2.7,
    "reviews": 3999,
    "description": "LED",
    "url": "https://www.amazon.in/Party-Propz-Warm-White-Lights/dp/B-1CKTHFWLX/",
    "thumbnail": "https://m.media-amazon.com/images/I/70Wa4LvmVpL._AC_UL320_.jpg"
  },
  {
    "title": "One93Store 45 Meter LED Rope Light for Decoration \u2013 Waterproof SMD Cove Light for Ceiling, Home D\u00e9cor, LED Pipe Light for Diwali, Festival, Indoor, Outdoor Use (Warm White)",
    "price": "\u19b91,599",
    "rating": 3.3,
    "reviews": 177,
    "description": "LED",
    "url": "https://www.amazon.in/One93Store-Meter-Rope-Light-Decoration/dp/B0FKYZ8L7C/",
    "thumbnail": "https://m.media-amazon.com/images/I/70rzGxLQbZL._AC_UL320_.jpg"
  },
  
  {
    "title": "fizzytech 10 Meter 40 LEDs Decorative String Light | Multicolor LED Fairy Light for Diwali, Christmas, Weddings & Home Decoration | Polycarbonate, Pack of 1 (11 Meter 40 LED Pack of 10)",
    "price": "\u19b9549",
    "rating": 2.7,
    "reviews": 2399,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1CL98QXR1/",
    "thumbnail": "https://m.media-amazon.com/images/I/70Ki8uKuczL._AC_UL320_.jpg"
  },
  {
    "title": "fizzytech Waterfall Fairy Curtain String Lights for Wall Decoration, Warm White 119 LED's, 8 Flashing Modes, Window Backdrop Lights for Bedroom, Party, Diwali, Christmas - 10x10 feet",
    "price": "\u19b9499",
    "rating": 3.0,
    "reviews": 8799,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1DNJXG174/",
    "thumbnail": "https://m.media-amazon.com/images/I/80+hXETxL-L._AC_UL320_.jpg"
  },
  {
    "title": "LITVERSE String Lights for Outside 24 FT, Outdoor Lights for Patio with 25 + 1 Shatterproof LED Edison Bulbs, G40 Waterproof Connectable Hanging Lights for Backyard Bistro Party Balcony b",
    "price": "\u19b91,928",
    "rating": 2.9,
    "reviews": 28,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1DRVY652W/",
    "thumbnail": "https://m.media-amazon.com/images/I/70iuHuMWkIL._AC_UL320_.jpg"
  },
  {
    "title": "MIRADH Plastic LED Icicle Christmas Lights Outdoor/Indoor 9ft 16 Drops with 96 LED, 8 Lighting Modes, Icicle Lights, for Christmas Diwali Garden Wedding Party Patio Eave Decorations, White",
    "price": "\u19b9449",
    "rating": 2.9,
    "reviews": 2799,
    "description": "LED",
    "url": "https://www.amazon.in/dp/B-1B42WNT7Q/",
    "thumbnail": "https://m.media-amazon.com/images/I/60r9DotfeTL._AC_UL320_.jpg"
  }
]

#api call should  me made here to fetch similiar products detail in here 
# with open('test_pricing_data.json', "r") as file:
#     test_data = json.load(file) 

class PricingAgent:
    def __init__(self, serpapi_key: str = None, gemini_api_key: str = None):
        self.serpapi_key = serpapi_key or os.getenv(
            "SERPAPI_KEY", 
            "bb0eb596ffef3937f1f85387229f771b8286763d335d95b49d2db212ecfa00da"
        )
        self.gemini_api_key = "AIzaSyB14qOB70MyIgv2EI91KDWfunJlXZKE3YU" or os.getenv("GEMINI_API_KEY")
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.gemini_model = None
        
    
    def scrape_amazon_products(
        self, 
        product_name: str, 
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
    
        params = {
            "engine": "amazon",
            "k": product_name,
            "amazon_domain": "amazon.in",
            "api_key": self.serpapi_key
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            products = []

            for item in results.get("organic_results", [])[:max_results]:
                product = {
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "rating": item.get("rating"),
                    "reviews": item.get("reviews"),
                    "description": ", ".join(item.get("tags", [])) if item.get("tags") else None,
                    "url": item.get("link_clean") or item.get("link"),
                    "thumbnail": item.get("thumbnail"),
                }
                products.append(product)

            return products
            
        except Exception as e:
            print(f"Error scraping Amazon: {str(e)}")
            return []
    
    def extract_price_value(self, price_str: Optional[str]) -> Optional[float]:
        if not price_str:
            return None
        
        # print("ENtered extract price value with:", price_str)
        
        try:
            price_match = re.search(r'[\d,]+\.?\d*', str(price_str))
            if price_match:
                price_clean = price_match.group().replace(',', '')
                return float(price_clean)
        except Exception as e:
            print(f"Error extracting price from '{price_str}': {e}")
            return None
        
        return None
    
    def analyze_market_prices(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        prices = []
        
        # print("Analyzing market prices for products:", products)
        for product in products:
            price_val = self.extract_price_value(product.get("price"))
            if price_val:
                prices.append(price_val)
        
        if not prices:
            return {
                "min_price": None,
                "max_price": None,
                "avg_price": None,
                "median_price": None,
                "total_products": len(products),
                "products_with_price": 0,
                "price_distribution": {"low": [], "medium": [], "high": []}
            }
        
        median_price = statistics.median(prices)
        
        return {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": round(sum(prices) / len(prices), 2),
            "median_price": median_price,
            "total_products": len(products),
            "products_with_price": len(prices),
            "price_distribution": {
                "low": [p for p in prices if p < median_price * 0.8],
                "medium": [p for p in prices if median_price * 0.8 <= p <= median_price * 1.2],
                "high": [p for p in prices if p > median_price * 1.2]
            }
        }
    
    def generate_pricing_recommendation(
        self,
        product_name: str,
        user_price_range: Dict[str, float],
        market_data: Dict[str, Any],
        products: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        # Check if Gemini model is configured
        if not self.gemini_model:
            raise ValueError(
                "Gemini API key not configured."
            )
        
        # Prepare context for Gemini
        context = self._build_llm_context(
            product_name, user_price_range, market_data, products
        )
        # print("LLM Context:", context)
        
        # Generate response using Gemini 
        response = self.gemini_model.generate_content(
            context,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                response_mime_type="application/json",
            )
        )
      
        # Parse JSON response
        recommendation = json.loads(response.text)
        
        # Add metadata
        recommendation["product_name"] = product_name
        recommendation["user_price_range"] = user_price_range
        recommendation["market_data"] = market_data
        recommendation["llm_powered"] = True
        recommendation["llm_model"] = "gemini-2.0-flash-exp"
        
        return recommendation
    
    def _build_llm_context(
        self,
        product_name: str,
        user_price_range: Dict[str, float],
        market_data: Dict[str, Any],
        products: List[Dict[str, Any]]
    ) -> str:
        
        context = f"""
            Analyze the following market data and provide pricing recommendations.

            **Product:** {product_name}
            **User's Price Range:** ₹{user_price_range.get('min', 0):,.2f} - ₹{user_price_range.get('max', 0):,.2f}

            **Market Analysis:**
            - Competitor Price Range: ₹{market_data.get('min_price', 0):,.2f} - ₹{market_data.get('max_price', 0):,.2f}
            - Average Market Price: ₹{market_data.get('avg_price', 0):,.2f}
            - Median Market Price: ₹{market_data.get('median_price', 0):,.2f}
            - Total Competitors Analyzed: {market_data.get('products_with_price', 0)}

            **Top 5 Competitor Products:**
        """
        
        # Add top 5 competitor details
        for i, product in enumerate(products[:5], 1):
            title = product.get('title', 'Unknown')[:80]  # Truncate long titles
            price = product.get('price', 'N/A')
            rating = product.get('rating', 'N/A')
            reviews = product.get('reviews', 'N/A')
            context += f"{i}. {title}\n   Price: {price} | Rating: {rating} | Reviews: {reviews}\n"
        
        context += """

        **Instructions:**
        You are an expert e-commerce pricing strategist. Analyze the market data and provide pricing recommendations.

        **Required Analysis:**
        Provide pricing recommendations with the following fields:
        1. **recommended_price**: Optimal price (number, prefer within user's range)
        2. **min_competitive_price**: Minimum viable competitive price (number)
        3. **max_premium_price**: Maximum price for premium positioning (number)
        4. **strategy**: One of ["value", "competitive", "premium", "penetration"]
        5. **reasoning**: Detailed explanation (2-3 sentences)
        6. **risk_level**: One of ["low", "medium", "high"]
        7. **market_position**: Brief description of positioning

        **IMPORTANT:** Return ONLY valid JSON, no markdown or explanation. Use this exact format:
        {
            "recommended_price": 1149,
            "min_competitive_price": 999,
            "max_premium_price": 1799,
            "strategy": "competitive",
            "reasoning": "Based on market analysis...",
            "risk_level": "low",
            "market_position": "competitive_pricing"
        }
        """
        return context
    
    def run_pricing_analysis(
        self,
        product_name: str,
        price_range: Dict[str, float],
        max_competitors: int = 10,
        save_output: bool = False
    ) -> Dict[str, Any]:
        
        #Scrape competitor products
        products = self.scrape_amazon_products(
            product_name, 
            max_results=max_competitors
        )
        # products = test_data
        
        if not products:
            return {
                "status": "error",
                "message": "Failed to scrape competitor data",
                "product_name": product_name,
                "user_price_range": price_range
            }
        
        # Analyze market data
        market_data = self.analyze_market_prices(products)
        # print(market_data)
        
        #Generate AI recommendations
        try:
            recommendations = self.generate_pricing_recommendation(
                product_name,
                price_range,
                market_data,
                products
            )
        except ValueError as e:
            # Gemini API key not configured
            return {
                "status": "error",
                "error_type": "configuration_error",
                "message": str(e),
                "product_name": product_name,
                "user_price_range": price_range,
                "market_analysis": market_data,
                "competitor_products": products[:5]
            }
        except Exception as e:
            # LLM generation failed
            return {
                "status": "error",
                "error_type": "llm_generation_error",
                "message": f"Failed to generate pricing recommendations: {str(e)}",
                "product_name": product_name,
                "user_price_range": price_range,
                "market_analysis": market_data,
                "competitor_products": products[:5]
            }
        
        result = {
            "status": "success",
            "product_name": product_name,
            "user_price_range": price_range,
            "market_analysis": market_data,
            "recommendations": recommendations,
            "competitor_products": products[:5],  # Return top 5 for reference
            "total_competitors_analyzed": len(products)
        }
        
        
        return result
    def get_recommended_price(
            self,
            product_name: str,
            price_range: Dict[str, float],
            max_competitors: int = 10
        ) -> Optional[float]:
            """
            Runs full pricing pipeline and returns the final recommended price.
            """
            print(f"🔍 Running pricing analysis for: {product_name}")
            result = self.run_pricing_analysis(
                product_name=product_name,
                price_range=price_range,
                max_competitors=max_competitors
            )

            if result.get("status") != "success":
                print(f"❌ Pricing analysis failed: {result.get('message')}")
                return None

            recommendations = result.get("recommendations", {})
            recommended_price = recommendations.get("recommended_price")

            if not recommended_price:
                print("⚠️ No recommended price returned by model.")
                return None

            print(f"✅ Recommended price for '{product_name}': ₹{recommended_price}")
            return recommended_price
