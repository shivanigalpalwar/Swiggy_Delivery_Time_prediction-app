import streamlit as st
import pandas as pd
import pickle
import base64

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Swiggy Delivery Time Prediction",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

# Use the same swiggy_img.png file as a soft, full-page background.
with open(r"C:\Users\LENOVO\Downloads\swiggy_img.png", "rb") as image_file:
    background_image = base64.b64encode(image_file.read()).decode("utf-8")

st.markdown(f"""
<style>

    /* Full-page background image with a light translucent overlay */
    .stApp {{
        background:
            linear-gradient(rgba(255, 248, 242, 0.76), rgba(255, 248, 242, 0.76)),
            url("data:image/png;base64,{background_image}") center center / cover fixed no-repeat;
    }}

    /* Remove default top padding */
    .block-container {{
        padding-top: 4.1rem;
        padding-bottom: 0.45rem;
        max-width: 1450px;
    }}

    /* Main title */
    .main-title {{
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        color: #e85d04;
        margin-bottom: 5px;
    }}

    .subtitle {{
        text-align: center;
        color: #777777;
        font-size: 17px;
        margin-bottom: 8px;
    }}

    /* Section headers */
    .section-title {{
        background: linear-gradient(90deg, #ff6b35, #ff9f1c);
        color: white;
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 17px;
        font-weight: 700;
        margin-top: 6px;
        margin-bottom: 4px;
        box-shadow: 0px 4px 12px rgba(255, 107, 53, 0.14);
    }}

    /* Input cards */
    .input-card {{
        background: rgba(255,255,255,0.72);
        padding: 10px;
        border-radius: 16px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.06);
        border: 1px solid #f1f1f1;
        margin-bottom: 15px;
    }}

    /* Prediction result */
    .prediction-card {{
        background: linear-gradient(135deg, #ff6b35, #f77f00);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        color: white;
        margin-top: 8px;
        box-shadow: 0px 8px 25px rgba(247,127,0,0.3);
    }}

    .prediction-title {{
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 5px;
    }}

    .prediction-value {{
        font-size: 38px;
        font-weight: 800;
    }}

    /* Predict button */
    div.stButton > button {{
        width: 100%;
        height: 55px;
        border-radius: 14px;
        border: none;
        background: linear-gradient(90deg, #ff6b35, #f77f00);
        color: white;
        font-size: 20px;
        font-weight: 700;
        transition: 0.3s;
        box-shadow: 0px 6px 18px rgba(247,127,0,0.25);
    }}

    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0px 10px 25px rgba(247,127,0,0.35);
    }}

    /* Labels */
    label {{
        font-weight: 700 !important;
        color: #222222 !important;
        font-size: 15px !important;
    }}

    /* Clean white input controls - removes the dark blue/black look */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] {{
        background-color: #ffffff !important;
        border: 1px solid #e7e1dc !important;
        border-radius: 10px !important;
        color: #333333 !important;
    }}

    div[data-baseweb="input"] input,
    div[data-baseweb="select"] input {{
        color: #333333 !important;
        background-color: #ffffff !important;
    }}

    div[data-baseweb="select"] span {{
        color: #333333 !important;
    }}

    div[data-baseweb="select"] svg {{
        fill: #666666 !important;
    }}

    /* Compact number inputs */
    div[data-testid="stNumberInput"] button {{
        background-color: #fff8f3 !important;
        color: #f26b38 !important;
        border: none !important;
    }}

    /* Keep the sliders clean and orange */
    div[data-testid="stSlider"] [role="slider"] {{
        background-color: #ff6b35 !important;
    }}

    /* Reduce vertical spacing between widgets */
    div[data-testid="stVerticalBlock"] {{
        gap: 0.25rem;
    }}

    /* Make the prediction button slightly shorter */
    div.stButton > button {{
        height: 48px;
        border-radius: 12px;
        font-size: 18px;
    }}

    /* Image styling */
    .hero-image {{
        border-radius: 20px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.12);
    }}

    /* Subtle translucent surfaces behind Streamlit content */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.16);
        border-radius: 12px;
    }}

    /* Keep form rows compact */
    div[data-testid="stNumberInput"],
    div[data-testid="stSelectbox"],
    div[data-testid="stSlider"] {{
        margin-bottom: 0 !important;
    }}

    /* Footer */
    .footer {{
        text-align: center;
        color: #999999;
        font-size: 13px;
        margin-top: 20px;
        padding-top: 10px;
        border-top: 1px solid #eeeeee;
    }}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------

model = pickle.load(open("swiggy.pkl", "rb"))


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🍔 Swiggy Delivery Time Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Predict your estimated food delivery time using machine learning</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# DELIVERY & DRIVER INFORMATION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🚴 Delivery & Driver Information</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    age = st.number_input("Age", 18, 60, 25)

with col2:
    distance = st.number_input(
        "Distance (km)",
        0.5,
        30.0,
        5.0
    )

with col3:
    pickup_time = st.number_input(
        "Pickup Time (minutes)",
        1,
        60,
        15
    )

with col4:
    ratings = st.slider("Ratings", 1.0, 5.0, 4.0)


col1, col2, col3 = st.columns(3)

with col1:
    multiple_deliveries = st.number_input(
        "Multiple Deliveries",
        min_value=0,
        max_value=5,
        value=1
    )

with col2:
    vehicle_condition = st.selectbox(
        "Vehicle Condition",
        [0, 1, 2]
    )

with col3:
    vehicle_type = st.selectbox(
        "Vehicle Type",
        [
            "motorcycle",
            "scooter",
            "electric_scooter",
            "bicycle"
        ]
    )


# ---------------------------------------------------------
# ORDER INFORMATION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🍕 Order Information</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    order_type = st.selectbox(
        "Order Type",
        ["snack", "meal", "drinks", "buffet"]
    )

with col2:
    day_of_week = st.selectbox(
        "Day of Week",
        [
            "saturday",
            "friday",
            "tuesday",
            "monday",
            "sunday",
            "wednesday",
            "thursday"
        ]
    )

with col3:
    is_weekend = st.selectbox(
        "Is Weekend",
        ["no", "yes"]
    )

with col4:
    order_hour = st.slider(
        "Order Time (Hour)",
        0,
        23,
        12
    )


# ---------------------------------------------------------
# ENVIRONMENT & TRAFFIC INFORMATION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🌦️ Traffic & Environment</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    weather = st.selectbox(
        "Weather",
        [
            "sunny",
            "cloudy",
            "fog",
            "stormy",
            "sandstorms",
            "windy"
        ]
    )

with col2:
    traffic = st.selectbox(
        "Traffic",
        [
            "low",
            "medium",
            "high",
            "jam"
        ]
    )

with col3:
    festival = st.selectbox(
        "Festival",
        ["no", "yes"]
    )

with col4:
    city = st.selectbox(
        "City Type",
        [
            "urban",
            "metropolitian",
            "semi-urban"
        ]
    )


# ---------------------------------------------------------
# PREDICTION BUTTON
# ---------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])

with predict_col2:

    if st.button("🚀 Predict Delivery Time ⏱️"):

        # -------------------------------------------------
        # CREATE INPUT DATAFRAME
        # -------------------------------------------------

        input_df = pd.DataFrame({
            "age": [age],
            "ratings": [ratings],
            "weather": [weather],
            "traffic": [traffic],
            "vehicle_condition": [vehicle_condition],
            "type_of_order": [order_type],
            "type_of_vehicle": [vehicle_type],
            "festival": [festival],
            "city_type": [city],
            "distance": [distance],
            "is_weekend": [is_weekend],
            "order_time_hour": [order_hour],
            "order_day_of_week": [day_of_week],
            "pickup_time_minutes": [pickup_time],
            "multiple_deliveries": [multiple_deliveries]
        })


        # -------------------------------------------------
        # DATA FIXES
        # -------------------------------------------------

        input_df["is_weekend"] = input_df["is_weekend"].map({
            "no": 0,
            "yes": 1
        })


        # -------------------------------------------------
        # FEATURE ENGINEERING
        # -------------------------------------------------

        input_df["distance_per_delivery"] = (
            input_df["distance"] /
            (input_df["multiple_deliveries"] + 1)
        )

        input_df["is_peak_hour"] = input_df[
            "order_time_hour"
        ].apply(
            lambda x: 1 if 18 <= x <= 22 else 0
        )

        input_df["is_rush"] = (
            (input_df["traffic"] == "jam") &
            (input_df["is_weekend"] == 1)
        ).astype(int)

        input_df["weekend_peak"] = (
            (input_df["is_weekend"] == 1) &
            (input_df["is_peak_hour"] == 1)
        ).astype(int)


        # -------------------------------------------------
        # COLUMN ORDER
        # -------------------------------------------------

        input_df = input_df[
            [
                "age",
                "ratings",
                "weather",
                "traffic",
                "vehicle_condition",
                "type_of_order",
                "type_of_vehicle",
                "festival",
                "city_type",
                "distance",
                "is_weekend",
                "order_time_hour",
                "order_day_of_week",
                "pickup_time_minutes",
                "multiple_deliveries",
                "distance_per_delivery",
                "is_peak_hour",
                "is_rush",
                "weekend_peak"
            ]
        ]


        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        try:

            prediction = model.predict(input_df)

            prediction_value = round(prediction[0], 2)

            st.markdown(
                f"""
                <div class="prediction-card">
                    <div class="prediction-title">
                        📦 Estimated Delivery Time
                    </div>
                    <div class="prediction-value">
                        {prediction_value:.2f} Minutes
                    </div>
                    <div>
                        Your order's estimated arrival time 🚴🍔
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error("❌ Error in prediction")
            st.write(e)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        🤖 Machine Learning • Food Delivery Prediction • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)

