# 🏠 Example: Real Estate data generation
## This example demonstrates how to generate realistic real estate data where field values are derived from other fields using `context`.
### The final property price depends on:
- apartment area (m²),
- location,
- date of last renovation.
---
## Pricing model
### Price per square meter
```python
PRICE_PER_SQM = {
    "city_center": 3000,
    "near_center": 2000,
    "suburbs": 1200,
}
```
### Renovation age coefficient
- Renovation <= 3 years -> +15%
- Renovation <= 10 years -> no change
- Renovation > 10 years -> -15%
---
## Price calculation function
```python
def calculate_price(context: dict) -> float:
    area = context["area"]
    location = context["location"]
    renovation_date = context["last_renovation"]

    base_price = area * PRICE_PER_SQM[location]
    years_since_renovation = (TODAY - renovation_date).days / 365

    if years_since_renovation <= 3:
        coef = 1.15
    elif years_since_renovation <= 10:
        coef = 1.0
    else:
        coef = 0.85

    return round(base_price * coef, 2)
```
The function receives `context` - a dictionary with previously generated fields of the current row - and returns the computed price.
---
## RealEstate data generator
```python
class RealEstate(BaseDataGen):
    __count__ = 10

    location: Choice(["city_center", "near_center", "suburbs"])
    area: Float(min=25, max=200, precision=1)
    last_renovation: Date(start="1995-01-01", end=TODAY.isoformat())
    price: Float(func=calculate_price)
    title: Str(func=lambda ctx: f"{ctx['area']} m² apartment in {ctx['location']}")
```
### Field dependencies
- `price` depends on: `area`, `location`, `last_renovation`
- `title` depends on: `area`, `location`

⚠️ Fields that use `context` must be declared after the fields they depend on.
---
## Generating the file
```python
RealEstate.generate("data.csv")
```
---
## Generated output example
```csv
location,    area,  last_renovation, price,    title
suburbs,     137.8, 2000-09-25,      140556.0, 137.8 m² apartment in suburbs
near_center, 87.2,  1998-09-11,      148240.0, 87.2 m² apartment in near_center
near_center, 96.9,  2023-08-04,      222870.0, 96.9 m² apartment in near_center
city_center, 134.9, 1996-11-19,      343995.0, 134.9 m² apartment in city_center
near_center, 157.0, 2010-06-14,      266900.0, 157.0 m² apartment in near_center
suburbs,     199.6, 2015-05-19,      203592.0, 199.6 m² apartment in suburbs
suburbs,     172.8, 2004-05-25,      176256.0, 172.8 m² apartment in suburbs
near_center, 89.6,  1995-07-14,      152320.0, 89.6 m² apartment in near_center
suburbs,     112.8, 2019-02-07,      135360.0, 112.8 m² apartment in suburbs
city_center, 111.9, 2006-10-08,      285345.0, 111.9 m² apartment in city_center
```