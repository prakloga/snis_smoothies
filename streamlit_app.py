# Import Python packages
# A warehouse will usually shut down within a few minutes of being idle (check the Auto-Suspend setting of the warehouse), 
# but when a warehouse is associated with a SiS app, it runs for a minimum of 15 minutes by default. 
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

# Add a Name Box for Smoothie Orders
# STREAMLIT DOCUMENTATION: https://docs.streamlit.io/library/api-reference/widgets/st.text_input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# We will use Streamlit's documentation to get sample code
# https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox

# Display fruit options list in Streamlit in Snowflake(SiS)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5 # We found the max_selections does what we need it to do. 
                     # But it's also a little wonky because it seems to give you the alert when you choose your fifth item instead of waiting until you try to add a 6th.
)

# New section to display smoothiefroot nutrition information
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response)
#st.text(smoothiefroot_response.json())
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# We can use the st.write() and st.text() methods to take a closer look at what is contained in our ingredients LIST. 
# Cleaning Up Empty Brackets
# actually means...if ingredients_list is not null: then do everything below this line that is indented. 
if ingredients_list:
    # Changing the LIST to a STRING
    # Create variable to hold string value
    ingredients_string = '' 
    # Use FOR loop to convert LIST to String
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' ' # Add space after each fruit name
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    # Output the string
    #st.write(ingredients_string)

    # Build a SQL insert statement
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                        values('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop() # The Streamlit Stop command is great for troubleshooting
    time_to_insert = st.button('Submit Order')
        
    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
