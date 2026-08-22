import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="محاكاة دركسون القيادة اليدوية", page_icon="🚗", layout="centered")

st.title("🚗 محاكاة نظام القيادة باليد (Drive-by-Wire)")
st.write("تصميم تفاعلي مستوحى من شكل المقود والأذرع الداخلية للتحكم الكامل.")

# تهيئة متغيرات الحالة
if 'speed' not in st.session_state:
    st.session_state.speed = 0.0
if 'steering_angle' not in st.session_state:
    st.session_state.steering_angle = 0  # زاوية التوجيه
if 'throttle' not in st.session_state:
    st.session_state.throttle = 0
if 'brake' not in st.session_state:
    st.session_state.brake = 0

# --- لوحة العدادات العلوية ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="السرعة", value=f"{st.session_state.speed:.1f} كم/س")

with col2:
    st.metric(label="زاوية المقود", value=f"{st.session_state.steering_angle}°")

with col3:
    status = "متوقفة 🛑"
    if st.session_state.throttle > 0:
        status = "تتسارع 🚀"
    elif st.session_state.brake > 0:
        status = "فرملة ⚠️"
    st.metric(label="الحالة", value=status)

st.markdown("---")

# --- تمثيل الدركسون البصري التفاعلي (مستوحى من الرسمة) ---
st.subheader("🎮 المقود التفاعلي (Steering Wheel)")

# استخدام مكون HTML/SVG لرسم الدركسون بشكل مطابق لرسمتك (دائرة خارجية وأذرع متصلة بالمنتصف)
steering_svg = f"""
<div style="display: flex; justify-content: center; align-items: center; margin: 20px 0;">
    <svg width="220" height="220" viewBox="0 0 200 200" style="transform: rotate({st.session_state.steering_angle}deg); transition: transform 0.1s ease;">
        <!-- الإطار الخارجي للدركسون -->
        <circle cx="100" cy="100" r="85" fill="none" stroke="#2c3e50" stroke-width="16" />
        <circle cx="100" cy="100" r="73" fill="none" stroke="#34495e" stroke-width="2" stroke-dasharray="4,4" />
        
        <!-- الأذرع الداخلية الثلاثة (مطابقة لرسمتك) -->
        <!-- الذراع الأيسر العلوي -->
        <line x1="100" y1="100" x2="35" y2="70" stroke="#2c3e50" stroke-width="12" stroke-linecap="round" />
        <!-- الذراع الأيمن العلوي -->
        <line x1="100" y1="100" x2="165" y2="70" stroke="#2c3e50" stroke-width="12" stroke-linecap="round" />
        <!-- الذراع السفلي -->
        <line x1="100" y1="100" x2="100" y2="165" stroke="#2c3e50" stroke-width="12" stroke-linecap="round" />
        
        <!-- الدائرة المركزية (المنصفة) -->
        <circle cx="100" cy="100" r="28" fill="#1abc9c" stroke="#16a085" stroke-width="4" />
        <text x="100" y="105" font-size="12" fill="white" font-weight="bold" text-anchor="middle" dominant-baseline="middle">AI</text>
    </svg>
</div>
"""
st.markdown(steering_svg, unsafe_allow_html=True)

# --- أدوات التحكم (المنزلقات للدركسون والبنزين والفرامل) ---
st.write("### لوحة تحكم المقبض والدواسات الافتراضية:")

# تحكم الدركسون (تدوير يمين ويسار)
st.session_state.steering_angle = st.slider(
    "🔄 تدوير المقود (يسار / يمين)",
    min_value=-90,
    max_value=90,
    value=st.session_state.steering_angle,
    step=10
)

col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    st.session_state.throttle = st.slider(
        "🚀 ضغط مسرع اليد",
        min_value=0,
        max_value=100,
        value=st.session_state.throttle,
        step=10
    )

with col_ctrl2:
    st.session_state.brake = st.slider(
        "🛑 ضغط فرملة اليد",
        min_value=0,
        max_value=100,
        value=st.session_state.brake,
        step=10
    )

# --- منطق حساب السرعة والحركة ---
if st.session_state.brake > 0:
    # الفرملة تلغي البنزين وتبطئ السيارة بسرعة
    st.session_state.throttle = 0
    speed_delta = - (st.session_state.brake * 0.4)
else:
    speed_delta = st.session_state.throttle * 0.15

# تحديث السرعة النهائية
st.session_state.speed = max(0.0, min(160.0, st.session_state.speed + speed_delta))

# تباطؤ طبيعي إذا تم ترك الأزرار
if st.session_state.throttle == 0 and st.session_state.brake == 0:
    st.session_state.speed = max(0.0, st.session_state.speed - 1.5)

# زر لتحديث الشاشة يدوي عند الحاجة
st.write("")
if st.button("تحديث حالة المحاكاة", use_container_width=True):
    st.rerun()
