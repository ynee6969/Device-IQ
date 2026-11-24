# Catalog source coverage

## Current public inventory

The website now uses the 24 November 2026 research snapshot through `scripts/build_public_catalog.py`. It publishes **28 source-linked models and 32 configurations**: 14 smartphones, 9 tablets, and 5 laptops. These are not an exhaustive Philippine market census. Eligibility uses official Philippine launch or availability evidence inside the website's 1 January 2021 to 24 November 2026 observed period. The three Galaxy S21 models are eligible under that window even though they are outside the research workbook's narrower rolling window.

The research database retains 396 pending model candidates, 29 otherwise source-linked models with unresolved local dates, seven explicit held-out cases, and three announced ProArt laptops with retail availability still unconfirmed by the cited source. They are not in public browse, filters, comparisons, or saved-item results. Missing prices and specifications remain unrecorded. Exact model-level sources, publication dates, configuration sources and observed PHP prices are preserved in the public snapshot and linked from the detail pages. The existing 30-record pilot described below is retained as research input and a regression fixture, not as the current public catalog.

## Prior pilot record

Checked 23 November 2026. The target is all qualifying models officially released or made available in the Philippines from 1 January 2021 through the planned 30 November 2026 cutoff. **Coverage is not complete.** The source pages below establish an official Philippine product page or store listing on the observation date. Except for the Samsung Galaxy Tab S10 FE, original local availability dates still need dated evidence. The model release dates and discontinued status also need review. Each page in the site links to its source.

| Category | Verified starter configurations | Coverage state |
| --- | ---: | --- |
| Smartphones | 10 | Exact configurations from official Philippine product pages; Philippine prices and original launch dates unavailable. Older illustrative seeds remain excluded. |
| Tablets | 10 | Exact listed configurations and selected specifications recorded; Philippine prices unavailable. |
| Laptops | 10 | Exact Acer SKUs and listed new prices recorded; launch dates and broader brand/type coverage pending. |

## Product images

All 30 pilot records have locally stored product images for the browse, saved, and detail pages. `lib/catalog/image-manifest.json` records the page and original asset URL for each image. Images establish appearance only; specifications, price, and Philippine availability remain grounded in the sources below. Two Acer images show the model family rather than the exact listed configuration: Aspire Lite AL15-33P and Swift Air 14 AI. The detail page labels those cases and links to the image source.

## Smartphone sources

The selected configurations appear on official Philippine manufacturer pages. These sources establish availability when observed, but the original local launch date, current Philippine price, and lifecycle status still need evidence.

| Model | Configuration | Primary source | Remaining gap |
| --- | --- | --- | --- |
| POCO F7 | 12/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/poco-f7/specs/) | Price, launch date, lifecycle |
| POCO F7 Pro | 12/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/poco-f7-pro/specs/) | Price, launch date, lifecycle |
| POCO F7 Ultra | 12/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/poco-f7-ultra/specs/) | Price, launch date, lifecycle |
| POCO X7 Pro | 8/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/poco-x7-pro/specs/) | Price, launch date, lifecycle |
| Xiaomi 15 | 12/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/xiaomi-15/specs/) | Price, launch date, lifecycle |
| Xiaomi 15 Ultra | 16/512 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/xiaomi-15-ultra/specs/) | Price, launch date, lifecycle |
| REDMI Note 14 | 6/128 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/redmi-note-14/specs/) | Price, launch date, lifecycle |
| REDMI Note 14 5G | 6/128 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/redmi-note-14-5g/specs/) | Price, launch date, lifecycle |
| REDMI Note 14 Pro 5G | 8/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/redmi-note-14-pro-5g/specs/) | Price, launch date, lifecycle |
| Galaxy A56 5G | 8/128 GB · SM-A566BZKSPHL | [Samsung Philippines](https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a56-5g-awesome-graphite-128gb-sm-a566bzksphl/) | Price, launch date, lifecycle |

## Tablet sources

All links are official Philippine manufacturer pages. A listed variant is not evidence that every variant shown on a global page is locally sold; only the chosen configuration from each Philippine page was recorded.

