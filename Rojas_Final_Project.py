"""
Class: CS230--Section 4 
Name: Paula Rojas Castellanos
Description: Final Project
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

sidebar = st.sidebar.selectbox("Find what you want to know about Fast Food in the US:",
                               ["Choose an option", "Find Restaurants in a Map!",
                                "How many restaurants are there in my city?", "How many of YOUR favorite "
                                "Restaurants are there?", "How many restaurants are there by Zipcode?",
                                "I want to see the Restaurants' Website Information!", "Show me Trendy Places to Eat at!",
                                "Want to see the Complete Data Set?"])


# FUNCTIONS

# Reading the data and QUERY to return values in California
def read_data():
    data = pd.read_csv("Fast Food Restaurants.csv").set_index("id")
    main = data.query("province == 'CA'")
    return main


# DataFrame - Filtering by Selected Cities
def filtering_city(data, list1):
    data_frame1 = pd.DataFrame()
    for i in list1:
        data_frame1 = data_frame1.append(data[data['city'] == i])
    return data_frame1


# DataFrame - Filtering by Restaurant Categories
def filtering_category(data, list1):
    data_frame2 = pd.DataFrame()
    for i in list1:
        data_frame2 = data_frame2.append(data[data['categories'] == i])
    return data_frame2


# DataFrame - Filtering by Postal Code
def filtering_code(data, list1):
    data_frame3 = pd.DataFrame()
    for i in list1:
        data_frame3 = data_frame3.append(data[data['postalCode'] == i])
    return data_frame3


# DataFrame - Filtering by Restaurant Name
def filtering_name(data, list1):
    data_frame4 = pd.DataFrame()
    for i in list1:
        data_frame4 = data_frame4.append(data[data['name'] == i])
    return data_frame4


# Counting the frequency of Cities selected
def freq_dict(dict, selection):
    dict_frequency = {}
    for i in dict.keys():
        if dict[i][selection] not in dict_frequency.keys:
            item = dict[i][selection]
            dict_frequency[item] = 1
        else:
            item = dict[i][selection]
            dict_frequency[item] += 1
        return dict_frequency


# List of cities in California
def cities():
    data_frame1 = read_data()
    cities_list = []
    for ind, row in data_frame1.iterrows():
        if row['city'] not in cities_list:
            cities_list.append(row['city'])
    cities_list.sort()
    return cities_list


# List of categories in the data
def categories():
    data_frame2 = read_data()
    categories_list = []
    for ind, row in data_frame2.iterrows():
        if row['categories'] not in categories_list:
            categories_list.append(row['categories'])
    categories_list.sort()
    return categories_list


# List of California postal codes
def zip_code():
    data_frame3 = read_data()
    post_list = []
    for ind, row in data_frame3.iterrows():
        if row['postalCode'] not in post_list:
            post_list.append(row['postalCode'])
    post_list.sort()
    return post_list


# List of restaurants names
def restaurants():
    data_frame4 = read_data()
    restaurant_list = []
    for ind, row in data_frame4.iterrows():
        if row['name'] not in restaurant_list:
            restaurant_list.append(row['name'])
    restaurant_list.sort()
    return restaurant_list


# Creating a map with all the restaurants in California
def create_map(dataframe):
    st.title("All of California's Restaurants in a Map!")
    map_df = dataframe.filter(['name', 'latitude', 'longitude'])
    view_state = pdk.ViewState(
        latitude=map_df["latitude"].mean(),
        longitude=map_df["longitude"].mean(),
        zoom=5)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=map_df,
                       get_position='[longitude,latitude]',
                       get_radius=1000,
                       get_color=[255, 0, 255],
                       pickable=True)
    tool_tip = {"html": "Restaurant Name:<br/> <b>{name}</b>",
                "style": {"backgroundColor": "steelblue",
                          "color": "white"}}
    map1 = pdk.Deck(
        map_style='mapbox://style/mapbox/navigation-night-v1',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip=tool_tip)
    st.pydeck_chart(map1)


# Creating a bar chart of restaurants per City
def bar(x, y, colors):
    plt.style.use('fivethirtyeight') # Cool theme I found to make my charts more interactive
    plt.bar(x, y)
    fig, ax = plt.subplots(figsize=(15, 8))
    width = 0.4
    ax.bar(x, y, width=width, align='center', color=colors, linewidth=width * 2, edgecolor='black')
    plt.title("Frequency of Restaurants per City", fontname="Courier New", fontsize=25)
    plt.ylabel("Num of Restaurants", fontname="Courier New", fontsize=20)
    plt.xlabel("Cities in California", fontname="Courier New", fontsize=20)
    plt.xticks(rotation=0, fontname="Courier New")
    plt.yticks(fontname="Courier New")
    return plt


# Pie chart of the Different Restaurant Names
def pie_chart(sizes, list):
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.pie(sizes, labels=list, autopct='%1.1f%%', startangle=90,
           wedgeprops={'linewidth': 3, 'edgecolor': 'white'})
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle) # Making my Pie Chart a Donut Chart!
    ax.axis('equal')
    plt.title("Percentage of Restaurants per Name")
    return plt


# Histogram of No. of restaurants by ZipCode
def zip_histogram(zipcodes):
    plt.style.use('fivethirtyeight') # Cool theme I found to make my charts more interactive
    plt.subplots(figsize=(15, 8))
    plt.hist(zipcodes, bins=[90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000], color="lightblue", ec="darkblue", lw=2) # The function bins separates the marks in the x-axis
    plt.title("Histogram of Restaurants by Zipcode", fontname="Courier New", fontsize=25)
    plt.xlabel('Zipcodes', fontname="Courier New", fontsize=20)
    plt.ylabel('No. of Restaurants within the Zipcode', fontname="Courier New", fontsize=20)
    plt.show()
    plt.xticks(rotation=0, fontname="Courier New")
    plt.yticks(fontname="Courier New")
    return plt


# THE DIFFERENT PAGES:

# Open Data for Streamlit
df = read_data()

# Display Entry Page
if sidebar == "Choose an option":
    st.title("The Hungry Californian")
    st.subheader("Are you in California and wondering where to eat next? Click on the SideBar to find out!")
    st.image("https://scontent-bos3-1.xx.fbcdn.net/v/t1.6435-9/32161261_1716789848402906_4079559116849152000_n.jpg?_nc_cat=108&ccb=1-6&_nc_sid=09cbfe&_nc_ohc=na3XRr3LugEAX8VQpWG&_nc_ht=scontent-bos3-1.xx&oh=00_AT-FI9hXJcM0DV5VjwOL0hxN3yLlvaHXVqAm9ut4k9yxuQ&oe=629E94F7")
    st.write(
        f"Fast-Food Restaurants: From over 10,000 fast food restaurants Nation-wide provided by "
        "Datafiniti's Business Database, I have selected those located in the sunny state of California. "
        "This program includes includes all of the things you would like to know about your favorite "
        "restaurants! Through various graphs, maps, videos, and links to external websites,"
        " I have created an interactive app useful to those eating in California")

# Data Set
if sidebar == "Want to see the Complete Data Set?":
    st.title("Data Set with all of California's Fast Food Restaurants:")
    st.write(df)  # QUESTION: Just want to show certain columns here
    # PUT THE FILTER

# map with all the restaurants
if sidebar == "Find Restaurants in a Map!":
    create_map(df)

# MULTISELECT of Cities in California they want to see and BAR CHART
if sidebar == "How many restaurants are there in my city?":
    c_list = cities()
    st.title("Number of Restaurants in cities around California!")
    select_city = st.multiselect("Select the City", c_list,
                                 default=["Anaheim", "Los Angeles",
                                          "San Diego", "Palo Alto", "San Francisco"])
    df = read_data()
    new_df = filtering_city(df, select_city)
    groups = new_df.groupby('city').count()
    st.write(groups.name)
    color = st.selectbox("Select a color", ["red", "blue", "green", "yellow", "purple", "black"])
    dict1 = groups.name.to_dict()
    st.pyplot(bar(dict1.keys(), dict1.values(), color))

# PIE CHART of Percentage of Restaurant Names
if sidebar == "How many of YOUR favorite Restaurants are there?":
    names_list = restaurants()
    st.title("YOUR favorite Restaurants in Sunny California!")
    select_name = st.multiselect("Select a Restaurant Name", names_list,
                                 default=["Subway", "Pizza Hut", "In-N-Out Burger", "Taco Bell",
                                          "Burger King", "Subway"])
    df = read_data()
    df2 = filtering_name(df, select_name)
    groups2 = df2.groupby('name').count()
    st.write(groups2.province)
    dict2 = groups2.province.to_dict()
    st.pyplot(pie_chart(dict2.values(), dict2.keys()))

# Frequency of Zipcodes through Histogram
if sidebar == "How many restaurants are there by Zipcode?":
    new_df2 = read_data()
    zipCodes = new_df2['postalCode']
    c_list = zipCodes.tolist()
    codes_list = [int(i) for i in c_list]
    st.title("All Restaurants per ZipCode!")
    st.pyplot(zip_histogram(codes_list))

# EXTRA: Restaurant's Website (User chooses the restaurant)
if sidebar == "I want to see the Restaurants' Website Information!":
    st.title("Find YOUR favorite Restaurant's Website!")
    restaurants_list = restaurants()
    df = read_data()
    select_restaurant = st.selectbox("Select a Restaurant", restaurants_list)
    new_df3 = filtering_name(df, [select_restaurant])
    menu = st.button(f"Find the Websites to different {select_restaurant}")
    web_list = new_df3.websites.tolist()
    if menu:
        st.write(f"Check out all the links:\n")
        for w in range(len(web_list)):
            st.write(web_list[w])

# EXTRA: YouTube Videos with Trendy Places to eat at
if sidebar == "Show me Trendy Places to Eat at!":
    st.title("Some YouTube videos with great recommendations!")
    st.header("TOP Trendy Places to Eat in California!")
    st.video("https://www.youtube.com/watch?v=6pwj3G00XKw")
    st.header("This one is for those in L.A.!")
    st.video("https://www.youtube.com/watch?v=cIUFJhjqZqg&t=9s")
