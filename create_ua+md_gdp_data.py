
import numpy as np
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
import xagg as xa
import pandas as pd

gdp = xr.open_dataset('data/GDP_per_capita_PPP_1990_2015_v2.nc').sel(time=2015).GDP_per_capita_PPP
pop = (rxr.open_rasterio('data/ppp_2013_1km_Aggregated.tif').sel(band=1)
       .rename({'x': 'longitude', 'y': 'latitude'}))
onshore_region = gpd.read_file('data/regions_onshore.geojson').query("country in ['UA', 'MD']")

idx = onshore_region.index[0]
x = onshore_region.loc[idx].x
y = onshore_region.loc[idx].y

# create cutouts
region_cutout = onshore_region.loc[idx:idx]
gdp_cutout = gdp.sel(longitude=slice(x-.5, x+.5), latitude=slice(y+.5, y-.5))
pop_cutout = (pop.sel(longitude=slice(x-.5, x+.5), latitude=slice(y+.5, y-.5))
              .where(lambda x: x>=0, np.nan))

# interpolate different resolutions
gdp_cutout = gdp_cutout.interp_like(pop_cutout)

# weighting for gdp and pop
gdp_pop_cutout = (0.6 * gdp_cutout + 0.4) * pop_cutout

weightmap = xa.pixel_overlaps(gdp_pop_cutout, region_cutout)
aggregated = xa.aggregate(gdp_pop_cutout, weightmap)

gdp_pop_df = pd.DataFrame(
    columns = aggregated.to_dataset().name,
    index = ['pop_gdp', 'country'],
    data = [aggregated.to_dataset()['var'].values, aggregated.to_dataset()['country'].values]
).T

gdp_pop_df.to_csv('results/ppp_2013_1km_Aggregated_and_GDP_per_capita_PPP_1990_2015_v2_mapped.csv')

# for some reason, passing all gdp+regions doesn't work. therefore, solve in a for-loop
counter = 1
print(f"{counter}/{len(onshore_region)}")
print("--- --- ---")
for idx in onshore_region.index[1:]:
    x = onshore_region.loc[idx].x
    y = onshore_region.loc[idx].y

    # create cutouts
    region_cutout = onshore_region.loc[idx:idx]
    gdp_cutout = gdp.sel(longitude=slice(x-.5, x+.5), latitude=slice(y+.5, y-.5))
    pop_cutout = (pop.sel(longitude=slice(x-.5, x+.5), latitude=slice(y+.5, y-.5))
                  .where(lambda x: x>=0, np.nan))

    # interpolate different resolutions
    gdp_cutout = gdp_cutout.interp_like(pop_cutout)

    # combine datasets with different weighting for gdp and pop
    gdp_pop_cutout = (0.6 * gdp_cutout + 0.4) * pop_cutout
    
    weightmap = xa.pixel_overlaps(gdp_pop_cutout, region_cutout)
    aggregated = xa.aggregate(gdp_pop_cutout, weightmap)
    
    gdp_pop_cutout_df = pd.DataFrame(
        columns = aggregated.to_dataset().name,
        index = ['pop_gdp', 'country'],
        data = [aggregated.to_dataset()['var'].values, aggregated.to_dataset()['country'].values]
    ).T
    
    gdp_pop_df = gdp_pop_df.append(gdp_pop_cutout_df)
    gdp_pop_df.to_csv(
        'results/ppp_2013_1km_Aggregated_and_GDP_per_capita_PPP_1990_2015_v2_mapped.csv'
    )
    
    counter+=1
    print(f"{counter}/{len(onshore_region)}")
    print("--- --- ---")