| Model | Configuration | Primary source | Remaining gap |
| --- | --- | --- | --- |
| Xiaomi Pad 7 | 8/128 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/xiaomi-pad-7/specs/) | Price, launch date, lifecycle |
| Xiaomi Pad 7 Pro | 8/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/xiaomi-pad-7-pro/specs/) | Price, launch date, lifecycle |
| Xiaomi Pad 8 | 8/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/xiaomi-pad-8/specs/) | Price, launch date, lifecycle |
| Xiaomi Pad 8 Pro | 8/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/xiaomi-pad-8-pro/specs/) | Price, launch date, lifecycle |
| Xiaomi Pad Mini | 8/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/xiaomi-pad-mini/specs/) | Price, launch date, lifecycle |
| POCO Pad M1 | 8/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/poco-pad-m1/specs/) | Price, launch date, lifecycle |
| POCO Pad X1 | 8/512 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/poco-pad-x1/specs/) | Price, launch date, lifecycle |
| REDMI Pad SE 8.7 4G | 4/64 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/redmi-pad-se-8-7-inch-4g/specs/) | Price, launch date, lifecycle |
| REDMI Pad 2 Pro | 8/256 GB | [Xiaomi Philippines](https://www.mi.com/ph/product/redmi-pad-2-pro/specs/) | Price, launch date, lifecycle |
| Galaxy Tab S10 FE | Wi-Fi 8/128 GB | [Samsung Newsroom Philippines](https://news.samsung.com/ph/galaxy-tab-s10-fe-series-brings-intelligent-experiences-to-the-forefront-with-premium-versatile-design) | Price, model release date, lifecycle; local availability announced for 15 May 2025 |

## Laptop sources

All links are exact-SKU pages on the Acer Philippines official store. Prices are observed PHP new-product listings, not permanent retail prices. Stock status can change. No item has been confirmed discontinued, so no used-price observation is asserted.

| Model/SKU | Primary source | Remaining gap |
| --- | --- | --- |
| Swift Go SFG14-75-55MB / NX.JNBSP.001 | [Acer PH](https://store.acer.com/en-ph/swift-go-sfg14-75-55mb-opi-steam-blue) | Exact CPU model, launch date, lifecycle |
| Swift Go SFG14-01-X2PX / NX.KYXSP.003 | [Acer PH](https://store.acer.com/en-ph/swift-go-sfg14-01-x2px-opi-steel-gray) | Launch date, lifecycle |
| Swift SF14-51-553D / NX.J2KSP.002 | [Acer PH](https://store.acer.com/en-ph/swift-sf14-51-553d-opi-frost-blue) | Launch date, lifecycle |
| Aspire Lite AL15-33P-332M / NX.DY0SP.001 | [Acer PH](https://store.acer.com/en-ph/aspire-lite-al15-33p-332m-natural-titanium) | Launch date, lifecycle |
| Aspire Go AG15-43P-R19X / NX.JPKSP.001 | [Acer PH](https://store.acer.com/en-ph/aspire-go-15-ai-ag15-43p-r19x-opi-pure-silver) | Launch date, lifecycle |
| Aspire Lite AL14-42P-R1LF / NX.DJ3SP.001 | [Acer PH](https://store.acer.com/en-ph/aspire-lite-al14-42p-r1lf-opi-light-silver) | Launch date, lifecycle |
| Predator Helios Neo 16 PHN16-73-93Y5 / NH.QX2SP.001 | [Acer PH](https://store.acer.com/en-ph/predator-helios-neo-16-phn16-73-93y5-opi-abyssal-black) | Launch date, lifecycle |
| Swift Air SFA14-I31-56FJ / NX.SHYSP.002 | [Acer PH](https://store.acer.com/en-ph/swift-air-14-ai-i-sfa14-i31-56fj-opi-sage-green) | Launch date, lifecycle |
| Predator Helios Neo Slim PHN16S-71-9269 / NH.QXASP.003 | [Acer PH](https://store.acer.com/en-ph/predator-helios-neo-slim-16-phn16s-71-9269-opi-abyssal-black) | Launch date, lifecycle |
| Predator Helios Neo 16 PHN16-72-99K9 / NH.QNNSP.003 | [Acer PH](https://store.acer.com/en-ph/intel-corei9-predator-helios-neo-16-phn16-72-99k9-opi-black) | Launch date, lifecycle; out of stock at page check |

## Next coverage work

Review other manufacturers, all laptop form factors, discontinued models, and every eligible year and price band. For discontinued models, manually verify a Philippine used listing or leave used price unavailable. Facebook Marketplace access and seller information are not part of this dataset. Do not infer a census total from the 30-record pilot.
