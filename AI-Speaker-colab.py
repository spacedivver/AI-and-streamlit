from IPython.display import Audio, display, Javascript
from gtts import gTTS
from IPython.display import display, Javascript
from base64 import b64decode
from io import BytesIO
from pydub import AudioSegment
import google.colab.output as output
from translate import Translator

def speak(text):
  print(f'[AI 스피커]: {text}')
  file_name = 'voice.mp3'
  tts = gTTS(text=text, lang='ko')
  tts.save(file_name)
  display(Audio(file_name, autoplay=True))

# 버전 1. 조용해질 때 까지 대기 후 녹음
# def listen(recognier):
#
#   # JavaScript 코드 (침묵 감지 녹음 기능)
#   RECORD = """
#     const sleep = time => new Promise((resolve) => setTimeout(resolve, time));
#
#     const b2text = blob => new Promise((resolve) => {
#       const reader = new FileReader();
#       reader.onloadend = (e) => resolve(e.srcElement.result);
#       reader.readAsDataURL(blob);
#     });
#
#     window.recordUntilSilence = (silenceTime = 2000, checkInterval = 200) => {
#       return new Promise(async (resolve) => {
#         const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
#         const recorder = new MediaRecorder(stream);
#         const audioContext = new AudioContext();
#         const source = audioContext.createMediaStreamSource(stream);
#         const analyser = audioContext.createAnalyser();
#
#         source.connect(analyser);
#         analyser.fftSize = 256;
#         const bufferLength = analyser.frequencyBinCount;
#         const dataArray = new Uint8Array(bufferLength);
#
#         const chunks = [];
#         let silenceStart = null;
#
#         const isSilent = () => {
#           analyser.getByteFrequencyData(dataArray);
#           const average = dataArray.reduce((a, b) => a + b) / bufferLength;
#           return average < 10; // 볼륨이 10 이하일 때 침묵으로 간주
#         };
#
#         recorder.ondataavailable = (e) => chunks.push(e.data);
#         recorder.start();
#         console.log("Recording started...");
#
#         const checkSilence = setInterval(() => {
#           if (isSilent()) {
#             if (!silenceStart) silenceStart = Date.now();
#             if (Date.now() - silenceStart >= silenceTime) {
#               console.log("Silence detected, stopping recording...");
#               clearInterval(checkSilence);
#               recorder.stop();
#             }
#           } else {
#             silenceStart = null;
#           }
#         }, checkInterval);
#
#         recorder.onstop = async () => {
#           const blob = new Blob(chunks);
#           const text = await b2text(blob);
#           resolve(text);
#         };
#       });
#     };
#   """
#
#   # 자바스크립트 코드 실행
#   display(Javascript(RECORD))
#
#   print("녹음을 시작합니다. 말을 멈추면 자동으로 종료됩니다...")
#   sound = output.eval_js('recordUntilSilence(2000, 200)')  # 침묵 시간 2초, 감지 주기 200ms
#   print("녹음이 종료되었습니다.")
#
#   # 녹음된 오디오 데이터를 저장
#   file_path = "recorded.wav"
#   b = b64decode(sound.split(',')[1])  # Base64로 인코딩된 오디오 데이터를 디코딩
#   audio = AudioSegment.from_file(BytesIO(b), format="webm")  # 오디오 데이터를 AudioSegment로 변환
#   audio.export(file_path, format="wav")
#
#   print(f"녹음된 파일이 저장되었습니다: {file_path}")
#
#   # 오디오 파일 열고 데이터를 인식기로 읽기
#   with sr.AudioFile(file_path) as source:
#     audio_data = recognier.record(source)
#
#   # 한국어로 TTS
#   text = recognizer.recognize_google(audio_data, language="ko")
#   print("변환된 텍스트:", text)
#
#   return text

# 버전 2. 5초 동안 듣기
def listen2(recognier):
  # JavaScript 코드 (5초 동안 녹음)
  RECORD = """
  const sleep = time => new Promise((resolve) => setTimeout(resolve, time));

  const b2text = blob => new Promise((resolve) => {
    const reader = new FileReader();
    reader.onloadend = (e) => resolve(e.srcElement.result);
    reader.readAsDataURL(blob);
  });

  window.record = time => new Promise(async (resolve) => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    const chunks = [];

    recorder.ondataavailable = (e) => chunks.push(e.data);
    recorder.start();
    console.log("Recording started...");

    await sleep(time);  // 녹음 시간 동안 대기

    recorder.onstop = async () => {
      const blob = new Blob(chunks);
      const text = await b2text(blob);
      resolve(text);
    };

    recorder.stop();
  });
  """

  # 자바스크립트 코드 실행
  display(Javascript(RECORD))

  # 녹음 시작
  print("5초 동안 녹음을 시작합니다...")
  sound = output.eval_js('record(5000)')  # 5000ms = 5초
  print("녹음이 종료되었습니다.")

  # 녹음된 오디오 데이터를 저장
  file_path = "recorded.wav"
  b = b64decode(sound.split(',')[1])  # Base64로 인코딩된 오디오 데이터를 디코딩
  audio = AudioSegment.from_file(BytesIO(b), format="webm")  # 오디오 데이터를 AudioSegment로 변환
  audio.export(file_path, format="wav")

  print(f"녹음된 파일이 저장되었습니다: {file_path}")

  # 오디오 파일 열고 데이터를 인식기로 읽기
  with sr.AudioFile(file_path) as source:
    audio_data = recognier.record(source)

  # 한국어로 TTS
  text = recognizer.recognize_google(audio_data, language="ko")

  return text


# 답변 생성
def answer(input_text):
  answer_text = ''

  if '이름' in input_text:
    answer_text = '내 이름은 AI야'
  elif '날씨' in input_text:
    answer_text = '오늘의 서울 기온은 10도 입니다. 눈이 내리고 있습니다.'
  elif '환율' in input_text:
    answer_text = '오늘의 환율은 1달러당 1300원 입니다.'
  else:
    answer_text = '무슨 말인지 모르겠어요.'

  return answer_text

# 번역
def translate(input_text):
  translator = Translator(from_lang='ko', to_lang='en')
  translation = translator.translate(input_text)
  return translation

# 답변 생성
def answer(input_text):
  answer_text = ''

  if '번역' in input_text:
    input_text = input_text.split('번역')[0]
    answer_text = translate(input_text)
  elif '이름' in input_text:
    answer_text = '내 이름은 AI야'
  elif '날씨' in input_text:
    answer_text = '오늘의 서울 기온은 10도 입니다. 눈이 내리고 있습니다.'
  elif '환율' in input_text:
    answer_text = '오늘의 환율은 1달러당 1300원 입니다.'
  else:
    answer_text = '무슨 말인지 모르겠어요.'

  return answer_text


# 음성 인식 객체 생성
recognizer = sr.Recognizer()

speak('무엇을 도와드릴까요?')
while True:
    time.sleep(2)

    input_text = listen2(recognizer)
    if '종료' in input_text:
        break

    answer_text = answer(input_text)
    speak(answer_text)