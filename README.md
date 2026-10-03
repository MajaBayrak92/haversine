# Haversine

Great-circle distance between two latitude/longitude points, using the Haversine formula.

```python
from haversine import haversine, haversine_unit

london = (51.5074, -0.1278)
paris  = (48.8566, 2.3522)

haversine(london, paris)                         # meters (float)
haversine_unit(london, paris, unit="kilometers") # kilometers (float)
haversine_unit(london, paris, unit="miles")      # miles (float)
```

## Why

Pure standard-library Python, no dependencies. The Haversine formula assumes
the Earth is a sphere with a single radius; this library uses the mean Earth
radius (6,371,000.8 m). For most applications the error from this assumption
is well under 0.5%. If you need ellipsoidal accuracy you need a different
library.

## Edge cases

- **Antipodal points**: handled by clamping the `asin` argument to `[0, 1]`.
- **Longitude wrap**: a pair like `(0, 179)` to `(0, -179)` is treated as a
  2° difference. No normalization of the input coordinates is done; this
  library expects latitude in `[-90, 90]` and longitude in `[-180, 180]`.

## Exported names

- `haversine(a, b, radius=EARTH_RADIUS_METERS)` — distance in the unit of `radius`
- `haversine_unit(a, b, unit="meters")` — distance in a named unit
- `EARTH_RADIUS_METERS`, `EARTH_RADIUS_KILOMETERS`, `EARTH_RADIUS_MILES`,
  `EARTH_RADIUS_NAUTICAL_MILES`

Valid units for `haversine_unit`: `"meters"`, `"kilometers"`, `"km"`,
`"miles"`, `"nautical_miles"`.
