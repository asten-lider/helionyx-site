# Yandex stock snapshot — 2026-10-28

Owner provided *two* stock columns: Ozon quantity and own local warehouse quantity. Only local warehouse stock is authoritative for direct sales. This CSV contains the 14 SKUs with **positive confirmed local warehouse stock**, not Ozon stock. Actual quantities are recorded below separately to preserve auditability; the YML generator uses in_stock status only.

- BAT1C6500: 237 local units; site price 2990 RUB
- BAT1C5200: 159 local units; site price 2790 RUB
- BATRO6500: 106 local units; site price 2990 RUB
- BAT1T6500: 108 local units; site price 2890 RUB
- BAT1T5200: 28 local units; site price 2590 RUB
- BATEXVAC660_3200: 56 local units; site price 2090 RUB
- BATJET70: 222 local units; site price 4490 RUB
- BATJET60: 45 local units; site price 4490 RUB
- BATLGA9: 83 local units; site price 3390 RUB
- BATMOP2_3200: 8 local units; site price 1990 RUB
- BATG1_3200: 168 local units; site price 2090 RUB
- BATJET90: 117 local units; site price 4790 RUB
- BATDYSV6_2500: 77 local units; site price 3090 RUB
- BATDYSV7_2500: 40 local units; site price 3190 RUB

**Excluded:** BATMOP2LITE3200 (no local count), BATMOPP3200 (no local count), BATDYSV11_4000 (not in provided stock list). Unknown is not the same as zero; these offers are omitted, not marked available.

This is a dated snapshot, **not a live inventory integration**. Before publishing or re-exporting, confirm current local quantities and the live site price, especially BATJET90 (owner-confirmed 4790 RUB). Never publish a YML price different from the corresponding product page and checkout price. Do not submit a feed unless that match is verified. Ozon warehouse units are deliberately not used.
