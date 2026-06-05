import os
import whisper
import asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip

print("🎬 === V-MAX AI Video Dubber (Terminal Edition) ===")

# طلب مسار الفيديو من المستخدم
video_path = input("📥 أدخل مسار ملف الفيديو (مثال: video.mp4): ").strip()
output_path = "arabic_output.mp4"

async def process_video(video_path, output_path):
    print("⏳ [1/3] جاري تفريغ الصوت وترجمته باستخدام Whisper...")
    model = whisper.load_model("tiny")
    result = model.transcribe(video_path, task="translate")
    arabic_text = result["text"]
    print("📝 النص المترجم:", arabic_text)

    print("⏳ [2/3] جاري توليد الصوت العربي بالذكاء الاصطناعي...")
    voice = "ar-SA-HamedNeural"
    communicate = edge_tts.Communicate(arabic_text, voice)
    temp_audio = "temp_voice.mp3"
    await communicate.save(temp_audio)

    print("⏳ [3/3] جاري دمج الصوت العربي الجديد مع الفيديو...")
    video = VideoFileClip(video_path)
    arabic_audio = AudioFileClip(temp_audio)
    final_video = video.set_audio(arabic_audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # إغلاق الملفات لتجنب المشاكل
    video.close()
    arabic_audio.close()
    if os.path.exists(temp_audio):
        os.remove(temp_audio)
    print(f"✅ تم دبلجة الفيديو بنجاح! تم حفظه باسم: {output_path}")

# التأكد من أن الملف موجود قبل البدء
if os.path.exists(video_path):
    try:
        asyncio.run(process_video(video_path, output_path))
    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {e}")
else:
    print("❌ خطأ: لم يتم العثور على ملف الفيديو في المسار الذي أدخلته!")
