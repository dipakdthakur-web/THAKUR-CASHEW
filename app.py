import streamlit as st
import streamlit as st
import pandas as pd

# १. पेजाची रचना (Page Configuration)
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
st.sidebar.title("🗂️ बिझनेस मेमरी")
st.sidebar.write("---")
st.sidebar.subheader("📋 सर्व १७ लाईव्ह रिपोर्ट्स")

# तुम्ही दिलेली १७ शीट्सची अचूक नावे (डावीकडे ॲपमधील नाव : उजवीकडे गुगल शीटमधील अचूक नाव)
sheet_options = {
    "1️⃣ RCN Purchase Details": "RCN Purchase Details",
    "2️⃣ Finish Goods Purchase": "Finish Goods Purchase",
    "3️⃣ Processing Quantity": "Processing Quantity",
    "4️⃣ Boiling Report": "Boiling",
    "5️⃣ Cutting Report": "Cutting Report",
    "6️⃣ Outward Sale": "Outward Sale",
    "7️⃣ Borma Report": "Borma Report",
    "8️⃣ Before After Borma Report": "Before After Borma Report",
    "9️⃣ Inward Job Work": "Inward Job Work",
    "🔟 Moisture Report": "Moisture Report",
    "1️⃣1️⃣ Everest To Indian Report": "Average To Indian Report",
    "1️⃣2️⃣ Kudal To Math Report": "Kudal To Mud Report",
    "1️⃣3️⃣ Old Lot Stock": "Old Lot Stock",
    "1️⃣4️⃣ Final Bucket Stock List": "Final Bucket Stock List",
    "1️⃣5️⃣ P&L Profit And Loss": "P&L Profit And Loss",
    "1️⃣6️⃣ Account Sales": "Account Sales",
    "1️⃣7️⃣ Cash Sales": "Cash Sales"
}

# सिलेक्ट बॉक्स ऐवजी सुंदर रेडिओ बटन्स जेणेकरून स्क्रोल करून पाहणे सोपे जाईल
selected_display_name = st.sidebar.radio("पाहण्यासाठी रिपोर्ट निवडा:", list(sheet_options.keys()))
st.sidebar.write("---")
st.sidebar.caption("💡 टीप: गुगल शीटमध्ये बदल केल्यास येथे दर ६० सेकंदांनी डेटा ऑटो-रिफ्रेश होईल.")

# ३. मुख्य स्क्रीन (Main Dashboard Context)
st.title("🏭 ठाकूर काश्यूज (Thakur Cashews)")
st.subheader("AI Business Legacy & Decision Support System")
st.write(f"📂 **चालू अहवाल:** `{selected_display_name}`")
st.write("---")

# ४. डेटा लोड करण्याचे फंक्शन (Cache ६० सेकंद ठेवला आहे जेणेकरून सिस्टीम फास्ट चालेल)
@st.cache_data(ttl=60)
def load_live_data(sheet_name):
    try:
        # गुगल शीटच्या विशिष्ट टॅबची लिंक तयार करणे
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        # रिकाम्या ओळी किंवा कॉलम्स काढून टाकणे
        df = df.dropna(how='all')
        return df
    except Exception as e:
        return None

# निवडलेल्या रिपोर्टचा डेटा मिळवणे
actual_sheet_name = sheet_options[selected_display_name]
with st.spinner("गुगल शीटमधून लाईव्ह डेटा आणत आहे... कृपया थांबा..."):
    df_data = load_live_data(actual_sheet_name)

# ५. डेटा स्क्रीनवर दाखवणे आणि फॅमिलीसाठी सोपे बिझनेस इन्साइट्स
if df_data is not None and not df_data.empty:
    st.success(f"📊 `{actual_sheet_name}` चा डेटा यशस्वीरित्या लोड झाला आहे.")
    
    # डेटा टेबल इंटरॅक्टिव्ह फॉरमॅटमध्ये दाखवणे (शोधणे आणि फिल्टर करणे सोपे जाईल)
    st.dataframe(df_data, use_container_width=True, hide_index=True)
    
    # फॅमिली हेडसाठी सोपे मार्गदर्शन आणि बिझनेस सेफ्टी नोट
    st.write("---")
    st.markdown("### 🔑 निर्णय आणि जोखीम व्यवस्थापन (Decision Support Note)")
    
    # प्रत्येक शीटच्या स्वरूपानुसार डायनॅमिक सल्ला
    if "Purchase" in actual_sheet_name or "Procurement" in actual_sheet_name:
        st.info("💡 **खरेदी विश्लेषण:** कच्च्या मालाच्या (RCN) खरेदी किमती आणि स्टॉकची उपलब्धता तपासूनच पुढील लॉटचे पेमेंट प्लॅनिंग करावे. वर्किंग कॅपिटल सुरक्षित ठेवण्याला प्राधान्य द्यावे.")
    elif "Stock" in actual_sheet_name:
        st.warning("⚠️ **स्टॉक अलर्ट:** जुन्या लॉटचा स्टॉक (Old Lot Stock) किंवा फायनल बकेट स्टॉक आधी रिकामा करण्यावर भर द्यावा, जेणेकरून कॅश फ्लो अडकून पडणार नाही.")
    elif "Sale" in actual_sheet_name or "P&L" in actual_sheet_name:
        st.success("💰 **नफा आणि आर्थिक स्थिती:** हा डेटा थेट नफा-तोटा आणि कॅश फ्लोशी संबंधित आहे. येणे बाकी (Receivables) आणि रोख विक्रीचा ताळमेळ तपासूनच पुढील व्यवहार करावेत.")
    else:
        st.info("⚙️ **प्रोसेसिंग आणि गुणवत्ता:** बॉईलिंग, कटिंग, मॉइश्चर आणि बोर्मा रिपोर्टमधील रिकव्हरी टक्केवारीवर बारीक लक्ष ठेवावे. इथली कार्यक्षमता थेट कारखान्याचा नफा ठरवते.")

else:
    # जर नाव मॅच झाले नाही किंवा शीट रिकामी असेल तर हा स्पष्ट मेसेज दिसेल
    st.error(f"❌ '{actual_sheet_name}' नावाचा टॅब गुगल शीटमध्ये सापडला नाही किंवा तो सध्या रिकामा आहे.")
    st.markdown(
        f"""
        **पुढील गोष्टी तपासा:**
        1. तुमच्या गुगल शीटमध्ये खाली असलेल्या टॅबचे नाव अचूक **`{actual_sheet_name}`** असेच आहे का? (स्पेस आणि कॅपिटल अक्षरे तपासा).
        2. जर शीटचे नाव वेगळे असेल, तर गुगल शीटमध्ये जाऊन टॅबचे नाव बदलून नेमके `{actual_sheet_name}` करा आणि हे पेज रिफ्रेश करा.
        """
    )
