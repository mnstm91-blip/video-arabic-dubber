import os
import asyncio
import edge_tts

print("🎬 ===============================================")
print("     🎬 V-MAX AI Video Dubber (Pydroid 3 Pro)    ")
print("==================================================")

# 1. طلب المدخلات من المستخدم
video_path = input("📥 أدخل اسم أو مسار ملف الفيديو (مثال: video.mp4): ").strip()
arabic_text = input("📝 أدخل النص العربي المراد دبلجته للفيديو: ").strip()
output_path = "output_arabic.mp4"

async def generate_arabic_audio(text, audio_path):
    """توليد صوت ذكاء اصطناعي عربي نقي جداً"""
    print("\n⏳ [1/2] جاري توليد الصوت العربي بالذكاء الاصطناعي...")
    # حامد هو أحد أفضل الأصوات الطبيعية المتاحة من مايكروسوفت
    voice = "ar-SA-HamedNeural" 
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(audio_path)
    print("✅ تم توليد ملف الصوت بنجاح.")

def merge_audio_video(video_in, audio_in, video_out):
    """دمج الصوت الجديد مع الفيديو باستخدام أدوات النظام المدمجة"""
    print("⏳ [2/2] جاري دمج الصوت الجديد مع الفيديو...")
    
    # أمر ffmpeg مدمج وسريع جداً يستبدل الصوت القديم بالجديد دون إعادة رندرة الفيديو
    cmd = f"ffmpeg -y -i {video_in} -i {audio_in} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {video_out}"
    
    exit_code = os.system(cmd)
    return exit_code == 0

# تشغيل الأداة
if not os.path.exists(video_path):
    print(f"❌ خطأ: لم يتم العثور على ملف الفيديو في هذا المسار: '{video_path}'")
else:
    temp_audio = "temp_voice.mp3"
    try:
        # تشغيل دالة توليد الصوت
        asyncio.run(generate_arabic_audio(arabic_text, temp_audio))
        
        # تشغيل عملية الدمج
        success = merge_audio_video(video_path, temp_audio, output_path)
        
        if success:
            print("\n==================================================")
            print(f"🎉 مبروك! تم دبلجة الفيديو بنجاح.")
            print(f"📂 الملف الجاهز باسم: {output_path}")
            print("==================================================")
        else:
            print("\n❌ فشل دمج الصوت مع الفيديو. تأكد من تثبيت حزمة ffmpeg في نظامك أو جرب دمج ملف 'temp_voice.mp3' يدوياً عبر أي تطبيق مونتاج.")
            
    except Exception as e:
        print(f"\n❌ حدث خطأ غير متوقع: {e}")
    finally:
        # تنظيف الملفات المؤقتة
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
