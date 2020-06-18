import pandas as pd
import folium
import streamlit as st

st.write("""
# Covid-19 Cases Visualization
This app shows the confirmed cases in Austria!
""")

# Coordinates of the states
coor_info = pd.read_html("https://www.distancelatlong.com/country/austria")
coordinates = pd.DataFrame(coor_info[2])
coordinates['States'] = coordinates['States'].apply(lambda x: x[:-4].strip())
coordinates.rename(columns={'States': 'State'}, inplace=True)

# confirmed cases
case_info = pd.read_html('https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Austria')
austria_cases = pd.DataFrame(case_info[3])
austria_cases.drop(austria_cases.columns[[0, 4, 5]], axis=1, inplace=True)
austria_cases.rename(columns={'Recov.': 'Recoveries'}, inplace=True)

st.subheader('Confirmed cases for states')
st.write(austria_cases)

austria_cases = austria_cases.iloc[:-1, :]
coordinates['State'] = austria_cases['State']

# merge to obtain final data frame
merged_data = pd.merge(coordinates, austria_cases, how='inner', on='State')

austria = folium.Map(location=[47.5162, 14.5501], zoom_start=6)
for state, lat, long, total_cases, Death, Recov, Active in zip(list(merged_data['State']),
                                                               list(merged_data['Latitude']),
                                                               list(merged_data['Longitude']),
                                                               list(merged_data['Total Cases']),
                                                               list(merged_data['Deaths']), list(merged_data['Recoveries']),
                                                               list(merged_data['Active'])):
    # for creating circle marker
    folium.CircleMarker(location=[lat, long],
                        radius=5,
                        color='red',
                        fill=True,
                        fill_color="red").add_to(austria)
    # for creating marker
    folium.Marker(location=[lat, long],
                  # adding information that need to be displayed on popup
                  popup=folium.Popup(('<strong><b>State  : ' + state + '</strong> <br>' +
                                      '<strong><b>Total Cases : ' + str(total_cases) + '</striong><br>' +
                                      '<strong><font color= red>Deaths : </font>' + str(Death) + '</striong><br>' +
                                      '<strong><font color=green>Recoveries : </font>' + str(Recov) + '</striong><br>' +
                                      '<strong><b>Active Cases : ' + str(Active) + '</striong>'),
                                     max_width=200)).add_to(austria)

st.markdown(austria._repr_html_(), unsafe_allow_html=True)
