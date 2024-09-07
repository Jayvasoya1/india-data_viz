import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="India Data Visualization Dashboard",
    page_icon="favicon.ico",
    layout='wide'
)
st.title('India Data Visualization Dashboard')
df = pd.read_csv('india.csv')

list_of_state = list(df['State'].unique())
list_of_state.insert(0, 'Overall India')

columns_to_extract = ['Population', 'sex_ratio', 'lieracy_rate',
                      'Households_with_Internet', 'Households_with_Computer',
                      'Households_with_Car_Jeep_Van']

st.sidebar.title('India ka Data Vizz')

action_type = st.sidebar.radio('Select Action', ['Plot Graph', 'Comparison'])

selected_state = st.sidebar.selectbox('Select State', list_of_state)

if action_type == 'Plot Graph':
    primary = st.sidebar.selectbox('Select Primary Parameter', sorted(columns_to_extract))
    secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(columns_to_extract))

    plot_graph = st.sidebar.button('Plot Graph')

    if plot_graph:
        st.markdown(f'''
                   <div style="font-size:24px; font-weight:bold; color:#4a90e2; background-color:#f5f5f5; padding:10px; border-radius:5px; text-align:center;">
                       Size represents <span style="color:#d0021b;">{primary}</span>
                   </div>
                   <div style="font-size:24px; font-weight:bold; color:#4a90e2; background-color:#f5f5f5; padding:10px; border-radius:5px; text-align:center;">
                       Color represents <span style="color:#d0021b;">{secondary}</span>
                   </div>
               ''', unsafe_allow_html=True)

        if selected_state == 'Overall India':
            filtered_df = df.copy()
            fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude",
                                    zoom=3,color=secondary ,size=primary,size_max=35,
                                    width=1200,height=600,hover_name='District')

            fig.update_layout(mapbox_style="carto-positron",
                              mapbox_zoom=3,
                              mapbox_center={"lat": df["Latitude"].mean(),
                                             "lon": df["Longitude"].mean()})

            st.plotly_chart(fig,use_container_width=True)
        else:
            state_df = df[df['State'] == selected_state]

            fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude",
                                    zoom=6, color=secondary, size=primary, size_max=35,
                                    width=1200, height=600, hover_name='District')

            fig.update_layout(mapbox_style="carto-positron",
                              mapbox_zoom=6,
                              mapbox_center={"lat": state_df["Latitude"].mean(),
                                             "lon": state_df["Longitude"].mean()})

            st.plotly_chart(fig, use_container_width=True)


elif action_type == 'Comparison':
    comparison_type = st.sidebar.radio('Select Comparison Type',
                                       ['Male vs Female', 'Hindu vs Muslim', 'Workers by Type'])

    plot_comparison = st.sidebar.button('Plot Comparison')

    if plot_comparison:
        if selected_state == 'Overall India':
            filtered_df = df.copy()
        else:
            filtered_df = df[df['State'] == selected_state]

        if comparison_type == 'Male vs Female':
            male_total = filtered_df['Male'].sum()
            female_total = filtered_df['Female'].sum()
            fig = px.pie(names=['Male', 'Female'], values=[male_total, female_total],
                         title=f'Male vs Female Population in {selected_state}')
            st.plotly_chart(fig)

        elif comparison_type == 'Hindu vs Muslim':
            hindu_total = filtered_df['Hindus'].sum()
            muslim_total = filtered_df['Muslims'].sum()
            fig = px.pie(names=['Hindus', 'Muslims'], values=[hindu_total, muslim_total],
                         title=f'Hindu vs Muslim Population in {selected_state}')
            st.plotly_chart(fig)

        elif comparison_type == 'Workers by Type':
            main_workers = filtered_df['Main_Workers'].sum()
            marginal_workers = filtered_df['Marginal_Workers'].sum()
            cultivator_workers = filtered_df['Cultivator_Workers'].sum()
            agricultural_workers = filtered_df['Agricultural_Workers'].sum()
            household_workers = filtered_df['Household_Workers'].sum()
            other_workers = filtered_df['Other_Workers'].sum()
            fig = px.pie(names=['Main Workers', 'Marginal Workers', 'Cultivator Workers',
                                'Agricultural Workers', 'Household Workers', 'Other Workers'],
                         values=[main_workers, marginal_workers, cultivator_workers,
                                 agricultural_workers, household_workers, other_workers],
                         title=f'Workers by Type in {selected_state}')
            st.plotly_chart(fig)
