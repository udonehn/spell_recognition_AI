import speech_recognition as sr
import spell


def onsei():
    # 音声認識器のインスタンスを作成
    recognizer = sr.Recognizer()

    # 音声をキャプチャするためのマイクを使う
    with sr.Microphone() as source:
        print("音声を話してください...")
        # ノイズを調整
        recognizer.adjust_for_ambient_noise(source)
        # 音声を聞く
        audio = recognizer.listen(source)

        print("認識中...")
        try:
            # Google Web Speech APIを使って音声を文字起こし
            text = recognizer.recognize_google(audio, language='ja-JP')
            print(text)
            get_score = spell.get_score(text)
            print("result: " + get_score)
        except sr.UnknownValueError:
            print("音声を理解できませんでした")
        except sr.RequestError as e:
            print(f"音声認識サービスに接続できませんでした: {e}")
            #test
        
        return get_score