# DeviceIQ Specification Completeness Report

Generated: 2026-11-26T16:26:04+08:00

> Research status only. The workbook and catalog are provisional research inputs, not a complete or fully verified census of Philippine releases.

## Coverage summary

| Metric | Actual result |
| --- | ---: |
| Models | 456 |
| Configurations | 562 |
| Models with manually verified source fields | 301 |
| Configurations with manually verified source fields | 410 |
| Laptop models with official-source reviews | 18/18 |
| Laptop configurations with reviewed source fields | 22 |
| Models with all fields assessed | 2 |
| Specification-complete models | 0 |
| Complete with disclosed gaps | 2 |
| Incomplete models | 454 |
| Conflicting specification records | 40 |
| Assessed specification fields | 12435 |
| Verified specification fields | 11915 |
| Unavailable fields | 373 |
| Not applicable fields | 107 |
| Pending verification fields | 13808 |
| Manually reviewed price candidates | 32 |
| Assessment coverage | 47.38% |
| Verified coverage | 45.40% |
| Candidate field observations | 5883 |
| Candidate prices | 428 |
| Candidate source links | 203 |
| Image-matched models | 48 |
| Models with image unavailable | 408 |
| Excluded models | 3 |
| Held-out claims / records | 7 |

Assessment coverage = fields with a reviewed status / applicable field rows. Verified coverage = fields supported by reviewed source evidence / applicable field rows. A model remains incomplete while any applicable field is pending or conflicting.

## By category

| Category | Models | Configurations | Applicable field rows | Assessed | Verified | Pending | Assessment | Verified coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| smartphones | 288 | 373 | 17158 | 9749 | 9407 | 7409 | 56.82% | 54.83% |
| tablets | 150 | 167 | 8183 | 2273 | 2097 | 5910 | 27.78% | 25.63% |
| laptops | 18 | 22 | 902 | 413 | 411 | 489 | 45.79% | 45.57% |

## Collection snapshot (candidate evidence, not verified facts)

- Snapshot timestamp: `2026-11-26T12:43:51+08:00`.
- Fetch attempts: 265; successful page extractions: 223.
- Extracted pages by source type: `{'independent_ph_reference': 204, 'official': 19}`; extracted models by source type: `{'independent_ph_reference': 204, 'official': 19}`.
- Fetch attempts by category: `{'smartphones': 192, 'tablets': 55, 'laptops': 18}`; unsuccessful attempts by category: `{'smartphones': 15, 'tablets': 9, 'laptops': 18}`.
- Candidate field observations by source type: `{'independent_ph_reference': 6135, 'local_technology_publication': 6, 'official': 144}`.
- Candidate prices: 428; discovery links: 203.
- Source observations are promoted only when the fetched page passes an exact-model check and the field is safe to share across configurations. Unmatched, conflicting, variant-specific, price, and Philippine-availability claims remain candidates until reviewed.
- 13808 applicable fields remain pending because no sufficiently matched source was recorded, a source does not establish the exact variant/region, or the available result is still only a candidate. A blank is not treated as zero or as a negative specification.

## Field backlog

Every category template field is enumerated in `research/enrichment/specification-fields.json`. The full configuration-level evidence matrix is in `research/enrichment/specification-field-audit.json`; a review copy is appended to the supplied workbook when it is available.

| Group | Applicable rows | Assessed | Verified | Pending |
| --- | ---: | ---: | ---: | ---: |
| Accessories | 334 | 94 | 92 | 240 |
| Audio | 562 | 339 | 336 | 223 |
| Battery | 2226 | 1035 | 920 | 1191 |
| Build | 2226 | 1013 | 974 | 1213 |
| Camera | 3262 | 1671 | 1546 | 1591 |
| Connectivity | 4057 | 2173 | 2125 | 1884 |
| Display | 3394 | 1911 | 1890 | 1483 |
| Identity | 1124 | 473 | 437 | 651 |
| Input | 44 | 7 | 7 | 37 |
| Memory | 2832 | 1273 | 1241 | 1559 |
| Other | 562 | 315 | 309 | 247 |
| Philippine market | 1708 | 460 | 432 | 1248 |
| Platform | 3372 | 1661 | 1598 | 1711 |
| Release history | 540 | 10 | 8 | 530 |

## Priority list

454 model records remain `SPECIFICATION_INCOMPLETE`. The list below is ordered by pending fields and missing current values, with exact configuration IDs so work can be assigned without merging variants.

