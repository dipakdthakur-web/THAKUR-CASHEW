import streamlit as st
import pandas as pd

# १. पेजाची रचना
st.set_page_config(
    page_title="ठाकूर काश्यूज डॅशबोर्ड", 
    page_icon="🏭", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# गुगल शीटचा आयडी
SHEET_ID = "1c_Hf3pBf27iZbJ4cFvwPCny2Tvt6jryKqL0pSpP-9q0"

# २. डाव्या बाजूचा नेव्हिगेशन मेनू (Sidebar)
st.sidebar.image("https://img.icons8.com/fluent/96/000000/factory.png", width=70)
st.sidebar.title("🗂️ बिझネス मेमरी")
st.sidebar.write("---")
st.sidebar.subheader("📋 सर्व १७ लाईव्ह रिपोर्ट्स")

# आपण ठरवलेला क्रम आणि गुगल शीटमधील अनुक्रमांक (0, 1, 2...)
sheet_by_index = {
    "1️⃣ RCN Purchase Details": 0,
    "2️⃣ Finish Goods Purchase": 1,
    "3️⃣ Processing Quantity": 2,
    "4️⃣ Boiling Report": 3,
    "5️⃣ Cutting Report": 4,
    "6️⃣ Outward Sale": 5,
    "7️⃣ Borma Report": 6,
    "8️⃣ Before After Borma Report": 7,
    "9️⃣ Inward Job Work": 8,
    "🔟 Moisture Report": 9,
    "1️⃣1️⃣ Everest To Indian Report": 10,
    "1️⃣2️⃣ Kudal To Math Report": 11,
    "1️⃣3️⃣ Old Lot Stock": 12,
    "1️⃣4️⃣ Final Bucket Stock List": 13,
    "1️⃣5️⃣ P&L Profit And Loss": 14,
    "1️⃣6️⃣ Account Sales": 15,
    "1️⃣7️⃣ Cash Sales": 16
}

selected_report = st.sidebar.radio("पाहण्यासाठी रिपोर्ट निवडा:", list(sheet_by_index.keys()))
st.sidebar.write("---")

# ३. मुख्य स्क्रीन
st.title("🏭 ठाकूर काश्यूज (Thakur Cashews)")
st.subheader("AI Business Legacy & Decision Support System")
st.write(f"📂 **चालू अहवाल:** `{selected_report}`")
st.write("---")

# ४. क्रमांकावरून थेट गुगल शीट लोड करण्याचे फंक्शन
@st.cache_data(ttl=60)
def load_data_by_index(sheet_index):
    try:
        # थेट विशिष्ट शीट नंबरवरून (Gid) डेटा उघडण्याची सर्वात वेगवान लिंक
        direct_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={sheet_index}"
        df = pd.read_csv(direct_url)
        df = df.dropna(how='all')
        return df
    except Exception as e:
        return None

target_index = sheet_by_index[selected_report]

with st.spinner("गुगल शीटमधून नंबरनुसार लाईव्ह डेटा लोड होत आहे..."):
    df_data = load_data_by_index(target_index)

# ५. स्क्रीनवर डेटा आणि फॅमिलीसाठी गाईडलाईन्स दाखवणे
if df_data is not None and not df_data.empty:
    st.success(f"📊 `{selected_report}` चा डेटा यशस्वीरित्या लोड झाला आहे.")
    st.dataframe(df_data, use_container_width=True, hide_index=True)
    
    st.write("---")
    st.markdown("### 🔑 निर्णय आणि जोखीम व्यवस्थापन (Decision Support Note)")
    
    if "Purchase" in selected_report:
        st.info("💡 **खरेदी विश्लेषण:** कच्च्या मालाच्या (RCN) खरेदी किमती आणि स्टॉकची उपलब्धता तपासूनच पुढील लॉटचे पेमेंट प्लॅनिंग करावे.")
    elif "Stock" in selected_report:
        st.warning("⚠️ **स्टॉक अलर्ट:** जुन्या लॉटचा स्टॉक (Old Lot Stock) किंवा फायナル बकेट स्टॉक आधी रिकामा करण्यावर भर द्यावा.")
    elif "Sale" in selected_report or "P&L" in selected_report:
        st.success("💰 **नफा आणि आर्थिक स्थिती:** हा डेटा थेट नफा-तोटा आणि कॅश फ्लोशी संबंधित आहे. येणे बाकी आणि रोख विक्रीचा ताळमेळ तपासावा.")
    else:
        st.info("⚙️ **प्रोसेसिंग आणि गुणवत्ता:** बॉईलिंग, कटिंग, मॉइश्चर आणि बोर्मा रिपोर्टमधील रिकव्हरी टक्केवारीवर बारीक लक्ष ठेवावे.")
else:
    st.error(f"❌ शीट क्रमांक `{target_index + 1}` मधून डेटा लोड होऊ शकला नाही.")
    st.info("💡 **टीप:** गुगल शीट 'Anyone with the link can view' या सेटिंगवर असल्याची खात्री करा.")
