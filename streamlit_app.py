import pandas
import streamlit
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('View Our Fruit List - Add Your Favorites!')

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

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

# quierying trial account metadata
streamlit.header("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

#don't run anything past here while we troubleshoot
#streamlit.stop()

#adding another text entry box
#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        #my_cur.execute("insert into fruit_load_list values ('from streamlit')")
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
        return "Thanks for adding " + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)

#don't run anything past here while we troubleshoot
streamlit.stop()
