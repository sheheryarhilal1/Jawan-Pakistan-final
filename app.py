import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import joblib
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NEXORA | Customer Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PREMIUM UI
# =========================================================

st.markdown("""
<style>

/* =========================
   GLOBAL
========================= */

.stApp {
    background:
        radial-gradient(
            circle at 85% 10%,
            rgba(0, 174, 255, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 10% 80%,
            rgba(79, 70, 229, 0.08),
            transparent 25%
        ),
        #070b14;
    color: #e8eef7;
}

.main .block-container {
    padding: 2.2rem 3rem 3rem 3rem;
    max-width: 1500px;
}


/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0a1220 0%,
            #07101c 100%
        );
    border-right: 1px solid rgba(255,255,255,0.07);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

.sidebar-brand {
    padding: 10px 8px 25px 8px;
}

.sidebar-logo {
    width: 46px;
    height: 46px;
    border-radius: 14px;
    background: linear-gradient(
        135deg,
        #00c6ff,
        #0072ff
    );
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    font-weight: 800;
    color: black;
    box-shadow:
        0 10px 30px rgba(0, 150, 255, 0.25);
    margin-bottom: 14px;
}

.sidebar-title {
    font-size: 21px;
    font-weight: 800;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    letter-spacing: -0.5px;
}

.sidebar-subtitle {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 12px;
    margin-top: 4px;
}


/* =========================
   NAVIGATION
========================= */

div[data-testid="stRadio"] label {
    color: #9aabc0 !important;
    font-size: 14px !important;
}

div[data-testid="stRadio"] > div {
    gap: 7px;
}

div[data-testid="stRadio"] label:hover {
    color: #ffffff !important;
}


/* =========================
   HEADINGS
========================= */

.hero-title {
    font-size: 40px;
    font-weight: 850;
    letter-spacing: -1.5px;
    margin-bottom: 5px;
    color: #ffffff;
}

.hero-gradient {
    background: linear-gradient(
        90deg,
        #ffffff,
        #5ddcff
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #8496ab;
    font-size: 15px;
    margin-bottom: 28px;
}

.section-title {
    color: #f0f5fb;
    font-size: 19px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 15px;
}


/* =========================
   KPI CARDS
========================= */

/* =========================================================
   NEXORA — KPI CARD THEME ONLY
========================================================= */

[data-testid="stMetric"] {
    position: relative;

    background:
        linear-gradient(
            145deg,
            #101c2d 0%,
            #0b1524 55%,
            #09111e 100%
        );

    border: 1px solid rgba(0, 198, 255, 0.16);

    border-radius: 18px;

    padding: 22px 22px 20px 22px;

    min-height: 125px;

    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.22),
        inset 0 1px 0 rgba(255, 255, 255, 0.035);

    overflow: hidden;

    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}


/* Top cyan accent */

[data-testid="stMetric"]::before {
    content: "";

    position: absolute;

    top: 0;
    left: 0;

    width: 100%;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00c6ff,
            #008cff,
            transparent
        );

    opacity: 0.85;
}


/* Glow circle */

[data-testid="stMetric"]::after {
    content: "";

    position: absolute;

    width: 110px;
    height: 110px;

    right: -55px;
    top: -55px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(0, 198, 255, 0.12),
            rgba(0, 198, 255, 0.02) 55%,
            transparent 70%
        );

    pointer-events: none;
}


/* Hover */

[data-testid="stMetric"]:hover {

    transform: translateY(-4px);

    border-color:
        rgba(0, 198, 255, 0.34);

    box-shadow:
        0 18px 38px rgba(0, 0, 0, 0.28),
        0 0 25px rgba(0, 174, 255, 0.06);
}


/* KPI label */

[data-testid="stMetricLabel"] {

    color: #7f94aa !important;

    font-size: 10px !important;

    font-weight: 800 !important;

    letter-spacing: 1.1px !important;

    text-transform: uppercase;

    position: relative;

    z-index: 2;
}


/* KPI value */

[data-testid="stMetricValue"] {

    color: #f4f8fc !important;

    font-size: 29px !important;

    font-weight: 850 !important;

    letter-spacing: -0.8px;

    margin-top: 7px;

    position: relative;

    z-index: 2;
}


/* Delta */

[data-testid="stMetricDelta"] {

    font-size: 10px !important;

    font-weight: 700 !important;

    position: relative;

    z-index: 2;
}

/* =========================
   CARDS
========================= */

.glass-card {
    background:
        linear-gradient(
            145deg,
            rgba(19, 31, 49, 0.88),
            rgba(9, 17, 29, 0.88)
        );
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 24px;
    box-shadow:
        0 18px 45px rgba(0,0,0,0.16);
}

.mini-label {
    color: #71849a;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.mini-value {
    color: #f5f8fc;
    font-size: 25px;
    font-weight: 800;
    margin-top: 6px;
}


/* =========================
   INPUTS
========================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #0c1624 !important;
    color: #edf4fb !important;
    border: 1px solid #23364d !important;
    border-radius: 11px !important;
}

.stTextArea textarea {
    min-height: 150px;
}


/* =========================
   BUTTON
========================= */

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 11px;
    padding: 11px 18px;
    font-weight: 750;
    color: white;
    background: linear-gradient(
        135deg,
        #009dff,
        #1769ff
    );
    box-shadow:
        0 10px 25px rgba(0, 126, 255, 0.20);
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 14px 30px rgba(0, 126, 255, 0.30);
}


/* =========================
   DATAFRAME
========================= */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    overflow: hidden;
}


/* =========================
   ALERTS
========================= */

.stAlert {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08);
}


/* =========================
   DIVIDER
========================= */

hr {
    border-color: rgba(255,255,255,0.07) !important;
}


/* =========================
   HIDE STREAMLIT BRANDING
========================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}



/* =========================
   STATUS BADGES
========================= */

.status-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 30px;
    background: rgba(0, 198, 255, 0.10);
    border: 1px solid rgba(0, 198, 255, 0.20);
    color: #5ddcff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.7px;
}



</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE
# =========================================================

@st.cache_data
def load_data():

    connection = sqlite3.connect("ecommerce_hackathon.db")

    customers = pd.read_sql(
        "SELECT * FROM customers",
        connection
    )

    products = pd.read_sql(
        "SELECT * FROM products",
        connection
    )

    orders = pd.read_sql(
        "SELECT * FROM orders",
        connection
    )

    reviews = pd.read_sql(
        "SELECT * FROM reviews",
        connection
    )

    connection.close()

    return customers, products, orders, reviews


customers, products, orders, reviews = load_data()


# =========================================================
# CLEAN ORDERS
# =========================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

orders = orders.dropna(
    subset=["order_date"]
)

orders["net_revenue"] = (
    orders["quantity"]
    * orders["unit_price"]
    * (1 - orders["discount"])
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    
    st.markdown("<br>", unsafe_allow_html=True)

    page = st.radio(
        "WORKSPACE",
        [
            "📊  Dashboard",
            "🎯  Churn Prediction",
            "💬  Sentiment Analysis"
        ],
        label_visibility="visible"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("AI • Analytics • Customer Intelligence")
    st.caption("Version 1.0")


# =========================================================
# PAGE 1 — DASHBOARD
# =========================================================

if page == "📊  Dashboard":

    st.markdown(
        '<div class="hero-title">'
        'Business <span class="hero-gradient">Intelligence</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Real-time overview of revenue, customers, orders and product performance.'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # KPIs
    # =====================================================

    total_revenue = orders["net_revenue"].sum()

    total_orders = orders["order_id"].nunique()

    total_customers = customers["customer_id"].nunique()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}"
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    col4.metric(
        "Average Order Value",
        f"${average_order_value:,.0f}"
    )


    # =====================================================
    # MONTHLY REVENUE
    # =====================================================

    st.markdown(
        '<div class="section-title">Revenue Performance</div>',
        unsafe_allow_html=True
    )

    monthly_revenue = (
        orders
        .assign(
            year_month=
            orders["order_date"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("year_month")["net_revenue"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        monthly_revenue.set_index("year_month"),
        height=350
    )


    # =====================================================
    # CATEGORY
    # =====================================================

    st.markdown(
        '<div class="section-title">Product Performance</div>',
        unsafe_allow_html=True
    )

    dashboard_data = orders.merge(
        products[
            ["product_id", "category"]
        ],
        on="product_id",
        how="left"
    )

    category_revenue = (
        dashboard_data
        .groupby("category")["net_revenue"]
        .sum()
        .sort_values(ascending=False)
    )


    col1, col2 = st.columns([1.15, 0.85])


    with col1:

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        st.write("### Revenue by Category")

        st.bar_chart(
            category_revenue,
            height=320
        )

        st.markdown("</div>", unsafe_allow_html=True)


    with col2:

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        st.write("### Top Products")

        top_products = (
            dashboard_data
            .groupby("product_id")["net_revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )

        top_products = top_products.merge(
            products[
                ["product_id", "product_name"]
            ],
            on="product_id",
            how="left"
        )

        top_products["Revenue"] = (
            top_products["net_revenue"]
            .map(lambda x: f"${x:,.0f}")
        )

        st.dataframe(
            top_products[
                ["product_name", "Revenue"]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("</div>", unsafe_allow_html=True)


    # =====================================================
    # CITY REVENUE
    # =====================================================

    st.markdown(
        '<div class="section-title">Customer Geography</div>',
        unsafe_allow_html=True
    )

    city_data = orders.merge(
        customers[
            ["customer_id", "city"]
        ],
        on="customer_id",
        how="left"
    )

    city_revenue = (
        city_data
        .groupby("city")["net_revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        city_revenue,
        height=320
    )



# =========================================================
# PAGE 2 — CHURN PREDICTION
# =========================================================

elif page == "🎯  Churn Prediction":


    st.markdown(
        """
       
        """,
        unsafe_allow_html=True
    )

   


    # =====================================================
    # LOAD CHURN MODEL
    # =====================================================

    model_path = "models/churn.pkl"

    if not os.path.exists(model_path):

        st.error(
            "Churn model not found. "
            "Please make sure churn.pkl exists inside the models folder."
        )

        st.stop()


    try:

        loaded_model = joblib.load(model_path)

        # -------------------------------------------------
        # DIRECT MODEL
        # -------------------------------------------------

        if hasattr(loaded_model, "predict"):

            churn_model = loaded_model


        # -------------------------------------------------
        # DICTIONARY MODEL
        # -------------------------------------------------

        elif isinstance(loaded_model, dict):

            churn_model = None

            possible_keys = [
                "model",
                "classifier",
                "churn_model",
                "best_model",
                "pipeline",
                "clf",
                "estimator",
                "nn_model"
            ]

            for key in possible_keys:

                if key in loaded_model:

                    candidate = loaded_model[key]

                    if hasattr(candidate, "predict"):

                        churn_model = candidate

                        break


            # -------------------------------------------------
            # SEARCH ALL VALUES
            # -------------------------------------------------

            if churn_model is None:

                for value in loaded_model.values():

                    if hasattr(value, "predict"):

                        churn_model = value

                        break


            if churn_model is None:

                st.error(
                    "No valid prediction model was found inside churn.pkl."
                )

                st.stop()


        else:

            st.error(
                "Invalid churn.pkl model format."
            )

            st.stop()


    except Exception:

        st.error(
            "Unable to load the churn model. "
            "Please verify models/churn.pkl."
        )

        st.stop()


    # =====================================================
    # CUSTOMER PROFILE
    # =====================================================

 


    # =====================================================
    # INPUTS
    # =====================================================

    col1, col2, col3 = st.columns(3)


    # =====================================================
    # COLUMN 1
    # =====================================================

    with col1:

        total_orders_input = st.number_input(
            "Total Orders",
            min_value=1,
            max_value=1000000,
            value=5,
            step=1,
            key="nexora_churn_total_orders"
        )

        total_spending_input = st.number_input(
            "Total Spending",
            min_value=0.0,
            value=500.0,
            step=10.0,
            key="nexora_churn_total_spending"
        )

        average_order_value_input = st.number_input(
            "Average Order Value",
            min_value=0.0,
            value=100.0,
            step=10.0,
            key="nexora_churn_average_order_value"
        )


    # =====================================================
    # COLUMN 2
    # =====================================================

    with col2:

        days_since_last_order_input = st.number_input(
            "Days Since Last Order",
            min_value=0,
            value=30,
            step=1,
            key="nexora_churn_days_since_last_order"
        )

        return_rate_input = st.number_input(
            "Return Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01,
            key="nexora_churn_return_rate"
        )

        average_delivery_days_input = st.number_input(
            "Average Delivery Days",
            min_value=0.0,
            value=5.0,
            step=0.5,
            key="nexora_churn_delivery_days"
        )


    # =====================================================
    # COLUMN 3
    # =====================================================

    with col3:

        age_input = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
            key="nexora_churn_age"
        )

        membership_input = st.selectbox(
            "Membership Type",
            [
                "Basic",
                "Premium",
                "Standard"
            ],
            key="nexora_churn_membership"
        )


    # =====================================================
    # MODEL INFO
    # =====================================================

  


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # =====================================================
    # PREDICT BUTTON
    # =====================================================

    predict = st.button(
        "◈  RUN CHURN PREDICTION",
        use_container_width=True,
        key="nexora_run_churn_prediction"
    )


    # =====================================================
    # PREDICTION
    # =====================================================

    if predict:

        try:

            # =================================================
            # ONE-HOT ENCODING
            # =================================================

            membership_basic = (
                1 if membership_input == "Basic" else 0
            )

            membership_premium = (
                1 if membership_input == "Premium" else 0
            )

            membership_standard = (
                1 if membership_input == "Standard" else 0
            )


            # =================================================
            # 10 FEATURES
            #
            # 7 NUMERIC
            # +
            # 3 MEMBERSHIP
            # =
            # 10
            # =================================================

            input_data = np.array(
                [[
                    total_orders_input,
                    total_spending_input,
                    average_order_value_input,
                    days_since_last_order_input,
                    return_rate_input,
                    average_delivery_days_input,
                    age_input,
                    membership_basic,
                    membership_premium,
                    membership_standard
                ]],
                dtype=np.float32
            )


            # =================================================
            # CHECK EXPECTED FEATURES
            # =================================================

            expected_features = None

            try:

                expected_features = int(
                    churn_model.input_shape[-1]
                )

            except Exception:

                try:

                    expected_features = int(
                        churn_model.n_features_in_
                    )

                except Exception:

                    expected_features = None


            # =================================================
            # FEATURE COUNT VALIDATION
            # =================================================

            if (
                expected_features is not None
                and expected_features != input_data.shape[1]
            ):

                st.error(
                    f"Model expects {expected_features} features, "
                    f"but the application generated "
                    f"{input_data.shape[1]} features."
                )

                st.stop()


            # =================================================
            # PREDICT
            # =================================================

            try:

                prediction_raw = churn_model.predict(
                    input_data,
                    verbose=0
                )

            except TypeError:

                prediction_raw = churn_model.predict(
                    input_data
                )


            prediction_array = np.asarray(
                prediction_raw
            )


            # =================================================
            # EXTRACT PROBABILITY
            # =================================================

            if prediction_array.ndim == 2:

                probability = float(
                    prediction_array[0][0]
                )

            else:

                probability = float(
                    prediction_array[0]
                )


            # =================================================
            # NORMALIZE
            # =================================================

            probability = max(
                0.0,
                min(
                    1.0,
                    probability
                )
            )


            # =================================================
            # CLASSIFICATION
            # =================================================

            prediction = (
                1
                if probability >= 0.50
                else 0
            )


            # =================================================
            # RESULT HEADER
            # =================================================

            st.markdown(
                """
                 """,
                unsafe_allow_html=True
            )


            # =================================================
            # RESULT COLUMNS
            # =================================================

            result_col, probability_col = st.columns(2)


            # =================================================
            # STATUS
            # =================================================

            with result_col:

                if prediction == 1:

                    st.markdown(
                        """
                        <div class="churn-result-card danger">

                            <div class="result-icon">
                                ⚠
                            </div>

                            <div>

                                <div class="mini-label">
                                    PREDICTED STATUS
                                </div>

                                <div class="result-main">
                                    HIGH CHURN RISK
                                </div>

                                <div class="result-detail">
                                    The model predicts an elevated
                                    likelihood of customer churn.
                                </div>

                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        """
                        <div class="churn-result-card safe">

                            <div class="result-icon">
                                ✓
                            </div>

                            <div>

                                <div class="mini-label">
                                    PREDICTED STATUS
                                </div>

                                <div class="result-main">
                                    LOW CHURN RISK
                                </div>

                                <div class="result-detail">
                                    The model predicts a relatively
                                    lower likelihood of customer churn.
                                </div>

                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


            # =================================================
            # PROBABILITY
            # =================================================

            with probability_col:

                st.markdown(
                    """
                    <div class="churn-result-card probability-card">

                        <div class="mini-label">
                            CHURN PROBABILITY
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.metric(
                    "Probability",
                    f"{probability * 100:.2f}%"
                )

                st.progress(
                    probability
                )


            # =================================================
            # INTERPRETATION
            # =================================================

            if probability >= 0.70:

                risk_text = (
                    "High predicted churn probability. "
                    "This customer falls within the higher-risk range."
                )

            elif probability >= 0.40:

                risk_text = (
                    "Moderate predicted churn probability. "
                    "This customer falls within an intermediate risk range."
                )

            else:

                risk_text = (
                    "Low predicted churn probability. "
                    "This customer falls within a lower-risk range."
                )


            st.markdown(
                f"""
                <div class="glass-card risk-summary">

                    <div class="mini-label">
                        MODEL INTERPRETATION
                    </div>

                    <div class="risk-text">
                        {risk_text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # INPUT SUMMARY
            # =================================================

            with st.expander(
                "⌄  View Prediction Inputs"
            ):

                display_data = pd.DataFrame({

                    "Feature": [

                        "Total Orders",
                        "Total Spending",
                        "Average Order Value",
                        "Days Since Last Order",
                        "Return Rate",
                        "Average Delivery Days",
                        "Age",
                        "Membership Type"

                    ],

                    "Value": [

                        total_orders_input,
                        f"{total_spending_input:,.2f}",
                        f"{average_order_value_input:,.2f}",
                        days_since_last_order_input,
                        f"{return_rate_input:.2f}",
                        f"{average_delivery_days_input:.1f}",
                        age_input,
                        membership_input

                    ]

                })

                st.dataframe(
                    display_data,
                    use_container_width=True,
                    hide_index=True
                )


            st.caption(
                "Prediction generated using the trained churn neural network."
            )


        except Exception as e:

            st.error(
                "Prediction failed. "
                "Please verify that the saved churn model "
                "is compatible with the 10-feature input format."
            )
# =========================================================
    # =====================================================
    # HERO
    # =====================================================

    st.markdown(
        '<div class="hero-title">'
        'Customer <span class="hero-gradient">Churn AI</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Predict customer churn probability using behavioral and demographic features.'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # LOAD CHURN MODEL
    # =====================================================

    model_path = "models/churn.pkl"

    if not os.path.exists(model_path):

        st.error(
            "Churn model not found. "
            "Please make sure churn.pkl exists inside the models folder."
        )

        st.stop()


    try:

        loaded_model = joblib.load(model_path)

        # Direct model
        if hasattr(loaded_model, "predict"):

            churn_model = loaded_model

        # Dictionary containing model
        elif isinstance(loaded_model, dict):

            churn_model = None

            possible_keys = [
                "model",
                "classifier",
                "churn_model",
                "best_model",
                "pipeline",
                "clf",
                "estimator",
                "nn_model"
            ]

            for key in possible_keys:

                if key in loaded_model:

                    candidate = loaded_model[key]

                    if hasattr(candidate, "predict"):

                        churn_model = candidate
                        break


            if churn_model is None:

                for value in loaded_model.values():

                    if hasattr(value, "predict"):

                        churn_model = value
                        break


            if churn_model is None:

                st.error(
                    "No valid prediction model was found inside churn.pkl."
                )

                st.stop()

        else:

            st.error(
                "Invalid churn.pkl model format."
            )

            st.stop()


    except Exception as e:

        st.error(
            f"Unable to load churn.pkl: {e}"
        )

        st.stop()


    # =====================================================
    # INPUT CARD
    # =====================================================

    st.markdown(
        '<div class="glass-card">',
        unsafe_allow_html=True
    )

    st.caption(
        "Enter historical customer behavior to generate a churn prediction."
    )


    col1, col2, col3 = st.columns(3)


    # =====================================================
    # COLUMN 1
    # =====================================================

    with col1:

        total_orders_input = st.number_input(
            "Total Orders",
            min_value=1,
            value=5,
            step=1
        )


        total_spending_input = st.number_input(
            "Total Spending",
            min_value=0.0,
            value=500.0,
            step=10.0
        )


        average_order_value_input = st.number_input(
            "Average Order Value",
            min_value=0.0,
            value=100.0,
            step=10.0
        )


    # =====================================================
    # COLUMN 2
    # =====================================================

    with col2:

        days_since_last_order_input = st.number_input(
            "Days Since Last Order",
            min_value=0,
            value=30,
            step=1
        )


        return_rate_input = st.number_input(
            "Return Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01
        )


        average_delivery_days_input = st.number_input(
            "Average Delivery Days",
            min_value=0.0,
            value=5.0,
            step=0.5
        )


    # =====================================================
    # COLUMN 3
    # =====================================================

    with col3:

        age_input = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1
        )


        membership_input = st.selectbox(
            "Membership Type",
            [
                "Basic",
                "Premium",
                "Standard"
            ]
        )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # =====================================================
    # PREDICT BUTTON
    # =====================================================

    predict = st.button(
        "◈  RUN CHURN PREDICTION",
        use_container_width=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # =====================================================
    # PREDICTION
    # =====================================================

    if predict:

        try:

            # =================================================
            # ONE-HOT ENCODE MEMBERSHIP
            # =================================================

            membership_basic = (
                1 if membership_input == "Basic" else 0
            )

            membership_premium = (
                1 if membership_input == "Premium" else 0
            )

            membership_standard = (
                1 if membership_input == "Standard" else 0
            )


            # =================================================
            # CREATE EXACTLY 10 FEATURES
            # =================================================

            input_data = np.array([

                [
                    total_orders_input,
                    total_spending_input,
                    average_order_value_input,
                    days_since_last_order_input,
                    return_rate_input,
                    average_delivery_days_input,
                    age_input,

                    membership_basic,
                    membership_premium,
                    membership_standard
                ]

            ], dtype=np.float32)


            # =================================================
            # CHECK MODEL INPUT SIZE
            # =================================================

            expected_features = None

            try:

                expected_features = int(
                    churn_model.input_shape[-1]
                )

            except Exception:

                pass


            if (
                expected_features is not None
                and expected_features != input_data.shape[1]
            ):

                st.error(
                    f"Model expects {expected_features} features, "
                    f"but the application generated "
                    f"{input_data.shape[1]} features."
                )

                st.stop()


            # =================================================
            # MODEL PREDICTION
            # =================================================

            prediction_raw = churn_model.predict(
                input_data,
                verbose=0
            )


            prediction_array = np.asarray(
                prediction_raw
            )


            # =================================================
            # GET PROBABILITY
            # =================================================

            if prediction_array.ndim == 2:

                probability = float(
                    prediction_array[0][0]
                )

            else:

                probability = float(
                    prediction_array[0]
                )


            # =================================================
            # KEEP PROBABILITY BETWEEN 0 AND 1
            # =================================================

            probability = max(
                0.0,
                min(
                    1.0,
                    probability
                )
            )


            # =================================================
            # CHURN CLASS
            # =================================================

            prediction = (
                1
                if probability >= 0.50
                else 0
            )


            # =================================================
            # RESULT TITLE
            # =================================================

            st.markdown(
                '<div class="section-title">'
                'Prediction Result'
                '</div>',
                unsafe_allow_html=True
            )


            result_col, probability_col = st.columns(
                [1, 1]
            )


            # =================================================
            # RESULT
            # =================================================

            with result_col:

                if prediction == 1:

                    st.error(
                        "⚠️ HIGH RISK — Customer predicted to churn"
                    )

                else:

                    st.success(
                        "✓ LOW RISK — Customer predicted to remain active"
                    )


            # =================================================
            # PROBABILITY
            # =================================================

            with probability_col:

                st.metric(
                    "Churn Probability",
                    f"{probability * 100:.2f}%"
                )


                st.progress(
                    probability
                )


            # =================================================
            # RISK INTERPRETATION
            # =================================================

            if probability >= 0.70:

                st.warning(
                    "This customer shows a high predicted "
                    "churn probability."
                )

            elif probability >= 0.40:

                st.info(
                    "This customer falls within a moderate "
                    "predicted churn-probability range."
                )

            else:

                st.success(
                    "This customer shows a relatively low "
                    "predicted churn probability."
                )


            # =================================================
            # INPUT SUMMARY
            # =================================================

            with st.expander(
                "View Prediction Inputs"
            ):

                display_data = pd.DataFrame({

                    "Feature": [

                        "Total Orders",
                        "Total Spending",
                        "Average Order Value",
                        "Days Since Last Order",
                        "Return Rate",
                        "Average Delivery Days",
                        "Age",
                        "Membership Type"

                    ],

                    "Value": [

                        total_orders_input,
                        f"{total_spending_input:,.2f}",
                        f"{average_order_value_input:,.2f}",
                        days_since_last_order_input,
                        f"{return_rate_input:.2f}",
                        f"{average_delivery_days_input:.1f}",
                        age_input,
                        membership_input

                    ]

                })


                st.dataframe(
                    display_data,
                    use_container_width=True,
                    hide_index=True
                )


            st.caption(
                "Prediction generated using the trained churn neural network."
            )


        except Exception as e:

            st.error(
                f"Prediction failed: {e}"
            )


# PAGE 3 — SENTIMENT
# =========================================================

elif page == "💬  Sentiment Analysis":

    st.markdown(
        '<div class="hero-title">'
        'Review <span class="hero-gradient">Sentiment AI</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Analyze customer feedback using your trained NLP classification model.'
        '</div>',
        unsafe_allow_html=True
    )

    # =========================================================
    # SENTIMENT MODEL PATH
    # =========================================================

    sentiment_model_path = "models/sentiment_model.pkl"

    if not os.path.exists(sentiment_model_path):

        st.warning(
            "Sentiment model not found. "
            "Save your trained NLP model as "
            "models/sentiment_model.pkl"
        )

    else:

        try:

            # =================================================
            # LOAD MODEL
            # =================================================

            sentiment_bundle = joblib.load(
                sentiment_model_path
            )

            sentiment_model = None
            sentiment_vectorizer = None

            # =================================================
            # IF SAVED FILE IS A DICTIONARY
            # =================================================

            if isinstance(sentiment_bundle, dict):

                # ---------------------------------------------
                # FIND VECTORIZER
                # ---------------------------------------------

                possible_vectorizer_keys = [
                    "vectorizer",
                    "tfidf",
                    "tfidf_vectorizer",
                    "text_vectorizer",
                    "vectorizer_model"
                ]

                for key in possible_vectorizer_keys:

                    if key in sentiment_bundle:

                        possible_vectorizer = (
                            sentiment_bundle[key]
                        )

                        if hasattr(
                            possible_vectorizer,
                            "transform"
                        ):

                            sentiment_vectorizer = (
                                possible_vectorizer
                            )

                            break

                # ---------------------------------------------
                # FIND MODEL
                # ---------------------------------------------

                possible_model_keys = [
                    "model",
                    "sentiment_model",
                    "classifier",
                    "clf",
                    "pipeline"
                ]

                for key in possible_model_keys:

                    if key in sentiment_bundle:

                        possible_model = (
                            sentiment_bundle[key]
                        )

                        if hasattr(
                            possible_model,
                            "predict"
                        ):

                            sentiment_model = (
                                possible_model
                            )

                            break

            # =================================================
            # IF SAVED FILE ITSELF IS A MODEL
            # =================================================

            else:

                if hasattr(
                    sentiment_bundle,
                    "predict"
                ):

                    sentiment_model = (
                        sentiment_bundle
                    )

            # =================================================
            # CHECK MODEL
            # =================================================

            if sentiment_model is None:

                st.error(
                    "❌ Sentiment model was loaded, "
                    "but a prediction model could not be found."
                )

                if isinstance(
                    sentiment_bundle,
                    dict
                ):

                    st.warning(
                        "Available model keys:"
                    )

                    st.code(
                        "\n".join(
                            sentiment_bundle.keys()
                        )
                    )

                st.stop()

            # =================================================
            # CUSTOMER REVIEW CARD
            # =================================================

            st.markdown(
                '<div class="glass-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                "### Customer Review"
            )

            st.caption(
                "Paste or type a customer review below."
            )

            review_text = st.text_area(
                "Review",
                height=190,
                placeholder=(
                    "Example: The product quality was excellent "
                    "and delivery was very fast."
                ),
                label_visibility="collapsed"
            )

            analyze = st.button(
                "◈  ANALYZE SENTIMENT",
                use_container_width=True
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

            # =================================================
            # ANALYZE REVIEW
            # =================================================

            if analyze:

                if review_text.strip() == "":

                    st.warning(
                        "Please enter a customer review first."
                    )

                else:

                    try:

                        # =========================================
                        # CASE 1:
                        # MODEL + VECTORIZER
                        # =========================================

                        if sentiment_vectorizer is not None:

                            transformed_review = (
                                sentiment_vectorizer.transform(
                                    [review_text]
                                )
                            )

                            prediction = (
                                sentiment_model.predict(
                                    transformed_review
                                )[0]
                            )

                        # =========================================
                        # CASE 2:
                        # COMPLETE PIPELINE
                        # =========================================

                        else:

                            prediction = (
                                sentiment_model.predict(
                                    [review_text]
                                )[0]
                            )

                        # =========================================
                        # CLEAN PREDICTION
                        # =========================================

                        prediction_text = str(
                            prediction
                        ).strip()

                        prediction_lower = (
                            prediction_text.lower()
                        )

                        # =========================================
                        # RESULT TITLE
                        # =========================================

                        st.markdown(
                            '<div class="section-title">'
                            'Analysis Result'
                            '</div>',
                            unsafe_allow_html=True
                        )

                        # =========================================
                        # POSITIVE
                        # =========================================

                        if prediction_lower in [
                            "positive",
                            "pos"
                        ]:

                            st.success(
                                "😊  POSITIVE — "
                                "The review expresses positive sentiment."
                            )

                            display_sentiment = "Positive"

                        # =========================================
                        # NEGATIVE
                        # =========================================

                        elif prediction_lower in [
                            "negative",
                            "neg"
                        ]:

                            st.error(
                                "☹️  NEGATIVE — "
                                "The review expresses negative sentiment."
                            )

                            display_sentiment = "Negative"

                        # =========================================
                        # NEUTRAL
                        # =========================================

                        elif prediction_lower == "neutral":

                            st.info(
                                "😐  NEUTRAL — "
                                "The review expresses neutral sentiment."
                            )

                            display_sentiment = "Neutral"

                        # =========================================
                        # NUMERIC LABELS
                        # =========================================

                        elif prediction_text == "1":

                            st.success(
                                "😊  POSITIVE — "
                                "The review expresses positive sentiment."
                            )

                            display_sentiment = "Positive"

                        elif prediction_text == "0":

                            st.error(
                                "☹️  NEGATIVE — "
                                "The review expresses negative sentiment."
                            )

                            display_sentiment = "Negative"

                        # =========================================
                        # OTHER LABEL
                        # =========================================

                        else:

                            st.info(
                                f"😐  {prediction_text.upper()} — "
                                "The review has been classified "
                                "by the NLP model."
                            )

                            display_sentiment = (
                                prediction_text.title()
                            )

                        # =========================================
                        # RESULT CARD
                        # =========================================

                        st.markdown(
                            f"""
                           
                            """,
                            unsafe_allow_html=True
                        )

                    except Exception as prediction_error:

                        st.error(
                            "❌ Sentiment prediction failed."
                        )

                        st.code(
                            str(prediction_error)
                        )

        except Exception as model_error:

            st.error(
                "❌ Sentiment model could not be loaded."
            )

            st.code(
                str(model_error)
            )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <br><br>
    <div style="
        text-align:center;
        color:#53657a;
        font-size:11px;
        padding:20px;
        border-top:1px solid rgba(255,255,255,0.05);
    ">
        NEXORA CUSTOMER INTELLIGENCE • DATA SCIENCE HACKATHON
    </div>
    """,
    unsafe_allow_html=True
)