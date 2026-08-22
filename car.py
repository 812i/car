import streamlit as st

st.set_page_config(page_title="محاكاة نظام القيادة باليد", page_icon="🚗", layout="centered")

st.title("🚗 محاكاة نظام القيادة باليد (Drive-by-Wire)")
st.write("مشروع استبدال الدواسات التقليدية بأزرار تحكم ومقابض خلف الدركسون مع نظام التوجيه.")

# تهيئة المتغيرات في حالة الجلسة (Session State)
if 'speed' not in st.session_state:
    st.session_state.speed = 0.0
if 'steering_angle' not in st.session_state:
    st.session_state.steering_angle = 0  # من -45 (يسار) إلى +45 (يمين)
if 'throttle' not in st.session_state:
    st.session_state.throttle = 0
if 'brake' not in st.session_state:
    st.session_state.brake = 0

# --- لوحة العدادات والمعلومات ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="السرعة الحالية", value=f"{st.session_state.speed:.1f} كم/س")

with col2:
    # اتجاه الدركسون
    steer_text = "مستقيم ⬆️"
    if st.session_state.steering_angle < 0:
        steer_text = f"يسار ⬅️ ({abs(st.session_state.steering_angle)}°)"
    elif st.session_state.steering_angle > 0:
        steer_text = f"يمين ➡️ ({st.session_state.steering_angle}°)"
    st.metric(label="وضع الدركسون", value=steer_text)

with col3:
    status = "متوقفة 🛑"
    if st.session_state.speed > 0 and st.session_state.brake == 0:
        status = "تتسارع 🚀"
    elif st.session_state.brake > 0:
        status = "فرملة ⚠️"
    st.metric(label="حالة السيارة", value=status)

# مؤشرات بصرية لمستوى الضغط
st.write("مستوى مسرع اليد (Throttle):")
st.progress(st.session_state.throttle)

st.write("مستوى فرامل اليد (Brake):")
st.progress(st.session_state.brake)

st.markdown("---")

# --- لوحة التحكم باليد (أزرار تفاعلية) ---
st.subheader("🎮 لوحة التحكم (الدركسون والأزرار)")

# تحكم الدركسون (يمين ويسار)
st.text("توجيه الدركسون:")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    if st.button("⬅️ لفة يسار", use_container_width=True):
        st.session_state.steering_angle = max(st.session_state.steering_angle - 15, -45)
        st.rerun()
with col_s2:
    if st.button("⬆️ تعديل الدركسون", use_container_width=True):
        st.session_state.steering_angle = 0
        st.rerun()
with col_s3:
    if st.button("➡️ لفة يمين", use_container_width=True):
        st.session_state.steering_angle = min(st.session_state.steering_angle + 15, 45)
        st.rerun()

st.write("")

# تحكم التسارع والفرامل
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("🚀 ضغط مسرع اليد (+)", use_container_width=True):
        st.session_state.throttle = min(st.session_state.throttle + 25, 100)
        st.session_state.brake = 0
        st.session_state.speed = min(st.session_state.speed + 15.0, 180.0)
        st.rerun()

with col_btn2:
    if st.button("🛑 فرملة اليد طارئة", use_container_width=True):
        st.session_state.brake = 100
        st.session_state.throttle = 0
        st.session_state.speed = max(0.0, st.session_state.speed - 50.0)
        st.rerun()

with col_btn3:
    if st.button("🔄 تحرير الأزرار", use_container_width=True):
        st.session_state.throttle = 0
        st.session_state.brake = 0
        st.rerun()

# التباطؤ الطبيعي عند عدم الضغط
if st.session_state.throttle == 0 and st.session_state.brake == 0 and st.session_state.speed > 0:
    st.session_state.speed = max(0.0, st.session_state.speed - 3.0)
