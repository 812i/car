import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="محاكاة القيادة باليد المتقدمة", page_icon="🚗", layout="centered")

st.title("🚗 محاكاة نظام القيادة اليدوية (Drive-by-Wire)")
st.write("استخدمي المُنزلقات (Sliders) بالأسفل للتحكم في السيارة كأنك تمسكين المقود بيدك.")

# تهيئة المتغيرات في حالة الجلسة (Session State)
if 'speed' not in st.session_state:
    st.session_state.speed = 0.0
if 'steering_angle' not in st.session_state:
    st.session_state.steering_angle = 0  # من -100 (يسار) إلى +100 (يمين)
if 'throttle_input' not in st.session_state:
    st.session_state.throttle_input = 0 # قيمة منزلق البنزين
if 'brake_input' not in st.session_state:
    st.session_state.brake_input = 0 # قيمة منزلق الفرامل

# --- لوحة العدادات ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    # تحويل قيمة زاوية الدركسون لعرضها كنص
    steer_display = "مستقيم ⬆️"
    if st.session_state.steering_angle < 0:
        steer_display = f"⬅️ يسار ({abs(st.session_state.steering_angle)})"
    elif st.session_state.steering_angle > 0:
        steer_display = f"➡️ يمين ({st.session_state.steering_angle})"
    st.metric(label="وضعية الدركسون", value=steer_display)

with col2:
    st.metric(label="السرعة الحالية", value=f"{st.session_state.speed:.1f} كم/س")

with col3:
    # تحديد الحالة بناءً على المدخلات
    car_status = "متوقفة 🛑"
    if st.session_state.throttle_input > 0:
        car_status = "تتسارع 🚀"
    elif st.session_state.brake_input > 0:
        car_status = "فرملة ⚠️"
    elif st.session_state.speed > 0:
        car_status = "تسير 🛣️"
    st.metric(label="حالة السيارة", value=car_status)

# مؤشرات بصرية لقوة الضغط
st.write("مستوى مسرع اليد:")
st.progress(min(st.session_state.throttle_input * 10, 100)) # ضرب في 10 للتناسب

st.write("مستوى فرامل اليد:")
st.progress(min(st.session_state.brake_input * 10, 100))

st.markdown("---")

# --- لوحة التحكم اليدوية (باستخدام المُنزلقات - Sliders) ---
st.subheader("🎮 لوحة التحكم التفاعلية")
st.write("اسحبي المؤشرات بيدك (بالماوس أو اللمس):")

# 1. تحكم التوجيه (الدركسون) - مُنزلق أفقي
# label: الاسم الظاهر
# min_value: أقصى يسار (-100)
# max_value: أقصى يمين (+100)
# value: القيمة الافتراضية الحالية
# step: مقدار القفزة عند التحريك (5 درجات)
st.session_state.steering_angle = st.slider(
    "↩️ تحكم الدركسون (يسار/يمين)",
    min_value=-100,
    max_value=100,
    value=st.session_state.steering_angle,
    step=5
)

st.write("") # مسافة فارغة

# 2. تحكم التسارع (مسرع اليد) - مُنزلق عمودي (اختياري vertical=True ليعطي إحساس المقبض)
# ملاحظة: المُنزلقات العمودية في Streamlit تتطلب نسخة حديثة، إذا لم تعمل، احذفي argument: vertical=True
st.session_state.throttle_input = st.slider(
    "🚀 مسرع اليد (Throttle)",
    min_value=0,
    max_value=10,
    value=st.session_state.throttle_input,
    step=1,
    #help="اسحبي للأعلى لزيادة السرعة",
    #vertical=True # قد يحتاج Streamlit حديث
)

# 3. تحكم الفرامل (فرامل اليد) - مُنزلق عمودي
st.session_state.brake_input = st.slider(
    "🛑 فرملة اليد (Brake)",
    min_value=0,
    max_value=10,
    value=st.session_state.brake_input,
    step=1,
    #vertical=True
)

# --- منطق حساب الحركة (Physics Logic) ---
# يتم تحديث القيم بناءً على مكان المُنزلقات عند عمل rerun

# أولوية الأمان: إذا تم الضغط على الفرامل، يلغى البنزين
if st.session_state.brake_input > 0:
    # فرملة قوية
    speed_change = - (st.session_state.brake_input * 6.0)
    st.session_state.throttle_input = 0 # إيقاف البنزين تلقائياً
else:
    # تسارع عادي بناءً على قيمة المسرع
    speed_change = st.session_state.throttle_input * 2.5

# التحديث النهائي للسرعة مع حدود (0 إلى 180)
st.session_state.speed = max(0.0, min(180.0, st.session_state.speed + speed_change))

# التباطؤ الطبيعي البسيط إذا لم يتم الضغط على شيء
if st.session_state.throttle_input == 0 and st.session_state.brake_input == 0:
    st.session_state.speed = max(0.0, st.session_state.speed - 1.0)


# زر لتحديث المحاكاة (اختياري مع وجود السلايدرات، لكن مفيد لضمان التحديث)
st.write("")
if st.button("تحديث الحركة الآن", use_container_width=True):
    st.rerun()
