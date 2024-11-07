import requests
import streamlit as st

st.set_page_config(layout="wide")

@st.cache_data
def get_hotels():
    """Return a list of hotels from the API."""
    api_endpoint = st.secrets["api"]["endpoint"]
    response = requests.get(f"{api_endpoint}/Hotels", timeout=10)
    
    # デバッグのため、ステータスコードとレスポンス内容を出力
    st.write(f"Status Code: {response.status_code}")
    st.write("Response Text:", response.text)
    
    # レスポンスが正常でJSON形式であることを確認
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Error: APIからのレスポンスがJSON形式ではありません。")
            return []
    else:
        st.error(f"Error: APIリクエストが失敗しました。ステータスコード: {response.status_code}")
        return []

@st.cache_data
def get_hotel_bookings(hotel_id):
    """Return a list of bookings for the specified hotel."""
    api_endpoint = st.secrets["api"]["endpoint"]
    response = requests.get(f"{api_endpoint}/Hotels/{hotel_id}/Bookings", timeout=10)
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Error: APIからのレスポンスがJSON形式ではありません。")
            return []
    else:
        st.error(f"Error: APIリクエストが失敗しました。ステータスコード: {response.status_code}")
        return []

@st.cache_data
def invoke_chat_endpoint(question):
    """Invoke the chat endpoint with the specified question."""
    api_endpoint = st.secrets["api"]["endpoint"]
    response = requests.post(f"{api_endpoint}/Chat", data={"message": question}, timeout=10)
    
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Error: APIリクエストが失敗しました。ステータスコード: {response.status_code}")
        return "Error in API request"

def main():
    """Main function for the Chat with Data Streamlit app."""

    st.write(
    """
    # API Integration via Semantic Kernel

    This Streamlit dashboard is intended to demonstrate how we can use
    the Semantic Kernel library to generate SQL statements from natural language
    queries and display them in a Streamlit app.

    ## Select a Hotel
    """
    )

    # Display the list of hotels as a drop-down list
    hotels_json = get_hotels()
    hotels = [{"id": hotel.get("hotelID", "Unknown"), "name": hotel.get("hotelName", "Unknown")} for hotel in hotels_json]
    
    selected_hotel = st.selectbox("Hotel:", hotels, format_func=lambda x: x["name"] if x else "No hotels available")

    # Display the list of bookings for the selected hotel as a table
    if selected_hotel:
        hotel_id = selected_hotel["id"]
        bookings = get_hotel_bookings(hotel_id)
        st.write("### Bookings")
        st.table(bookings)

    st.write(
        """
        ## Ask a Bookings Question

        Enter a question about hotel bookings in the text box below.
        Then select the "Submit" button to call the Chat endpoint.
        """
    )

    question = st.text_input("Question:", key="question")
    if st.button("Submit"):
        with st.spinner("Calling Chat endpoint..."):
            if question:
                response = invoke_chat_endpoint(question)
                st.write(response)
                st.success("Chat endpoint called successfully.")
            else:
                st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
