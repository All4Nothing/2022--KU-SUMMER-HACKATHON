import React, {useState} from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import axios from 'axios';


function Dictaphone() {
  const {transcript, listening, resetTranscript, browserSupportsSpeechRecognition} = useSpeechRecognition();
  const [text, setText] = useState('');

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }


  const onClickInput = async () => {
      try {
          console.log('transcript : ', transcript)
          const speech = {
            text : transcript
          }
          const response = await axios.post(`http://127.0.0.1:8000/character/`, speech)
          console.log(response)
          if(response.status === 200) {
              console.log(response.data.contents)
              setText(response.data.contents)
              // TODO document.location.href = `/contents/${text}` -> contents페이지로 연결
          }
      } catch (error) {
          console.dir(error)
      }
      
  }


  return (
    <div>
      <p>Microphone: {listening ? 'on' : 'off'}</p>
      <button onClick={SpeechRecognition.startListening}>Start</button>
      <button onClick={()=>{
        SpeechRecognition.stopListening();
        onClickInput();
      }}>Stop</button>
      <button onClick={resetTranscript}>Reset</button>
      <p>{transcript}</p>
      <p>{text}</p>
    </div>
  );
};
export default Dictaphone;