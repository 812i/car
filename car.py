import tkinter as tk
from tkinter import ttk

class CarSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("نموذج محاكاة نظام قيادة يدوي")
        self.root.geometry("500x450")

        self.current_speed = 0.0
        self.max_speed = 200.0
        self.throttle_value = 0.0
        self.brake_value = 0.0
        self.is_running = True

        # --- عناصر الواجهة ---
        
        # عنوان
        lbl_title = ttk.Label(root, text="لوحة تحكم القيادة اليدوية (Drive-by-Wire)", font=("Helvetica", 16, "bold"))
        lbl_title.pack(pady=15)

        # منطقة عرض السرعة (Dashboard)
        dashboard_frame = ttk.LabelFrame(root, text="معلومات السيارة", padding=10)
        dashboard_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_speed = ttk.Label(dashboard_frame, text=f"السرعة الحالية: {self.current_speed:.1f} كم/س", font=("Helvetica", 14))
        self.lbl_speed.pack()

        # منطقة عرض التحكم اليدوي
        controls_frame = ttk.LabelFrame(root, text="أزرار التحكم اليدوي", padding=10)
        controls_frame.pack(fill="x", padx=20, pady=10)

        # مؤشر البنزين
        self.pbar_throttle = ttk.Progressbar(controls_frame, orient="horizontal", mode="determinate", maximum=100)
        self.pbar_throttle.pack(pady=5, fill="x")
        lbl_throttle = ttk.Label(controls_frame, text="مسرع اليد (اضغط A)")
        lbl_throttle.pack()

        # مؤشر الفرامل
        self.pbar_brake = ttk.Progressbar(controls_frame, orient="horizontal", mode="determinate", maximum=100)
        self.pbar_brake.pack(pady=5, fill="x")
        lbl_brake = ttk.Label(controls_frame, text="فرامل اليد (اضغط S)")
        lbl_brake.pack()

        # تعليمات
        ttk.Label(root, text="استخدم الأزرار A (للتسريع) و S (للفرملة) للتحكم بالسرعة.", font=("Helvetica", 10, "italic")).pack(pady=10)

        # --- ربط الأحداث (Event Binding) ---
        # ربط الضغط على الأزرار بالكيبورد
        self.root.bind('<KeyPress-a>', self.press_throttle)
        self.root.bind('<KeyRelease-a>', self.release_throttle)
        self.root.bind('<KeyPress-s>', self.press_brake)
        self.root.bind('<KeyRelease-s>', self.release_brake)

        # بدء حلقة المحاكاة
        self.root.after(100, self.update_simulation) # تحديث كل 100 مللي ثانية

    # --- منطق المحاكاة ---

    def press_throttle(self, event):
        """محاكاة الضغط على مسرع اليد"""
        self.throttle_value = min(self.throttle_value + 10, 100) # زيادة القوة تدريجياً
        self.pbar_throttle['value'] = self.throttle_value
        # منع الفرملة أثناء التسريع (منطق أمان مبدئي)
        if self.brake_value > 0:
            self.brake_value = 0
            self.pbar_brake['value'] = 0

    def release_throttle(self, event):
        """محاكاة رفع اليد عن المسرع"""
        # قد تختلف الاستراتيجية: هل السرعة تثبت أم تبدأ بالتباطؤ؟ سنعتبرها تثبت الآن.
        # self.throttle_value = 0
        # self.pbar_throttle['value'] = 0
        pass # يمكن تطبيق تباطؤ هنا

    def press_brake(self, event):
        """محاكاة الضغط على فرامل اليد"""
        self.brake_value = min(self.brake_value + 20, 100) # فرملة أسرع من التسارع
        self.pbar_brake['value'] = self.brake_value
        # تقليل قوة التسريع عند الفرملة
        if self.throttle_value > 0:
            self.throttle_value = max(0, self.throttle_value - 30)
            self.pbar_throttle['value'] = self.throttle_value

    def release_brake(self, event):
        """محاكاة رفع اليد عن الفرامل"""
        # self.brake_value = 0
        # self.pbar_brake['value'] = 0
        pass # يمكن تطبيق تباطؤ هنا

    def update_simulation(self):
        """الحلقة الرئيسية لتحديث حالة السيارة الافتراضية"""
        if not self.is_running: return

        # منطق حساب سرعة السيارة بناءً على الأوامر اليدوية
        
        # التسارع (زيادة السرعة)
        if self.throttle_value > 0:
            self.current_speed = min(self.current_speed + (self.throttle_value * 0.5), self.max_speed)
        
        # الفرملة (نقصان السرعة)
        if self.brake_value > 0:
            self.current_speed = max(0, self.current_speed - (self.brake_value * 1.5))
            
        # التباطؤ الطبيعي (مثلاً بسبب مقاومة الهواء والاحتكاك عند رفع اليد)
        # إذا لم يكن هناك تسارع أو فرملة، تبطئ السيارة ببطء
        if self.throttle_value == 0 and self.brake_value == 0 and self.current_speed > 0:
            self.current_speed = max(0, self.current_speed - 1.0)

        # تحديث واجهة المستخدم
        self.lbl_speed.config(text=f"السرعة الحالية: {self.current_speed:.1f} كم/س")
        
        # نداء الدالة مرة أخرى بعد 100 مللي ثانية
        self.root.after(100, self.update_simulation)

if __name__ == "__main__":
    root = tk.Tk()
    app = CarSimulator(root)
    root.mainloop()