| Year (claimed) | Category | Brand | Model | Configuration | Record ID | Missing current values | Applicable fields | Status |
| --- | --- | --- | --- | --- | --- | ---: | ---: | --- |
| 2022 | tablets | Nokia | T10 | Configuration not recorded | `device_122fb62b2868fc-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Samsung | Galaxy Tab S8 | Configuration not recorded | `device_211eea228c21fc-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Samsung | S8 Ultra | Configuration not recorded | `device_b1f198b69a803a-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Samsung | S8+ | Configuration not recorded | `device_104702347ea1db-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | ABC TECH | X10 | Configuration not recorded | `device_2d3b3b3ff3d487-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | ABC TECH | X10+ | Configuration not recorded | `device_01ffae05ba688a-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | ABC TECH | X8 | Configuration not recorded | `device_87e79ad13fe93b-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | DOOGEE | T10 | Configuration not recorded | `device_6d0aa2c52b2ae3-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | DOOGEE | T20 Ultra | Configuration not recorded | `device_6e3c9bac9e1aee-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | DOOGEE | T20mini Pro | Configuration not recorded | `device_2789997925aa9f-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | DOOGEE | T30 Pro | Configuration not recorded | `device_d9ff705b937a45-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | DOOGEE | T30 Ultra | Configuration not recorded | `device_a29ccf8f940bd5-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Huawei | MatePad 11 (2023) | Configuration not recorded | `device_a7a945ae754e5c-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Huawei | MatePad Air PaperMatte Edition | Configuration not recorded | `device_4264ad7b1391c7-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Redmi | Pad SE | Configuration not recorded | `device_659d0e6fb64dfe-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | Galaxy Tab S9 | Configuration not recorded | `device_7867f6ebccc2fa-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | Galaxy Tab S9 Ultra | Configuration not recorded | `device_82e9616b879292-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | Galaxy Tab S9+ | Configuration not recorded | `device_3bdcbc7b1b3d1b-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | S9 FE | Configuration not recorded | `device_dfa2be77dc5b49-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | S9 FE+ | Configuration not recorded | `device_e39dec48267850-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | S9 Ultra | Configuration not recorded | `device_3311c3af053490-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | S9+ | Configuration not recorded | `device_e0d19db4c6a510-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | ALLDOCUBE | X Game Tablet | Configuration not recorded | `device_b105da4a1aa1d6-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | CHERRY | Omega Tab Pro | Configuration not recorded | `device_f7adfb1435ab69-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | CHUWI | Hi10 Max | Configuration not recorded | `device_5a5d644e80a0bc-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | DOOGEE | U10 Pro | Configuration not recorded | `device_9f3b9a33d1db71-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Huawei | MatePad 11.5 PaperMatte Edition | Configuration not recorded | `device_4a8fac1db9995f-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Huawei | MatePad 11.5S | Configuration not recorded | `device_e96773081205db-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Huawei | MatePad 12 X | Configuration not recorded | `device_4de0db79c591ed-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | OPPO | Pad Neo | Configuration not recorded | `device_2086ae7e14dc6d-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | POCO | Pad | Configuration not recorded | `device_cbe116bce09923-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Samsung | Galaxy Tab S10+ | Configuration not recorded | `device_5a4be926237b63-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | TECLAST | T60 Plus | Configuration not recorded | `device_0c57c113794938-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | TECNO | MEGAPAD 11 | Configuration not recorded | `device_e487afbd486554-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | TechLife | Pad Neo | Configuration not recorded | `device_aada61bbbb8d13-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Xiaomi | Pad 6S Pro | Configuration not recorded | `device_0a08afaa2bffa0-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | AXZY | Pad | Configuration not recorded | `device_f423be385de374-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | AXZY | Pad Pro | Configuration not recorded | `device_3ed6e2de3d6c2b-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | HONOR | MagicPad 3 | Configuration not recorded | `device_3e74d3a7b1be43-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Huawei | MatePad Pro 12.2 | Configuration not recorded | `device_f2b3f5dd7c2e57-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Huawei | MatePad Pro 13.2 | Configuration not recorded | `device_1244787433e698-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Infinix | XPAD GT | Configuration not recorded | `device_366121902935ff-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Lenovo | Idea Tab Pro | Configuration not recorded | `device_8b6a8c7e13cc65-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Lenovo | Legion Tab Gen 3 | Configuration not recorded | `device_386e49035676e1-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Lenovo | Tab | Configuration not recorded | `device_fe963d150c0c05-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | OPPO | Pad 3 Matte Display Edition | Configuration not recorded | `device_7222203012f965-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Redmi | Pad 2 | Configuration not recorded | `device_613aa6e8b4e9f6-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Redmi | Pad 2 4G | Configuration not recorded | `device_d002382dd14e32-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Samsung | S10 FE+ | Configuration not recorded | `device_55b2a42e335e05-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Samsung | S11 | Configuration not recorded | `device_0c0a1d1059579e-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Samsung | S11 Ultra | Configuration not recorded | `device_471ef377eb2f8b-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | TECNO | MEGAPAD 10 | Configuration not recorded | `device_8961747cd8e2cb-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | TechLife | Pad Plus 12" | Configuration not recorded | `device_a99b4deb3254b8-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | TechLife | Pad Pro 12" | Configuration not recorded | `device_f0ab11fc7f2291-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | itel | VistaTab 10 mini | Configuration not recorded | `device_ee44f544afd990-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | itel | VistaTab 30 Pro | Configuration not recorded | `device_0cb0809d8065c9-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | itel | VistaTab 30GT | Configuration not recorded | `device_ea9fcd62d9b50b-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | HONOR | Pad X7b | Configuration not recorded | `device_60e0fa4776a699-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Huawei | MatePad 11.5 (2026) | Configuration not recorded | `device_1014e3d6ae10d7-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Huawei | MatePad Air (2026) | Configuration not recorded | `device_2263c0821998e3-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Infinix | XPAD 30 | Configuration not recorded | `device_c5134accc7f9ed-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Infinix | XPAD 30E | Configuration not recorded | `device_66ea188d5e96f4-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Infinix | XPAD Edge | Configuration not recorded | `device_e0e53b6e2f02ac-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Lenovo | Tab Plus Gen 2 | Configuration not recorded | `device_4de5bc878d7e64-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | NEXAL | Pad | Configuration not recorded | `device_2e7d91e5c076d1-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | OPPO | Pad Air 6 | Configuration not recorded | `device_da89397e7bff35-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | OnePlus | Pad 4 | Configuration not recorded | `device_7fee65356eb6db-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | OnePlus | Pad Go 2 | Configuration not recorded | `device_f69cb8702e308c-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Redmi | Pad 2 9.7 | Configuration not recorded | `device_7f3df035e1e1e0-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Samsung | Galaxy Tab A11+ | Configuration not recorded | `device_c91013243e8782-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | TCL | Note A1 NXTPAPER | Configuration not recorded | `device_7efc476a86ac0c-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | TECNO | MEGAPAD 2 | Configuration not recorded | `device_5d6fb2994f5a30-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | TechLife | Pad Mini | Configuration not recorded | `device_f7cbc853c644dc-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | TechLife | Pad Neo SE | Configuration not recorded | `device_1535d8a05f2fa1-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | TechLife | Pad Plus 2 | Configuration not recorded | `device_9d4cf39af3e3ef-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | itel | VistaTab 12 | Configuration not recorded | `device_3a0c056003bdcb-unrecorded` | 48 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | Galaxy Tab S9 FE | Configuration not recorded | `device_33bf4ec88cc229-unrecorded` | 47 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Samsung | Galaxy Tab S9 FE+ | Configuration not recorded | `device_ca40d8c136e83b-unrecorded` | 47 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Samsung | Galaxy Tab S10 FE+ | Configuration not recorded | `device_8a813e7f0aaaae-unrecorded` | 47 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Samsung | Galaxy Tab S12 Ultra | Configuration not recorded | `device_3c3b3adfeb221f-unrecorded` | 47 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Samsung | Galaxy Tab S12+ | Configuration not recorded | `device_c1720f94c84582-unrecorded` | 47 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Samsung | Galaxy Tab S10 FE | Wi-Fi / 8 GB / 128 GB | `config_0879d9d92c6c34` | 34 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Redmi | 9T | Configuration not recorded | `device_b52492e270dd1f-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Redmi | Note 10 | Configuration not recorded | `device_91090601d354b8-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | TECNO | Camon 17P | Configuration not recorded | `device_097c07418374a0-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | TECNO | Spark 7 | Configuration not recorded | `device_cca2630fec4a42-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | vivo | V21 | Configuration not recorded | `device_09d07effbd7687-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Cherry Mobile | Aqua SV 5G | Configuration not recorded | `device_35bc65487e1514-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Nokia | X30 5G | Configuration not recorded | `device_71110a4a38ebff-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | OPPO | Reno8 | Configuration not recorded | `device_61b7b139393500-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | OnePlus | 10 Pro | Configuration not recorded | `device_63c58f9b94a470-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | POCO | F4 GT | Configuration not recorded | `device_fadbe684bc9a48-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | REDMAGIC | 7 | Configuration not recorded | `device_6908e733a06a0b-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | REDMAGIC | 7 Pro | Configuration not recorded | `device_5e189eced7d16d-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Samsung | Z Fold4 | Configuration not recorded | `device_63467ee4825c94-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | TCL | 20 R 5G | Configuration not recorded | `device_af0706eb4c718f-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | TCL | 20B | Configuration not recorded | `device_41c970f372aada-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | vivo | V23 | Configuration not recorded | `device_768d170ed1109b-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Coolpad | CP12 | Configuration not recorded | `device_5bc54f4d744bec-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Coolpad | Cool 20 Plus | Configuration not recorded | `device_14031d3cddb48d-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | DOOGEE | S mini | Configuration not recorded | `device_64797b9452613a-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Infinix | ZERO 30 | Configuration not recorded | `device_d14dd9dfdf860b-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Nokia | G42 5G | Configuration not recorded | `device_9ba373722ace11-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | OnePlus | Nord CE 3 Lite | Configuration not recorded | `device_2077faec2ddf17-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | REDMAGIC | 8 Pro | Configuration not recorded | `device_504422c5fc36f4-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | Z Flip5 | Configuration not recorded | `device_8d098d93ab5f47-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | Z Fold5 | Configuration not recorded | `device_8b71a65802ab50-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | ZTE | Blade V41 Vita 5G | Configuration not recorded | `device_bf5cf152c95ed1-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | ZTE | nubia Neo 5G | Configuration not recorded | `device_03f3856685042e-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | HMD | Barbie Phone | Configuration not recorded | `device_3c4d4f2e60c05a-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | HMD | Fusion | Configuration not recorded | `device_6c2ccca01e23d1-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | HMD | Pulse Pro | Configuration not recorded | `device_551e5a0e0e32cb-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | HMD | Skyline | Configuration not recorded | `device_14e0231a8d245e-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Huawei | nova Y72 | Configuration not recorded | `device_7e42ec1404e4a8-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Infinix | GT 20 Pro | Configuration not recorded | `device_8dc5ff47081aa0-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | OnePlus | Nord CE4 Lite | Configuration not recorded | `device_8a4529440550bd-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | S24 FE | Configuration not recorded | `device_f7fdf0130dfa08-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | Z Flip6 | Configuration not recorded | `device_f7b03019bb41af-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | Z Fold6 | Configuration not recorded | `device_8b17ead850bbec-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | TNT | Panalo Phone 5G | Configuration not recorded | `device_0083abb033ca34-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | ZTE | Blade A34 | Configuration not recorded | `device_20ae867db27440-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | ZTE | Blade A35 | Configuration not recorded | `device_ea48c6aea99c43-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | ZTE | Blade V50 Vita | Configuration not recorded | `device_3304af0b6511d1-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | itel | P55 4G | Configuration not recorded | `device_f145a46ebb0b9d-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | itel | P55+ | Configuration not recorded | `device_3a3e99a448f402-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | nubia | Music | Configuration not recorded | `device_c9a7424e0c8f5e-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | nubia | V60 Design | Configuration not recorded | `device_ac7a16d95c6b28-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | nubia | V70 Design | Configuration not recorded | `device_7d0fac170a9909-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | nubia | Z60 Ultra | Configuration not recorded | `device_4e6eda78a432ca-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | HMD | Crest | Configuration not recorded | `device_49c685883799a4-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Huawei | Mate XT | Configuration not recorded | `device_f0f00ed492e980-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Meizu | Note 21 | Configuration not recorded | `device_b7447bb03ebaa3-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Meizu | mblu 21 | Configuration not recorded | `device_dae69efa077092-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Nothing | Phone (3) | Configuration not recorded | `device_cb646c28f1c43b-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Nothing | Phone (3a) | Configuration not recorded | `device_d4cd36656dd62d-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OnePlus | Nord CE 5 | Configuration not recorded | `device_c2930a90e8912e-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | POCO | M7 Pro | Configuration not recorded | `device_29700631949a7d-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | REDMAGIC | 10 Pro | Configuration not recorded | `device_b170a1dc62d29f-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Samsung | S25 FE | Configuration not recorded | `device_1eaeaa69774a5f-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Samsung | Z Flip7 | Configuration not recorded | `device_d0485c1f1741bd-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Samsung | Z Fold7 | Configuration not recorded | `device_3e59218b898a0c-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | itel | A90 | Configuration not recorded | `device_cb987f3c8adfc3-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | nubia | Air | Configuration not recorded | `device_761fca96a9c988-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | nubia | V80 Design | Configuration not recorded | `device_55dfbac4d5c407-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Infinix | GT 50 Pro | Configuration not recorded | `device_a65111cbade52d-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Infinix | NOTE Edge | Configuration not recorded | `device_3525e4f5531676-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Nothing | Phone (4b) | Configuration not recorded | `device_d6cf74c181b450-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | OnePlus | 15R | Configuration not recorded | `device_63885f8e6d85c2-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | A08 | Configuration not recorded | `device_06a98f8968e4f1-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | A27 5G | Configuration not recorded | `device_51a0b1844a9713-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | S26 FE | Configuration not recorded | `device_2b358151a5e55f-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | TCL | NXTPAPER 60 Ultra | Configuration not recorded | `device_d4d915d251eb2c-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | nubia | Neo 5 | Configuration not recorded | `device_4dd1c6a4964b01-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | nubia | Neo 5 GT | Configuration not recorded | `device_0c3af34f502bf5-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | nubia | Neo 5 Max | Configuration not recorded | `device_a7e9bf31e81aa4-unrecorded` | 45 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Apple | iPad Pro M5 | Configuration not recorded | `device_639dbf609255e4-unrecorded` | 44 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Apple | iPad Pro M1 (2021) | Configuration not recorded | `device_e8026097f286fd-unrecorded` | 43 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Apple | iPad Pro M2 | Configuration not recorded | `device_9b65c21f337198-unrecorded` | 43 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Apple | iPad Air M3 | Configuration not recorded | `device_99d1f134735d0c-unrecorded` | 43 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Apple | iPad Air M4 | Configuration not recorded | `device_5327f2410c22e5-unrecorded` | 43 | 49 | SPECIFICATION_INCOMPLETE |
| Unassigned | tablets | Redmi | Pad SE 8.7 4G | 4 GB / 64 GB | `config_6721ffc171a8f2` | 30 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Apple | iPad 9th Gen | Configuration not recorded | `device_80a03073c65780-unrecorded` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Apple | iPad mini 6 | Configuration not recorded | `device_b3800bdea59d3d-unrecorded` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Apple | iPad 10th Gen | Configuration not recorded | `device_e4a50bfd310ec0-unrecorded` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Apple | iPad (A16/11th Gen) | Configuration not recorded | `device_73e4c3a19b8741-unrecorded` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Apple | iPad mini A20 Pro | 128GB Wi-Fi | `config_b3c69f6891ff28` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Apple | iPad mini A20 Pro | 256GB Wi-Fi | `config_1171e674caabc1` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Apple | iPad mini A20 Pro | 512GB Wi-Fi | `config_f7884a7190b8b4` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Apple | iPad mini A20 Pro | 128GB Wi-Fi + Cellular | `config_e74b8f67e15305` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Apple | iPad mini A20 Pro | 256GB Wi-Fi + Cellular | `config_0b2b6a049360ec` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Apple | iPad mini A20 Pro | 512GB Wi-Fi + Cellular | `config_dfd138a4b870e9` | 38 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Apple | iPad Air 5th Gen | Configuration not recorded | `device_a9930490a861ed-unrecorded` | 37 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Apple | iPhone SE (2022) | Configuration not recorded | `device_c1417eab404447-unrecorded` | 35 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Apple | 15 Plus | Configuration not recorded | `device_e737cf440a960c-unrecorded` | 35 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Apple | 16 Plus | Configuration not recorded | `device_4f49fc59fe2970-unrecorded` | 35 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Apple | 15 Pro | Configuration not recorded | `device_538f6645a137ee-unrecorded` | 34 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Apple | 15 Pro Max | Configuration not recorded | `device_331a91ecca31d0-unrecorded` | 34 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Apple | 16 Pro | Configuration not recorded | `device_a35cecf3e59fde-unrecorded` | 34 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Apple | 16 Pro Max | Configuration not recorded | `device_305c8f9c273ea1-unrecorded` | 34 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | ASUS | ROG Phone 5 | Configuration not recorded | `device_603fa1d223e7e0-unrecorded` | 32 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | ASUS | ROG Phone 6 Pro | 18 GB RAM / 512 GB storage · Storm White | `device_645b2e6accb6b4-18gb-512gb-ph` | 30 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Predator Helios Neo Slim 16 PHN16S-71-9269 | NH.QXASP.003 | `config_33fd77e02f526e` | 30 | 41 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Nokia | T20 | 4 GB RAM / 64 GB storage (global source configuration) | `device_1352c430fa0bb9-4-64-global` | 28 | 49 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Aspire Lite AL14-42P-R1LF | NX.DJ3SP.001 | `config_26dcd487702194` | 28 | 41 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Predator Helios Neo 16 PHN16-73-93Y5 | NH.QX2SP.001 | `config_3ee1892f38ed88` | 27 | 41 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Aspire Go 15 AI AG15-43P-R19X | NX.JPKSP.001 | `config_503035c068c969` | 27 | 41 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Aspire Lite AL15-33P-332M | NX.DY0SP.001 | `config_2d6dbc293f1116` | 27 | 41 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Swift Air 14 AI SFA14-I31-56FJ | NX.SHYSP.002 | `config_b35b4fb479b661` | 27 | 41 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | TCL | TAB 10S | Configuration not recorded | `device_59bc941c580cee-unrecorded` | 26 | 49 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Swift Go SFG14-75-55MB | NX.JNBSP.001 | `config_045742254d2835` | 26 | 41 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Xiaomi | Pad 5 | 6 GB RAM / 128 GB storage (global source configuration) | `device_eb3d0871ddd09e-6-128-global` | 25 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Xiaomi | Pad 5 | 6 GB RAM / 256 GB storage (global source configuration) | `device_eb3d0871ddd09e-6-256-global` | 25 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Redmi | Pad | Configuration not recorded | `device_f8c900df95cea4-unrecorded` | 25 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | realme | Pad Mini | Configuration not recorded | `device_1689321a84eec2-unrecorded` | 24 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Huawei | MatePad 11 | 6 GB RAM / 128 GB storage | `device_a12a6e701e607e-6-128-ph` | 25 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Huawei | MatePad 11 | 6 GB RAM / 256 GB storage | `device_a12a6e701e607e-6-256-ph` | 25 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | OPPO | Pad Air | 4 GB RAM / 64 GB storage | `device_169befc354ccf8-auto-4gb-64gb` | 25 | 49 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Swift SF14-51-553D | NX.J2KSP.002 | `config_c310afe3f6e51c` | 25 | 41 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | realme | Pad 2 | Configuration not recorded | `device_71d80065a119c2-unrecorded` | 23 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | TechLife | Pad | Configuration not recorded | `device_c8187c0bade95b-unrecorded` | 23 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook S16 (UM5606GA) | UM5606GA-SR368WSM | `config_166ca092fbd09a` | 21 | 41 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Lenovo | Tab M10 3rd Gen | Configuration not recorded | `device_534b809677bd0c-unrecorded` | 23 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | ProArt GoPro Edition (PX13) | HN7306EAC-LX075WSM | `device_ea2924f7ecf7ce-hn7306eac-lx075wsm` | 23 | 41 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | ProArt PX13 (HN7306) | HN7306EA-LX054WSM | `config_15a5da2d8b61bc` | 23 | 41 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | POCO | Pad C1 | Configuration not recorded | `device_7c8c3eaa1d8fa2-unrecorded` | 23 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | realme | Pad | Configuration not recorded | `device_23b53732758d44-unrecorded` | 23 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Samsung | A56 | 8 GB RAM / 128 GB storage | `device_183607a456844b-auto-8gb-128gb` | 23 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Samsung | A56 | 8 GB RAM / 256 GB storage | `device_183607a456844b-auto-8gb-256gb` | 23 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Huawei | MatePad 11.5 | Configuration not recorded | `device_ba6168d35e6a0f-unrecorded` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | OnePlus | Pad 3 | Configuration not recorded | `device_24d6c8bd87e1fa-unrecorded` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Swift Go SFG14-01-X2PX | NX.KYXSP.003 | `config_99091889235c83` | 22 | 41 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Infinix | XPAD | Configuration not recorded | `device_c031a0ffc97f29-unrecorded` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Samsung | Galaxy Tab S10 Ultra | Configuration not recorded | `device_c3193f69093d79-unrecorded` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | A35 | RAM not recorded / 128 GB storage · Globe Prepaid variant | `device_45c7e8bb258a1d-auto-ram-unrecorded-128gb` | 23 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Samsung | Galaxy Tab A7 Lite | LTE · 3 GB RAM / 32 GB storage · Gray | `device_2bbc3980a61c93-lte-gray-3-32` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Samsung | Galaxy Tab A7 Lite | LTE · 3 GB RAM / 32 GB storage · Silver | `device_2bbc3980a61c93-lte-silver-3-32` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Huawei | MatePad 10.4 (2022) | Wi-Fi only · 4 GB RAM / 64 GB storage | `device_dcf630692f9701-wifi-4-64` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Huawei | MatePad 10.4 (2022) | LTE · 4 GB RAM / 64 GB storage | `device_dcf630692f9701-lte-4-64` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Huawei | MatePad 10.4 (2022) | Wi-Fi only · 4 GB RAM / 128 GB storage | `device_dcf630692f9701-wifi-4-128` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Huawei | MatePad 10.4 (2022) | LTE · 4 GB RAM / 128 GB storage | `device_dcf630692f9701-lte-4-128` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | realme | Pad X | 6 GB RAM / 128 GB storage | `device_48ddda3db2685b-auto-6gb-128gb` | 22 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Lenovo | Tab P11 Plus | 4 GB RAM / 64 GB storage | `device_c581212ca1211c-auto-4gb-64gb` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Lenovo | Yoga Tab 11 | 4 GB RAM / 128 GB storage | `device_39c5786ef8c63f-auto-4gb-128gb` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Nokia | T21 | 4 GB RAM / 128 GB storage | `device_624b73097478bd-auto-4gb-128gb` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | MyPhone | MYT10 | 4 GB RAM / 64 GB storage | `device_7336303d0db747-auto-4gb-64gb` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook 14 (UX3480) | UX3480AA-U2489WSM | `config_2104cbd53025ef` | 21 | 41 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook 14 (UX3480) | UX3480AA-U2477WSM | `config_18ad6d3f8d0f8e` | 21 | 41 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook 14 (UX3480) | UX3480KA-U1137WSM | `config_f66f082a33d7c7` | 21 | 41 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook 14 (UX3480) | UX3480KA-U1135WSM | `config_4cc45014b7ad2d` | 21 | 41 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook 14 (UX3480) | UX3480QA-U1004WSM | `config_5104406ef8b646` | 21 | 41 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook DUO (UX8407) | UX8407AA-SN152WSM | `device_fc5e931cb8adc4-ux8407aa-sn152wsm` | 21 | 41 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Infinix | XPAD 20 | Configuration not recorded | `device_6b43251e18ef32-unrecorded` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Infinix | XPAD 20 Pro | Configuration not recorded | `device_278edd50241a63-unrecorded` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | A35 | 8 GB RAM / 256 GB storage | `device_45c7e8bb258a1d-auto-8gb-256gb` | 22 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26+ | 12 GB RAM / 256 GB storage | `device_f7d2b14d45c9bb-auto-12gb-256gb` | 22 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26+ | 12 GB RAM / 512 GB storage | `device_f7d2b14d45c9bb-auto-12gb-512gb` | 22 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Cherry Mobile | Aqua X | 3 GB RAM / 32 GB storage | `device_11aecb35329f4f-auto-3gb-32gb` | 21 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | HONOR | Pad 8 | 6 GB RAM / 128 GB storage | `device_1528d817e4015e-auto-6gb-128gb` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | HONOR | Pad X9 | 4 GB RAM / 128 GB storage | `device_9589e6ff44f20f-auto-4gb-128gb` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | HONOR | Pad X9a | 8 GB RAM / 128 GB storage | `device_31b9f8f3285827-auto-8gb-128gb` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | OPPO | Pad SE | 4 GB RAM / 128 GB storage | `device_03480f852fe594-auto-4gb-128gb` | 21 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | HONOR | 70 | 8 GB RAM / 256 GB storage | `device_5317d55fb742f4-8gb-256gb-ph` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Infinix | Note 12 | Configuration not recorded | `device_247e05ea3a4cdd-unrecorded` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | WIKO | 10 | Configuration not recorded | `device_b03d147075f61a-unrecorded` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Redmi | 12C | Configuration not recorded | `device_dd43c143572e76-unrecorded` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | DOOGEE | T10s | 6 GB RAM / 128 GB storage | `device_258deabd12180c-auto-6gb-128gb` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Redmi | Pad Pro | Configuration not recorded | `device_46fd114457fc6b-unrecorded` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook S14 (UX5406) | UX5406AA-SU165WSM | `device_686411caae8d78-ux5406aa-su165wsm` | 20 | 41 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Apple | iPhone Air | 256GB | `config_77be646abc47cc` | 21 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Apple | iPhone Air | 512GB | `config_caf187bebd3220` | 21 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Apple | iPhone Air | 1TB | `config_4c2f2f39ba2b5d` | 21 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Cherry Mobile | Aqua Infinity | 8 GB RAM / 128 GB storage | `device_5695810422dccc-auto-8gb-128gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Nokia | C1 Plus | 1 GB RAM / 16 GB storage | `device_805dbeb4c0bae8-auto-1gb-16gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Nokia | C20 | 2 GB RAM / 32 GB storage | `device_541056be6673d0-auto-2gb-32gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | TECNO | POVA 2 | 6 GB RAM / 128 GB storage | `device_151a397bc29d04-auto-6gb-128gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Lenovo | Tab P11 Pro | 128 GB RAM / 128 GB storage | `device_c7c06dd1d17701-auto-128gb-128gb` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | tablets | Xiaomi | Pad 6 | 8 GB RAM / 256 GB storage | `device_14877e82e6027a-auto-8gb-256gb` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | A55 | 8 GB RAM / 128 GB storage · operator variant | `device_8a8a8e9ba58d74-auto-8gb-128gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | HONOR | Pad X8a | 4 GB RAM / 128 GB storage | `device_241647cca09f91-auto-4gb-128gb` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Huawei | MatePad 11.5 (2025) | 8 GB RAM / 256 GB storage | `device_3e441cd553c8c1-auto-8gb-256gb` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | HONOR | Pad X8b | 4 GB RAM / 128 GB storage | `device_30a7d574ecef20-auto-4gb-128gb` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Infinix | Hot 11S | Configuration not recorded | `device_a1f48f0c79b49a-unrecorded` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | realme | C35 | Configuration not recorded | `device_ccc5b6f7e52ddb-unrecorded` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Redmi | 13C | Configuration not recorded | `device_e0475d3fdc975c-unrecorded` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | itel | S23 Plus | 8 GB RAM / 256 GB storage | `device_a8c831d7277179-s23-plus-8gb-256gb-ph` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | tablets | Lenovo | Tab M11 | 8 GB RAM / 128 GB storage | `device_9011ccfd930d9d-auto-8gb-128gb` | 19 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | TechLife | Pad Lite 8" | 4 GB RAM / 64 GB storage | `device_4c55a02cdd003d-auto-4gb-64gb` | 19 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Samsung | A36 | 8 GB RAM / 128 GB storage | `device_6649cf0c87cf5f-auto-8gb-128gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Samsung | A36 | 8 GB RAM / 256 GB storage | `device_6649cf0c87cf5f-auto-8gb-256gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Apple | iPhone 17e | 512GB | `config_6b2f688927f361` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Infinix | Note 10 | 6 GB RAM / 128 GB storage | `device_52041f12a45248-auto-6gb-128gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Nokia | C10 | 2 GB RAM / 16 GB storage | `device_f98c34eaca7076-auto-2gb-16gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Huawei | MatePad Pro 12.6 | 8 GB RAM / 256 GB storage | `device_3a670bbfcef402-8-256-ph` | 19 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | HONOR | X6 | 4 GB RAM / 64 GB storage | `device_b63dd5835e8cd8-auto-4gb-64gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Nokia | C2 2nd Edition | 2 GB RAM / 32 GB storage | `device_97dbe17ac8a890-auto-2gb-32gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Nokia | C12 | 3 GB RAM / 64 GB storage | `device_bbb78b8fe1364a-auto-3gb-64gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | A55 | 8 GB RAM / 256 GB storage | `device_8a8a8e9ba58d74-auto-8gb-256gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | HONOR | Pad 10 | 8 GB RAM / 256 GB storage | `device_bd4d2a440f137c-auto-8gb-256gb` | 19 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | HONOR | Play 10 | 3 GB RAM / 64 GB storage | `device_06de8fda08e269-auto-3gb-64gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | HONOR | Pad X9b Max | 6 GB RAM / 128 GB storage | `device_eab85ba6ec455b-auto-6gb-128gb` | 19 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | POCO | F3 | Configuration not recorded | `device_1d5e7c90315b84-unrecorded` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | POCO | M3 Pro 5G | Configuration not recorded | `device_490fb1ca65c6ae-unrecorded` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | POCO | X3 Pro | Configuration not recorded | `device_ee3bda03baa9d0-unrecorded` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Huawei | P50 Pocket | Configuration not recorded | `device_5cb25865e2fde7-unrecorded` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | Galaxy S23+ | 8 GB RAM / 256 GB storage | `device_9b51cd23075357-auto-8gb-256gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | Galaxy S23+ | 8 GB RAM / 512 GB storage | `device_9b51cd23075357-auto-8gb-512gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Apple | iPhone 16 | Configuration not recorded | `device_474454700e62e5-unrecorded` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | Galaxy S24+ | 12 GB RAM / 256 GB storage | `device_af72f6e6d0b475-auto-12gb-256gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | Galaxy S24+ | 12 GB RAM / 512 GB storage | `device_af72f6e6d0b475-auto-12gb-512gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Infinix | XPAD 30 Pro | 6 GB RAM / 128 GB storage | `device_e2c2dc7df3be86-auto-6gb-128gb` | 18 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | OPPO | Pad 5 Matte Display Edition | 8 GB RAM / 256 GB storage | `device_5692cd69038766-auto-8gb-256gb` | 18 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | A54 | 8 GB RAM / 128 GB storage | `device_de761fe6bf288e-auto-8gb-128gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | A54 | 8 GB RAM / 256 GB storage | `device_de761fe6bf288e-auto-8gb-256gb` | 20 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Apple | iPhone 16 | 128GB | `config_090985e9899f2d` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Apple | iPhone 17 | 512GB | `config_4de2116e55aafa` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Apple | iPhone 17e | 256GB | `config_0b03e89a32a315` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Cherry Mobile | Aqua S10 Pro | 6 GB RAM / 128 GB storage | `device_f94d1b9dfd4d9b-auto-6gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Lenovo | K12 Pro | 4 GB RAM / 128 GB storage | `device_0f47e06408a58e-auto-4gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Nokia | G10 | 4 GB RAM / 64 GB storage | `device_9cc70ec57738cf-auto-4gb-64gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | OPPO | A95 | 8 GB RAM / 128 GB storage | `device_9165cc4fcf2166-auto-8gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | realme | C25 | 4 GB RAM / 64 GB storage | `device_21393609ebfd19-auto-4gb-64gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | vivo | Y31 | 8 GB RAM / 128 GB storage | `device_a489c6c49c7f69-auto-8gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Cherry Mobile | Aqua S10 Pro 5G | 4 GB RAM / 128 GB storage | `device_a0dfb566ac341b-auto-4gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | TECNO | POVA 5G | 8 GB RAM / 128 GB storage | `device_24509b9edc7b24-auto-8gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | WIKO | T10 | 2 GB RAM / 64 GB storage | `device_1e2b30a9072d78-auto-2gb-64gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | WIKO | T10 | 4 GB RAM / 128 GB storage | `device_1e2b30a9072d78-auto-4gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | WIKO | T50 | 6 GB RAM / 128 GB storage | `device_808c2644b3d887-auto-6gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Nokia | C32 | 4 GB RAM / 128 GB storage | `device_e9be4016956527-auto-4gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | itel | A60s | 4 GB RAM / 128 GB storage | `device_f2f9c00c607e1a-auto-4gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | itel | P65 | 4 GB RAM / 128 GB storage | `device_d83a5f22e7e2ad-auto-4gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Apple | iPhone 16e | Configuration not recorded | `device_fe5c3b9c543e0f-unrecorded` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | itel | A200 | 3 GB RAM / 128 GB storage | `device_79dfbc51fea9ef-auto-3gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | POCO | F4 | Configuration not recorded | `device_4caf9ccacef3eb-unrecorded` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | A34 | 8 GB RAM / 128 GB storage | `device_b1444d256c2933-auto-8gb-128gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | A34 | 8 GB RAM / 256 GB storage | `device_b1444d256c2933-auto-8gb-256gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Apple | iPhone 17 | 256GB | `config_7cd9ec48d797fa` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Huawei | nova 8i | 8 GB RAM / 128 GB storage | `device_166dd84278e563-auto-8gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Motorola | Moto E40 | 4 GB RAM / 64 GB storage | `device_cdfd272b688da3-auto-4gb-64gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | TCL | 10 5G | 6 GB RAM / 128 GB storage | `device_5f1edc054cbdf8-auto-6gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | TCL | 20 SE | 4 GB RAM / 64 GB storage | `device_f0904d2ba34d51-auto-4gb-64gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | realme | 8 | 8 GB RAM / 128 GB storage | `device_043e146b87712e-auto-8gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Samsung | Galaxy Tab S7 FE | 6 GB RAM / 128 GB storage, LTE | `device_a1f3d16dd15fe1-samsung-lte-6gb-128gb` | 17 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Nokia | G21 | 6 GB RAM / 128 GB storage | `device_1ab818fc45adac-auto-6gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | TECNO | POVA 4 | 8 GB RAM / 128 GB storage | `device_afae56a06194c8-auto-8gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | realme | 9i | 6 GB RAM / 128 GB storage | `device_405dab530fa8bf-auto-6gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | HONOR | X6a | 4 GB RAM / 128 GB storage | `device_817ebdb2e912d8-auto-4gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Infinix | HOT 20 Play | 4 GB RAM / 128 GB storage | `device_8440a68663f2a0-auto-4gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | itel | P55 5G | 6 GB RAM / 128 GB storage | `device_d9d15762aebfca-auto-6gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | CHERRY | Aqua S11 Pro | 8 GB RAM / 256 GB storage | `device_87d23641a5c416-auto-8gb-256gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Huawei | nova 12i | 8 GB RAM / 256 GB storage | `device_2aad742ff083cd-auto-8gb-256gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | itel | S24 | 8 GB RAM / 256 GB storage | `device_7f63b0c0e24b70-auto-8gb-256gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Infinix | SMART 10 Plus | 4 GB RAM / 128 GB storage | `device_91332f13540838-auto-4gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | nubia | V70 Max | 6 GB RAM / 128 GB storage | `device_64ecb2c748158c-auto-6gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | HONOR | X5c Plus | 4 GB RAM / 128 GB storage | `device_563dcebaff857f-auto-4gb-128gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Huawei | Mate X7 | 16 GB RAM / 512 GB storage | `device_7af7c3bbb8daed-auto-16gb-512gb` | 17 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Lenovo | Legion Phone Duel 2 | Configuration not recorded | `device_0aa6c34889b55c-unrecorded` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | realme | GT Master Edition | Configuration not recorded | `device_f865ad8302ccf2-unrecorded` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Nothing | Phone (1) | Configuration not recorded | `device_78795cead1e4cf-unrecorded` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | POCO | X4 Pro 5G | Configuration not recorded | `device_69c90b908413ed-unrecorded` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | Galaxy S23 | Configuration not recorded | `device_043c45f5f5aaea-unrecorded` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | Galaxy S23 Ultra | Configuration not recorded | `device_2fdccd7c04cdf9-unrecorded` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Samsung | A13 | 4 GB RAM / 128 GB storage | `device_ea7538b5f9c456-samsung-4gb-128gb` | 19 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Huawei | MatePad 10.4 (2021) | 4 GB RAM / 128 GB storage | `device_e82e93c423ed2a-kirin820-4gb-128gb` | 18 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Samsung | A13 | 6 GB RAM / 128 GB storage | `device_ea7538b5f9c456-samsung-6gb-128gb` | 18 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Huawei | nova 8 | 8 GB RAM / 128 GB storage | `device_bf7b4c859d650f-auto-8gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Huawei | nova 9 | 8 GB RAM / 256 GB storage | `device_ebec3be5bc183d-auto-8gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Infinix | ZERO X | 8 GB RAM / 128 GB storage | `device_cb3407a3cd88f4-auto-8gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | OnePlus | 9 | 12 GB RAM / 256 GB storage | `device_d73622136db863-auto-12gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | OnePlus | Nord N10 5G | 6 GB RAM / 128 GB storage | `device_e32584e4c2c966-auto-6gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Xiaomi | Mi 11 | 8 GB RAM / 256 GB storage | `device_f028ce40054ac5-auto-8gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | vivo | X60 | 12 GB RAM / 256 GB storage | `device_2adfa323eaf7c3-auto-12gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | vivo | X70 | 12 GB RAM / 256 GB storage | `device_b329974b67de8a-auto-12gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Huawei | P50 Pro | 8 GB RAM / 256 GB storage | `device_19d17b7352b92b-auto-8gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Motorola | Moto G31 | 4 GB RAM / 128 GB storage | `device_45bf8d657b5cb0-auto-4gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Motorola | Moto G51 5G | 4 GB RAM / 128 GB storage | `device_c4d84bf4eac670-auto-4gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | OnePlus | 10T | 8 GB RAM / 128 GB storage | `device_55cd9c564ff45c-auto-8gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Apple | iPhone 15 | Configuration not recorded | `device_d35f986ae89db2-unrecorded` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | HONOR | X7a | 6 GB RAM / 128 GB storage | `device_b895f62b149c40-auto-6gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Huawei | Mate X3 | 12 GB RAM / 512 GB storage | `device_19e802eacb942b-auto-12gb-512gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | CHERRY | Aqua GR | 8 GB RAM / 256 GB storage | `device_0f5b5c515bfea4-auto-8gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Huawei | nova 12 SE | 8 GB RAM / 256 GB storage | `device_7e7a5726c99b5b-auto-8gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | itel | RS4 | 8 GB RAM / 128 GB storage | `device_1ac2da32137ff2-auto-8gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | itel | RS4 | 12 GB RAM / 256 GB storage | `device_1ac2da32137ff2-auto-12gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | HONOR | Magic V5 | 16 GB RAM / 512 GB storage | `device_2ea87ff8e9a1bf-auto-16gb-512gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | HONOR | X5b | 4 GB RAM / 64 GB storage | `device_e3ae704e116829-auto-4gb-64gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OPPO | A6 Pro | 8 GB RAM / 256 GB storage | `device_b29408857dadb7-auto-8gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Redmi | A3x | 3 GB RAM / 64 GB storage | `device_2cb105eb8b9081-auto-3gb-64gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | nubia | Neo 3 | 8 GB RAM / 128 GB storage | `device_41f7ce0f9a5e75-auto-8gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Huawei | Mate 80 Pro | 16 GB RAM / 512 GB storage | `device_60c2fce774423f-auto-16gb-512gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Infinix | HOT 70 | 4 GB RAM / 128 GB storage | `device_d5a711fa586d17-auto-4gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Infinix | HOT 70 | 4 GB RAM / 256 GB storage | `device_d5a711fa586d17-auto-4gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Infinix | HOT 70 | 6 GB RAM / 128 GB storage | `device_d5a711fa586d17-auto-6gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Infinix | HOT 70 | 6 GB RAM / 256 GB storage | `device_d5a711fa586d17-auto-6gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | OPPO | A7 Pro 5G | 6 GB RAM / 256 GB storage | `device_f3b7d074083170-auto-6gb-256gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | TECNO | Spark Go 3 | 4 GB RAM / 64 GB storage | `device_0a6709312abef7-auto-4gb-64gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | TECNO | Spark Go 3 | 4 GB RAM / 128 GB storage | `device_0a6709312abef7-auto-4gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | nubia | V80 Max | 8 GB RAM / 128 GB storage | `device_ccaeeb90588d4f-auto-8gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Nothing | Phone (2) | Configuration not recorded | `device_bdec9cf376402d-unrecorded` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Samsung | Galaxy S23 FE | Configuration not recorded | `device_df7fc1f337d112-unrecorded` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Infinix | ZERO 5G | 8 GB RAM / 128 GB storage | `device_e8a5c1ec8bfd41-auto-8gb-128gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | realme | GT 2 Pro | 12 GB RAM / 256 GB storage | `device_48951d316c74ab-auto-12gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | realme | GT Neo 3 | 8 GB RAM / 256 GB storage | `device_32f97d66a7332b-auto-8gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | vivo | X80 | 12 GB RAM / 256 GB storage | `device_c24cb88bbab74c-auto-12gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | realme | C53 | 6 GB RAM / 128 GB storage | `device_558f40aef6c88e-auto-6gb-128gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | realme | C53 | 8 GB RAM / 256 GB storage | `device_558f40aef6c88e-auto-8gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | vivo | Y27 | 6 GB RAM / 128 GB storage | `device_6f256573a0fb54-auto-6gb-128gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | vivo | Y36 | 8 GB RAM / 256 GB storage | `device_d2f928e59b41f6-auto-8gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | HONOR | X8b | 8 GB RAM / 512 GB storage | `device_7d4200667d6578-auto-8gb-512gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | realme | Note 50 | 4 GB RAM / 64 GB storage | `device_e50fa244828c14-auto-4gb-64gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | vivo | Y27s | 8 GB RAM / 256 GB storage | `device_423537c0dfcff7-auto-8gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | HONOR | Magic7 Pro | 12 GB RAM / 512 GB storage | `device_7b761653f996f8-auto-12gb-512gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Huawei | Mate X6 | 12 GB RAM / 512 GB storage | `device_345b9ae6196e43-auto-12gb-512gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | TECNO | SPARK Slim | 8 GB RAM / 256 GB storage | `device_0d1b682662c173-auto-8gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | vivo | X200 FE | 12 GB RAM / 512 GB storage | `device_56f7b1663af010-auto-12gb-512gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | HONOR | X8d | 8 GB RAM / 256 GB storage | `device_fb0127404d4a05-auto-8gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Infinix | NOTE 60 Ultra | 12 GB RAM / 512 GB storage | `device_8e5704a6d2a18f-auto-12gb-512gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | TCL | NXTPAPER 70 Pro | 8 GB RAM / 256 GB storage | `device_c61a590d1264be-auto-8gb-256gb` | 15 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | HONOR | 90 | 12 GB RAM / 512 GB storage | `device_1298822c3211ec-12gb-512gb-ph` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | tablets | Huawei | MatePad 10.4 (2021) | 4 GB RAM / 64 GB storage / LTE | `device_e82e93c423ed2a-kirin820-4gb-64gb-lte` | 16 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Samsung | A23 | 6 GB RAM / 128 GB storage | `device_61c7ea30c4c22b-samsung-6gb-128gb` | 16 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | POCO | M5 | 4 GB RAM / 64 GB storage | `device_5e715b3d9e49b9-auto-4gb-64gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | POCO | M5 | 6 GB RAM / 128 GB storage | `device_5e715b3d9e49b9-auto-6gb-128gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | OPPO | Find N2 Flip | 8 GB RAM / 256 GB storage | `device_83e936d401c190-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | OPPO | Reno8 T | 8 GB RAM / 256 GB storage | `device_c809f816ac8afe-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | realme | C55 | 6 GB RAM / 128 GB storage | `device_3b6b36276e33de-auto-6gb-128gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | realme | C55 | 8 GB RAM / 256 GB storage | `device_3b6b36276e33de-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | CMF | Phone 1 | 8 GB RAM / 128 GB storage | `device_f2c44f4fcced4e-auto-8gb-128gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | CMF | Phone 1 | 8 GB RAM / 256 GB storage | `device_f2c44f4fcced4e-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | HONOR | Magic6 Pro | 12 GB RAM / 512 GB storage | `device_fafaabfbc99686-auto-12gb-512gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Nothing | Phone (2a) Plus | 12 GB RAM / 256 GB storage | `device_97fad2be2c9fe2-auto-12gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | POCO | M6 | 6 GB RAM / 128 GB storage | `device_55867d7699ae56-auto-6gb-128gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | POCO | M6 | 8 GB RAM / 256 GB storage | `device_55867d7699ae56-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | vivo | Y18 | 6 GB RAM / 128 GB storage | `device_91c53f265e9c3c-auto-6gb-128gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | vivo | Y18 | 8 GB RAM / 256 GB storage | `device_91c53f265e9c3c-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | HONOR | X7d | 8 GB RAM / 256 GB storage | `device_d888d354971d56-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | HONOR | X7d | 8 GB RAM / 512 GB storage | `device_d888d354971d56-auto-8gb-512gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OPPO | A5 Pro | 8 GB RAM / 128 GB storage | `device_9eb1785b48b4be-auto-8gb-128gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OPPO | A5 Pro | 8 GB RAM / 256 GB storage | `device_9eb1785b48b4be-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OPPO | Find X9 | 16 GB RAM / 512 GB storage | `device_47d6b992fed55a-auto-16gb-512gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Redmi | Pad 2 Pro 5G | 8 GB RAM / 256 GB storage | `device_c40842fa2183ab-redmi-pad-2-pro-5g-8-256` | 14 | 49 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | TECNO | CAMON Slim 5G | 8 GB RAM / 128 GB storage | `device_1ac008d82e15cc-auto-8gb-128gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | TECNO | CAMON Slim 5G | 8 GB RAM / 256 GB storage | `device_1ac008d82e15cc-auto-8gb-256gb` | 14 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Huawei | P60 Pro | 12 GB RAM / 512 GB storage | `device_a41c76670e8533-auto-12gb-512gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | POCO | C65 | 6 GB RAM / 128 GB storage | `device_8d417b7be5469c-auto-6gb-128gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | POCO | C65 | 8 GB RAM / 256 GB storage | `device_8d417b7be5469c-auto-8gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | OPPO | A60 | 8 GB RAM / 128 GB storage | `device_05c37682b4f4ff-auto-8gb-128gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | OPPO | A60 | 8 GB RAM / 256 GB storage | `device_05c37682b4f4ff-auto-8gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | OPPO | Find X8 | 12 GB RAM / 256 GB storage | `device_dc29499d7bd766-auto-12gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | OnePlus | 12 | 12 GB RAM / 256 GB storage (global source configuration) | `device_a8aa4ea8df33a0-12-256-global` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | OnePlus | 12 | 16 GB RAM / 512 GB storage (global source configuration) | `device_a8aa4ea8df33a0-16-512-global` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | OnePlus | 12R | 16 GB RAM / 256 GB storage | `device_987a2678ee5fbd-auto-16gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | realme | C67 | 8 GB RAM / 128 GB storage | `device_3c3e9ccda860c9-auto-8gb-128gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | realme | C67 | 8 GB RAM / 256 GB storage | `device_3c3e9ccda860c9-auto-8gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | ASUS | ROG Phone 9 Pro | 16 GB RAM / 512 GB storage · Phantom Black | `device_d8d3dc343261b9-16gb-512gb-ph` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | CMF | Phone 2 Pro | 8 GB RAM / 128 GB storage | `device_391d612f3650e7-auto-8gb-128gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | CMF | Phone 2 Pro | 8 GB RAM / 256 GB storage | `device_391d612f3650e7-auto-8gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26 Ultra | 12 GB RAM / 256 GB storage | `device_172f055ffd379c-auto-12gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26 Ultra | 12 GB RAM / 512 GB storage | `device_172f055ffd379c-auto-12gb-512gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | vivo | V70 | 8 GB RAM / 256 GB storage | `device_3acf9503580082-auto-8gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | vivo | V70 | 12 GB RAM / 256 GB storage | `device_3acf9503580082-auto-12gb-256gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | vivo | V70 | 12 GB RAM / 512 GB storage | `device_3acf9503580082-auto-12gb-512gb` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | Zenbook 14 (UM3406GA) | UM3406GA-QD123WSM | `config_2b0cd196931eaf` | 11 | 41 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Xiaomi | Pad 8 Pro | 8 GB / 256 GB | `config_49328beb62a309` | 13 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | ASUS | Zenfone 8 | 8 GB RAM / 128 GB storage | `device_bfb5e856a9a659-auto-8gb-128gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | ASUS | Zenfone 8 | 16 GB RAM / 256 GB storage | `device_bfb5e856a9a659-auto-16gb-256gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | OnePlus | 11 5G | 12 GB RAM / 128 GB storage | `device_11074670a799fc-auto-12gb-128gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | OnePlus | 11 5G | 16 GB RAM / 256 GB storage | `device_11074670a799fc-auto-16gb-256gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | ASUS | ROG Phone 8 | 12 GB RAM / 256 GB storage · Phantom Black | `device_fca6be23997740-12-256-black-ph` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | ASUS | ROG Phone 8 | 12 GB RAM / 256 GB storage · Storm Gray | `device_fca6be23997740-12-256-gray-ph` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | ASUS | ROG Phone 8 Pro | 16 GB RAM / 512 GB storage · Phantom Black | `device_92c3d063a77fd3-16-512-ph` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | ASUS | ROG Phone 8 Pro | 24 GB RAM / 1 TB storage · Phantom Black · Pro Edition | `device_92c3d063a77fd3-24-1024-ph` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | REDMAGIC | 9 Pro | 12 GB RAM / 256 GB storage | `device_756f45cfe5400c-auto-12gb-256gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | REDMAGIC | 9 Pro | 16 GB RAM / 512 GB storage | `device_756f45cfe5400c-auto-16gb-512gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Nothing | Phone (3a) Lite | 8 GB RAM / 128 GB storage | `device_7d1a06486f5fce-auto-8gb-128gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Nothing | Phone (3a) Lite | 8 GB RAM / 256 GB storage | `device_7d1a06486f5fce-auto-8gb-256gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OnePlus | 13 | 12 GB RAM / 256 GB storage (OnePlus Philippines spec page) | `device_edc07536e9cd09-12-256-phspec` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OnePlus | 13 | 16 GB RAM / 512 GB storage (OnePlus Philippines spec page) | `device_edc07536e9cd09-16-512-phspec` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OnePlus | 15 | 12 GB RAM / 256 GB storage | `device_613da26efd7a82-auto-12gb-256gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OnePlus | 15 | 16 GB RAM / 512 GB storage | `device_613da26efd7a82-auto-16gb-512gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OnePlus | Nord 5 | 8 GB RAM / 128 GB storage | `device_8ff869a1c2cd22-auto-8gb-128gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | OnePlus | Nord 5 | 12 GB RAM / 512 GB storage | `device_8ff869a1c2cd22-auto-12gb-512gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Redmi | 15C | 4 GB RAM / 128 GB storage | `device_37b298a84397b6-auto-4gb-128gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Redmi | 15C | 6 GB RAM / 128 GB storage | `device_37b298a84397b6-auto-6gb-128gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Redmi | 15C | 8 GB RAM / 256 GB storage | `device_37b298a84397b6-auto-8gb-256gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | tablets | Redmi | Pad 2 Pro | 8 GB / 256 GB | `config_4efe2baa687b69` | 12 | 49 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Xiaomi | 14 | Configuration not recorded | `device_e2f76126f7f83b-unrecorded` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | A52 | 8 GB RAM / 128 GB storage | `device_edb8f688862988-samsung-8gb-128gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | A72 | 8 GB RAM / 128 GB storage | `device_528380ceb337d2-samsung-8gb-128gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | ASUS | ROG Phone 6 | 12 GB RAM / 256 GB storage | `device_67c3c6cf323fd4-auto-12gb-256gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Nothing | Phone (2a) | 8 GB RAM / 128 GB storage | `device_c98433a0c7ffce-auto-8gb-128gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Nothing | Phone (2a) | 12 GB RAM / 256 GB storage | `device_c98433a0c7ffce-auto-12gb-256gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Redmi | 14C | 4 GB RAM / 128 GB storage | `device_42b5f469649788-auto-4gb-128gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Redmi | 14C | 6 GB RAM / 128 GB storage | `device_42b5f469649788-auto-6gb-128gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Redmi | 14C | 8 GB RAM / 256 GB storage | `device_42b5f469649788-auto-8gb-256gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26 | 12 GB RAM / 256 GB storage | `device_9d2bde71f611d2-auto-12gb-256gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26 | 12 GB RAM / 512 GB storage | `device_9d2bde71f611d2-auto-12gb-512gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26 FE | 8 GB RAM / 128 GB storage | `device_6c173ec56f86ac-auto-8gb-128gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26 FE | 8 GB RAM / 256 GB storage | `device_6c173ec56f86ac-auto-8gb-256gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | Samsung | Galaxy S26 FE | 8 GB RAM / 512 GB storage | `device_6c173ec56f86ac-auto-8gb-512gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | A52 | 8 GB RAM / 256 GB storage | `device_edb8f688862988-samsung-8gb-256gb` | 10 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | A72 | 8 GB RAM / 256 GB storage | `device_528380ceb337d2-samsung-8gb-256gb` | 10 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | ASUS | ROG Phone 6 | 16 GB RAM / 512 GB storage | `device_67c3c6cf323fd4-auto-16gb-512gb` | 10 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | tablets | Xiaomi | Pad 8 | 8 GB / 256 GB | `config_6d5db11cec127a` | 10 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | ASUS | ROG Phone 7 | 12 GB RAM / 256 GB storage | `device_3f9fd3e4da0935-auto-12gb-256gb` | 9 | 46 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | ASUS | ROG Phone 7 | 16 GB RAM / 512 GB storage | `device_3f9fd3e4da0935-auto-16gb-512gb` | 9 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Redmi | 13 | 8 GB RAM / 256 GB storage | `device_8ee4324c75a16a-auto-8gb-256gb` | 9 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Lenovo | Tab M10 Plus 3rd Gen | 4 GB RAM / 64 GB storage / 4G LTE (ZAAN0009PH / TB128XU; chipset unresolved) | `device_d34ec0baa2b329-zaan0009ph-4gb-64gb-lte` | 14 | 49 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | Huawei | P60 Pro | 8 GB RAM / 256 GB storage | `device_a41c76670e8533-auto-8gb-256gb` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Xiaomi | Pad Mini | 8 GB / 256 GB | `config_4b5c4d8d92c12d` | 8 | 49 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | Z Fold3 | 12 GB RAM / 256 GB storage | `device_f6ce8c275dee32-samsung-12gb-256gb` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | Z Fold3 | 12 GB RAM / 512 GB storage | `device_f6ce8c275dee32-samsung-12gb-512gb` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | ASUS | ROG Phone 9 FE | 12 GB RAM / 256 GB storage | `device_59b130760709ea-auto-12gb-256gb` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 Pro 5G | 8 GB RAM / 128 GB storage | `device_b4990c6cf5cce8-auto-8gb-128gb` | 6 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | Galaxy S24 | 8 GB RAM / 256 GB storage | `device_f1fa8c58ea3104-auto-8gb-256gb` | 8 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | Galaxy S24 | 8 GB RAM / 512 GB storage | `device_f1fa8c58ea3104-auto-8gb-512gb` | 8 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | Galaxy S24 Ultra | 12 GB RAM / 256 GB storage | `device_32624044543da4-auto-12gb-256gb` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | Samsung | Galaxy S24 Ultra | 12 GB RAM / 512 GB storage | `device_32624044543da4-auto-12gb-512gb` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Xiaomi | 15T | 12 GB RAM / 256 GB storage | `device_cec396af42f346-auto-12gb-256gb` | 6 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Xiaomi | 15T | 12 GB RAM / 512 GB storage | `device_cec396af42f346-auto-12gb-512gb` | 6 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Xiaomi | 15T Pro | 12 GB RAM / 256 GB storage | `device_7c9508acf8b24a-auto-12gb-256gb` | 6 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | Xiaomi | 15T Pro | 12 GB RAM / 512 GB storage | `device_7c9508acf8b24a-auto-12gb-512gb` | 6 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | laptops | Acer | Predator Helios Neo 16 PHN16-72-99K9 | NH.QNNSP.003 | `config_7e6c1ccdc91313` | 5 | 41 | SPECIFICATION_INCOMPLETE |
| 2023 | smartphones | HONOR | X9a | 8 GB RAM / 256 GB storage | `device_beb039b6abbf82-8gb-256gb-ph` | 9 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Lenovo | Tab M10 Plus 3rd Gen | 3 GB RAM / 32 GB storage / Wi-Fi / MediaTek Helio G80 (TB125FU) | `device_d34ec0baa2b329-tb125fu-g80-3gb-32gb-wifi` | 8 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Black Shark | 5 | 8 GB RAM / 128 GB storage | `device_a9d69522a3d0fe-8gb-128gb-ph` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Black Shark | 5 | 12 GB RAM / 256 GB storage | `device_a9d69522a3d0fe-12gb-256gb-ph` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | HONOR | X9b | 12 GB RAM / 256 GB storage | `device_38ef56f303cc59-12gb-256gb-ph` | 13 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | HONOR | X9c | 12 GB RAM / 256 GB storage | `device_bd830ce3628852-12gb-256gb-ph` | 9 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | HONOR | X9d | 12 GB RAM / 256 GB storage | `device_efb3b8a0ab65ed-12gb-256gb-ph` | 8 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Black Shark | 4 | 6 GB RAM / 128 GB storage | `device_fa4c0f6cdc39f6-6gb-128gb-ph` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Black Shark | 4 | 12 GB RAM / 128 GB storage | `device_fa4c0f6cdc39f6-12gb-128gb-ph` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Black Shark | 4 | 12 GB RAM / 256 GB storage | `device_fa4c0f6cdc39f6-12gb-256gb-ph` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 5G | 6 GB RAM / 128 GB storage | `config_adeb944ad88c96` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | laptops | ASUS | ProArt P16 (H7606) | H7606WW-SE021WSM | `device_8cef5fb897991d-h7606ww-se021wsm` | 5 | 41 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | Galaxy S21+ 5G | 8 GB RAM / 256 GB storage | `config_13d4c1daf696b2` | 3 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Xiaomi | Pad 7 | 12 GB RAM / 256 GB storage | `device_d54d421faa66b2-12gb-256gb` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Xiaomi | Pad 7 Pro | 8 GB RAM / 128 GB storage | `device_1fcd05aca0e35c-8gb-128gb` | 20 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Xiaomi | Pad 7 | 8 GB RAM / 128 GB storage | `config_488551c84ada27` | 18 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Xiaomi | Pad 7 | 8 GB RAM / 256 GB storage | `device_d54d421faa66b2-8gb-256gb` | 18 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Xiaomi | Pad 7 Pro | 8 GB RAM / 256 GB storage | `config_207429d6c307c3` | 18 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | Xiaomi | Pad 7 Pro | 12 GB RAM / 512 GB storage | `device_1fcd05aca0e35c-12gb-512gb` | 18 | 49 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Black Shark | 5 Pro | 8 GB RAM / 128 GB storage | `device_abadb9044528e9-8gb-128gb-ph` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | Black Shark | 5 Pro | 12 GB RAM / 256 GB storage | `device_abadb9044528e9-12gb-256gb-ph` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | tablets | Huawei | MatePad Pro 11 (2022) | 8 GB RAM / 256 GB storage / Wi-Fi (GOT-W29) | `device_070c7fa225849f-8gb-256gb-wifi-got-w29` | 11 | 49 | SPECIFICATION_INCOMPLETE |
| 2025 | smartphones | HONOR | 400 | 12 GB RAM / 512 GB storage | `device_32de18b7c0de7e-12gb-512gb-ph` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2026 | smartphones | HONOR | Play 20A | 4 GB RAM / 64 GB storage | `device_111b3317778f61-4gb-64gb-ph` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Black Shark | 4 | 8 GB RAM / 128 GB storage | `device_fa4c0f6cdc39f6-8gb-128gb-ph` | 6 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | Galaxy S21 5G | 8 GB RAM / 256 GB storage | `config_07943b6753bcc7` | 2 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Samsung | Galaxy S21 Ultra 5G | 12 GB RAM / 256 GB storage | `config_aec7e905ce4e48` | 2 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Samsung | Galaxy A56 5G | 8 GB RAM / 256 GB storage | `device_28ca17138af731-8gb-256gb` | 12 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Samsung | Galaxy A56 5G | 8 GB RAM / 128 GB storage | `config_663b8685d47596` | 11 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | POCO | Pad X1 | 8 GB RAM / 512 GB storage | `config_01c13f8793cfc7` | 9 | 49 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Xiaomi | 15 Ultra | 16 GB RAM / 512 GB storage | `config_534999edbd1ef0` | 9 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 Pro 5G | 12 GB RAM / 256 GB storage | `device_b4990c6cf5cce8-12gb-256gb` | 8 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 Pro 5G | 12 GB RAM / 512 GB storage | `device_b4990c6cf5cce8-12gb-512gb` | 8 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | OPPO | Reno5 4G | 8 GB RAM / 128 GB storage | `device_914fe6b0343102-8gb-128gb-ph` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | OPPO | Reno6 5G | 8 GB RAM / 128 GB storage | `device_97f548edfe54b5-8gb-128gb-ph` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2024 | smartphones | HONOR | Magic V3 | 12 GB RAM / 512 GB storage | `device_3e151a6e24dc04-12gb-512gb-ph` | 7 | 46 | SPECIFICATION_INCOMPLETE |
| 2025 | tablets | POCO | Pad M1 | 8 GB RAM / 256 GB storage | `config_65229b275c86d9` | 7 | 49 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 Pro 5G | 8 GB RAM / 256 GB storage | `config_17fbad37e49629` | 6 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | OPPO | A96 | 8 GB RAM / 256 GB storage | `device_98cec94dc9f934-unrecorded` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | F7 | 12 GB RAM / 256 GB storage | `config_d799ea69cae501` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | F7 | 12 GB RAM / 512 GB storage | `device_aa672fab7d46f3-12gb-512gb` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | F7 Pro | 12 GB RAM / 256 GB storage | `config_8686aa695a9d92` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | F7 Pro | 12 GB RAM / 512 GB storage | `device_8817ae147c9edb-12gb-512gb` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 | 6 GB RAM / 128 GB storage | `config_913af9dcd461b1` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 | 8 GB RAM / 128 GB storage | `device_5315b6e9963c31-8gb-128gb` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 | 8 GB RAM / 256 GB storage | `device_5315b6e9963c31-8gb-256gb` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 5G | 8 GB RAM / 256 GB storage | `device_f473ccfae26096-8gb-256gb` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Redmi | Note 14 5G | 12 GB RAM / 512 GB storage | `device_f473ccfae26096-12gb-512gb` | 5 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | OnePlus | Nord 2 | 12 GB RAM / 256 GB storage — Gray Sierra | `device_15827b1eab335d-12gb-256gb-ph` | 4 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | F7 Ultra | 12 GB RAM / 256 GB storage | `config_1bb046ae479c43` | 4 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | F7 Ultra | 16 GB RAM / 512 GB storage | `device_c63651e46ba072-16gb-512gb` | 4 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | X7 Pro | 8 GB RAM / 256 GB storage | `config_f31bfff33ae82b` | 4 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | X7 Pro | 12 GB RAM / 256 GB storage | `device_a8a17a9d88abab-12gb-256gb` | 4 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | POCO | X7 Pro | 12 GB RAM / 512 GB storage | `device_a8a17a9d88abab-12gb-512gb` | 4 | 46 | SPECIFICATION_INCOMPLETE |
| 2022 | smartphones | OPPO | A77s | 8 GB RAM / 128 GB storage | `device_3dc0d9f8e23b3a-unrecorded` | 3 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Xiaomi | 15 | 12 GB RAM / 256 GB storage | `config_058cc95f012890` | 2 | 46 | SPECIFICATION_INCOMPLETE |
| Unassigned | smartphones | Xiaomi | 15 | 12 GB RAM / 512 GB storage | `device_ab1ddec763e1d7-12gb-512gb` | 2 | 46 | SPECIFICATION_INCOMPLETE |
| 2021 | smartphones | Motorola | Moto G50 | 4 GB RAM / 128 GB storage | `device_195cb093808ae0-4gb-128gb-ph` | 6 | 46 | SPECIFICATION_COMPLETE_WITH_DISCLOSED_GAPS |
| 2021 | smartphones | Motorola | Edge 20 Pro | 12 GB RAM / 256 GB storage | `device_cef4dc913ac418-12gb-256gb-ph` | 5 | 46 | SPECIFICATION_COMPLETE_WITH_DISCLOSED_GAPS |
| 2021 | smartphones | OnePlus | Nord 2 | 8 GB RAM / 128 GB storage — Blue Haze | `device_15827b1eab335d-8gb-128gb-ph` | 4 | 46 | SPECIFICATION_INCOMPLETE |

## Philippine market and image coverage

- Models with an exact-match catalog image carrying a reusable license: 48/456. The remaining 408 show the neutral unavailable-image placeholder.
- Of those unavailable images, 50 require reuse permission, 29 have reuse rights that are not established, and 329 have no reliable exact-model match recorded.
- The workbook copy's `IMAGE AUDIT` sheet records each image's source, credit, license, rights-check date, and the reason an image is unavailable. Images without documented reuse rights are not published.
- Excluded master records: 3; held-out records/claims: 7. These are visible with explicit labels but stay outside eligible searches/recommendations.
- The public site retains each record's existing verification and scope status. This specification audit does not upgrade Philippine availability status.

## Reference source policy

- **Official manufacturer documentation** (`official_manufacturer`): Allowed only after robots.txt permits the exact page; follow site terms and record the page actually checked. Can support a specification or product identity when it describes the exact device or configuration.
- **[Pinoy Techno Guide](https://www.pinoytechnoguide.com/)** (`pinoy_techno_guide`): Existing collector may fetch exact product pages only when robots.txt permits; do not copy descriptions or images. Independent Philippine-market evidence; corroborate material technical claims against manufacturer documentation where available.
- **[NanoReview](https://nanoreview.net/), [robots.txt](https://nanoreview.net/robots.txt)** (`nanoreview`): Blocked for automated GPT research: robots.txt disallows GPTBot and ChatGPT-User. Do not fetch pages with a disguised user agent. Link-only candidate in this project. Do not claim a page was checked or promote NanoReview-derived values from this automated run.
- **[Kimovil](https://www.kimovil.com/en/), [terms](https://www.kimovil.com/en/info/terms-and-conditions)** (`kimovil`): No automated content extraction. Its terms prohibit reproducing, copying, distributing, transforming, or modifying site content without express written authorization. Link-only candidate in this project. Do not store copied descriptions, images, or scraped specifications; verify candidates against sources that permit reuse.
- **[Notebookcheck](https://www.notebookcheck.net/)** (`notebookcheck`): Check robots.txt and terms for each exact URL; use source URLs and concise factual evidence only. Secondary evidence; retain conflicts until independently resolved.

## Scope and limitations

- NanoReview and Kimovil are included as manual discovery/reference links. No NanoReview specifications were collected because its published robots rules disallow GPT/ChatGPT automated access. Kimovil specifications and images were not extracted because its terms restrict copying or transformation without express authorization.
- The automated collector made 18 laptop-page attempts without extracting structured laptop specifications. A separate manual review added official manufacturer evidence for 18/18 laptop models across 22 exact configurations; the laptop records remain incomplete where fields are still pending.
- `NOT_DISCLOSED`, `UNAVAILABLE_AFTER_RESEARCH`, `CONFLICTING_INFORMATION`, and `NOT_APPLICABLE` are reserved for field decisions supported by actual research. They are not assigned by guesswork.
- `DEVICEIQ_RESEARCH_PROGRESS.md` records actual source-extraction counts and remaining work by claimed year, category, and brand.
