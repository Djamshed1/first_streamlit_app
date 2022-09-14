import pandas
import streamlit
import requests

streamlit.title('My Parents New Health Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🍌 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥭 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥝 Hard-Boiled Free-Range Egg')
streamlit.text('🍇 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Give customers the ability to choose by fruit names
my_fruit_list = my_fruit_list.set_index('Fruit')

#We want to filter the table data based on the fruits a customer will choose, so we'll pre-populate the list to set an example for the customer.
#Let's put a pick list here so they can pick the fruit they want to include
#Filter the Table Data. We'll ask our app to put the list of selected fruits into a variable called fruits_selected. 
#Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the full data set 
#(and assign that data to a variable called fruits_to_show). 
#Finally, we'll ask the app to use the data in fruits_to_show in the dataframe it displays on the page. 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# take the json version of the response and normilize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it the screen as a table
streamlit.dataframe(fruityvice_normalized)
