## First Homework for ATS780 Machine Learning for the Atmosphere Sciences
### Using Random Forests to Assess the Utility of Using the MJO to Predict TTT Intensity


Tropical Temperate Troughs (TTTs) are the dominant rainfall producers over
southern Africa during austral summer. TTTs are defined by a NW-SE oriented
cloud band which connectes the tropical Atlantic Ocean to the extratropical
Indian Ocean. TTTs can account for 25-40% of rainy season rainfall
in some locations in South Africa and represent an important synoptic scale
feature of this regions climate. [Ratna et al. 2013](https://www.researchgate.net/profile/Satyaban-B-Ratna/publication/257411681_An_index_for_tropical_temperate_troughs_over_Southern_Africa/links/0c960532934d565482000000/An-index-for-tropical-temperate-troughs-over-Southern-Africa.pdf) developed an index for TTT
intensity based on Outgoing longwave radiation (OLR) and 850 hPa winds.

The Madden-Julian Oscillation (MJO) is an intraseasonal oscillation (30-90 day
time period) with many teleconnections within the tropics, extratropics, and
even the polar regions. The MJO initiates in the western tropical Indian Ocean
and over coastal equatorial eastern Africa. Due to its proximity and influence
it has been speculated that the MJO may influence the intensity and timing of
TTTs, results however in understanding or even proving such a teleconnection
have been mixed.

The goal of this project is to try and classify whether or not a TTT event is
occurring based on the values from a modified version of the Ratna et al. 2013
index and data from ERA5 as well the OLR MJO Index (OMI). 

### Data Used
- Daily Mean Interpolated OLR from NOAA PSL (1979 - Present)
- 1981-2010 Mean Interpolated OLR from NOAA PSL
- OLR MJO Index (OMI) from NOAA PSL (01/01/1979 - 12/31/2022)
- q850, u850, v850, z200, surface pressure, and w500 from ERA5 (01/01/1979-12/31/2022)
- OLR Derived TTT Index based on Ratna et al. 2013
