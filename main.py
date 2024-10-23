import streamlit as st
import pandas as pd

# Function to calculate the total based on inputs
def calculate_plan(daily_walk, walks_per_week, grooming, vet_checkup, training_sessions, months, discount):
    # Dog walk calculations
    walk_cost = daily_walk * walks_per_week * 4 * months * 500  # 500 per walk
    # Grooming cost per session
    grooming_cost = grooming * months * 3000  # 3000 per grooming session
    # Vet checkup cost per session
    vet_cost = vet_checkup * months * 3500  # 3500 per vet checkup
    # Dog training cost per session
    training_cost = training_sessions * months * 2000  # 2000 per training session

    # Total cost without discount
    total_cost = walk_cost + grooming_cost + vet_cost + training_cost

    # Apply discount
    discounted_cost = total_cost * (1 - discount / 100)

    return round(total_cost, 2), round(discounted_cost, 2)

# Streamlit UI
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
        }
        .table {
            font-size: 20px; /* Increased text size */
        }
    </style>
""", unsafe_allow_html=True)

st.title("Tails on Trails - Pet Service Subscription Calculator")

# Sidebar for user input
st.sidebar.title("Select Plan Type")
plan_type = st.sidebar.selectbox("Plan Type", ["Half-Yearly", "Quarterly", "Monthly"])

st.sidebar.title("Service Parameters")
daily_walk = st.sidebar.number_input("Daily Walks (per day)", min_value=0, value=1, step=1,max_value=2)
walks_per_week = st.sidebar.number_input("Walks per Week", min_value=0, value=1, step=1,max_value=7)
grooming = st.sidebar.number_input("Grooming Sessions per Month", min_value=0, value=1, step=1,max_value=28)
vet_checkup = st.sidebar.number_input("Vet Checkups per Month", min_value=0, value=1, step=1,max_value=28)
training_sessions = st.sidebar.number_input("Training Sessions per Month", min_value=0, value=1, step=1,max_value=28)
customers = st.sidebar.number_input("Number of Customers", min_value=1, value=1, step=1,max_value=28)

# Define the months and discount rate based on the selected plan
if plan_type == "Half-Yearly":
    months = 6
    discount = 30  # 30% discount
elif plan_type == "Quarterly":
    months = 3
    discount = 20  # 20% discount
else:
    months = 1
    discount = 10  # 10% discount

# Call the function to calculate the total and discounted cost
total_cost, discounted_cost = calculate_plan(daily_walk, walks_per_week, grooming, vet_checkup, training_sessions, months, discount)

# Add option for a la carte services
st.header("A La Carte Services")

ala_dog_walks = st.number_input("Additional Dog Walks", min_value=0, step=1)
ala_grooming_sessions = st.number_input("Additional Grooming Sessions", min_value=0, step=1)
ala_vet_checkups = st.number_input("Additional Vet Checkups", min_value=0, step=1)
ala_training_sessions = st.number_input("Additional Training Sessions", min_value=0, step=1)

# Calculate the cost of additional a la carte services
ala_walk_cost = ala_dog_walks * 500  # 500 per additional walk
ala_grooming_cost = ala_grooming_sessions * 3000  # 3000 per additional grooming session
ala_vet_cost = ala_vet_checkups * 3500  # 3500 per additional vet checkup
ala_training_cost = ala_training_sessions * 2000  # 2000 per additional training session

# Total a la carte cost
total_ala_carte = ala_walk_cost + ala_grooming_cost + ala_vet_cost + ala_training_cost

# Grand total for all customers (including the subscription plan and a la carte)
grand_total = discounted_cost * customers + total_ala_carte

# Calculate GST (assumed at 18%)
gst_rate = 0.18
gst_amount = grand_total * gst_rate
final_balance_with_gst = grand_total + gst_amount

# Display the results in a table format
st.header(f"**{plan_type} Plan Summary - Balance Sheet**")

# A La Carte Table
st.subheader("A La Carte Services")
ala_carte_data = {
    "Service": ["Additional Dog Walks", "Additional Grooming Sessions", "Additional Vet Checkups", "Additional Training Sessions"],
    "Unit Cost (rs)": [500, 3000, 3500, 2000],
    "Quantity": [ala_dog_walks, ala_grooming_sessions, ala_vet_checkups, ala_training_sessions],
    "Total Cost (rs)": [round(ala_walk_cost, 2), round(ala_grooming_cost, 2), round(ala_vet_cost, 2), round(ala_training_cost, 2)]
}
ala_carte_df = pd.DataFrame(ala_carte_data)
st.dataframe(ala_carte_df.style.set_table_attributes('class="table"'), use_container_width=True)

# Subscription Plan Table
st.subheader(f"{plan_type} Subscription Plan")
subscription_data = {
    "Item": [
        f"Daily Walks ({walks_per_week} walks/week)",
        f"Grooming ({grooming} per month)",
        f"Vet Checkups ({vet_checkup} per month)",
        f"Training ({training_sessions} per month)",
        "Total Cost (before discount)",
        f"Discount ({discount}% off)",
        "Final Cost (after discount)"
    ],
    "Cost (rs)": [
        round(daily_walk * walks_per_week * 4 * months * 500, 2),
        round(grooming * months * 3000, 2),
        round(vet_checkup * months * 3500, 2),
        round(training_sessions * months * 2000, 2),
        round(total_cost, 2),
        round(total_cost * (discount / 100), 2),
        round(discounted_cost, 2)
    ]
}
subscription_df = pd.DataFrame(subscription_data)
st.dataframe(subscription_df.style.set_table_attributes('class="table"'), use_container_width=True)

# Final Balance Table with GST
st.subheader("Final Balance with GST")
final_balance_data = {
    "Description": ["Subscription Plan Cost", "Total A La Carte Cost", "Subtotal", "GST (18%)", "Grand Total (Including GST)"],
    "Amount (rs)": [
        round(discounted_cost * customers, 2),
        round(total_ala_carte, 2),
        round(grand_total, 2),
        round(gst_amount, 2),
        round(final_balance_with_gst, 2)
    ]
}
final_balance_df = pd.DataFrame(final_balance_data)

# Display the final balance table without highlighting the grand total
st.table(final_balance_df.style.set_table_attributes('class="table"'))

# Footer
st.write("---")
st.write("**Tails on Trails** - Bringing the best care to your pets!")
