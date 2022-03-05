### **Pypsa-Eur compatible DGP dataset for Ukraine (UA) and the Republic of Moldova (MD)**

This short and script (jupyter notebook) is developed as pre-processing toolkit to be used in an extended version of pypsa-eur that also colvers the Ukraine and the Republic of moldova.

**Input**:
* _GDP_PPP_30arcsec_v3.nc_: raw dataset. Available at: [M. Kummu, M. Taka, J. H. A. Guillaume. (2020), Data from: Gridded global datasets for Gross Domestic Product and Human Development Index over 1990-2015, Dryad, Dataset. doi: https://doi.org/10.5061/dryad.dk1j0] - **_PLEASE DOWNLOAD YOURSELF_**! -
* _regions_onshore.geojson_: `pypsa-eur` output file, available after executing the workflow in `pypsa-eur/resources/regions_onshore.geojson`

**Output**:
_GDP_PPP_30arcsec_v3_mapped.csv_: file that maps the pypsa-eur onshore regions in UA and MD to it's associated GDP value.

**Requirements**:
* python
* xarray
* geopandas
* pandas
* xagg
