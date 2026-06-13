import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# १. पेजाची रचना आणि सेटिंग्स
st.set_page_config(
    page_title="ठाकूर कॅश्यू बिझनेस डॅशबोर्ड",
    page_icon="📊",
    layout="wide"
)

# २. गुगल शीटचा आयडी
SHEET_ID = "1c_Hf3pBf27izBj4cFvwPCny2Tvt6jryKqU"

# ३. गुगल शीट कनेक्ट करण्यासाठीचे फंक्शन (सर्व्हिस अकाउंट क्रेडेंशियल्ससह)
@st.cache_resource
def get_gspread_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    # Streamlit Secrets मधून क्रेडेंशियल्स लोड करणे
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    return gspread.authorize(creds)

# ४. डेटा लोड करण्याचे मुख्य फंक्शन (इंडेक्स बदलला की डेटा ऑटोमॅटिक बदलतो)
@st.cache_data(ttl=300)  # ५ मिनिटांनी डेटा ऑटोमॅटिक रिफ्रेश होईल
def load_sheet_data(sheet_index):
    try:
        client = get_gspread_client()
        spreadsheet = client.open_by_key(SHEET_ID)
        worksheet = spreadsheet.get_worksheet(sheet_index)
        
        # सर्व डेटा गोळा करून पांडाज डेटाफ्रेममध्ये रूपांतरित करणे
        data = worksheet.get_all_records()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"डेटा लोड करताना त्रुटी आली: {e}")
        return pd.DataFrame()

# ५. डाव्या बाजूचा नेव्हिगेशन मेनू (Sidebar)
st.sidebar.image("https://img.icons8.com/fluency/96/dashboard.png", width=80)
st.sidebar.title("📁 बिझネス मेमरी")
st.sidebar.write("---")
st.sidebar.subheader("📋 सर्व १७ लाईव्ह रिपोर्ट्स")

# ६. तुमच्या अचूक १७ शीट्सच्या नावांची आणि इंडेक्सची डिक्शनरी (० ते १६)
sheet_by_index = {
    "1. RCN Purchase Details": 0,
    "2. Finish Goods Purchase": 1,
    "3. Processing Quantity": 2,
    "4. Boiling Report": 3,
    "5. Cutting Report": 4,
    "6. Outward Sale": 5,
    "7. Borma Report": 6,
    "8. Before After Borma Report": 7,
    "9. Inward Job Work": 8,
    "10. Moisture Report": 9,
    "11. Everest To Indian Report": 10,
    "12. Kudal To Math Report": 11,
    "13. Old Lot Stock": 12,
    "14. Final Bucket Stock List": 13,
    "15. P&L Profit And Loss": 14,
    "16. Account Sales": 15,
    "17. Cash Sales": 16
}

# ७. युझरला ड्रॉपडाऊन दाखवणे
selected_sheet_name = st.sidebar.selectbox(
    "कृपया रिपोर्ट निवडा:", 
    list(sheet_by_index.keys())
)

# ८. निवडलेल्या रिपोर्टचा इंडेक्स नंबर मिळवणे
selected_index = sheet_by_index[selected_sheet_name]

# ९. मुख्य स्क्रीनवर रिपोर्टचे नाव दाखवणे
st.title(f"📊 {selected_sheet_name}")
st.write(f"खाली तुम्हाला `{selected_sheet_name}` चा लाईव्ह डेटा दिसत आहे.")
st.write("---")

# डेटा लोड करण्यासाठी फंक्शन कॉल करणे
with st.spinner('गुगल शीटवरून लाईव्ह डेटा आणत आहे, कृपया प्रतीक्षा करा...'):
    df = load_sheet_data(selected_index)

# १०. डेटा स्क्रीनवर सुंदर टेबल स्वरूपात दाखवणे
if not df.empty:
    # डेटा सर्च आणि फिल्टर करण्यासाठी आधुनिक डेटा ग्रिड
    st.dataframe(df, use_container_width=True)
    
    # बेसिक आकडेवारी (Metrics)
    st.write("---")
    col1, col2 = st.columns(2)
    col1.metric(label="एकूण नोंदी (Rows)", value=len(df))
    col2.metric(label="एकूण कॉलम्स (Columns)", value=len(df.columns))
else:
    st.info("या शीटमध्ये सध्या कोणताही डेटा उपलब्ध नाही किंवा हे शीट रिकामे आहे.")
