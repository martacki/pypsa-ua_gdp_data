import xarray as xr
import geopandas as gpd
import xagg as xa
import pandas as pd

gdp = xr.open_dataset('data/GDP_PPP_30arcsec_v3.nc').sel(time=2015)
onshore_region = gpd.read_file('data/regions_onshore.geojson').query("country in ['UA', 'MD']")


idx = onshore_region.index[0]
x = onshore_region.loc[idx].x
y = onshore_region.loc[idx].y

region_cutout = onshore_region.loc[idx:idx]
gdp_cutout = gdp.sel(longitude=slice(x-.5, x+.5), latitude=slice(y+.5, y-.5))

weightmap = xa.pixel_overlaps(gdp_cutout, region_cutout)
aggregated = xa.aggregate(gdp_cutout, weightmap)

gdp_ua_df = pd.DataFrame(
    columns = aggregated.to_dataset().name,
    index = ['GDP_PPP', 'country'],
    data = [aggregated.to_dataset().GDP_PPP.values, aggregated.to_dataset().country.values]
).T

gdp_ua_df.to_csv('results/GDP_PPP_30arcsec_v3_mapped.csv')

# for some reason, passing all gdp+regions doesn't work. therefore, solve in a for-loop

counter = 1
print(f"{counter}/{len(onshore_region)}")
print("--- --- ---")
for idx in onshore_region.index[1:]:
    x = onshore_region.loc[idx].x
    y = onshore_region.loc[idx].y

    region_cutout = onshore_region.loc[idx:idx]
    gdp_cutout = gdp.sel(longitude=slice(x-.5, x+.5), latitude=slice(y+.5, y-.5))
    
    weightmap = xa.pixel_overlaps(gdp_cutout, region_cutout)
    aggregated = xa.aggregate(gdp_cutout, weightmap)
    
    gdp_ua_df_cutout = pd.DataFrame(
        columns = aggregated.to_dataset().name,
        index = ['GDP_PPP', 'country'],
        data = [aggregated.to_dataset().GDP_PPP.values, aggregated.to_dataset().country.values]
    ).T
    
    gdp_ua_df = gdp_ua_df.append(gdp_ua_df_cutout)
    gdp_ua_df.to_csv('results/GDP_PPP_30arcsec_v3_mapped.csv')
    
    counter+=1
    print(f"{counter}/{len(onshore_region)}")
    print("--- --- ---")
