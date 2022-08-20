import React, { useState } from 'react';
import axios from 'axios';

function Record() {
    const [speech, setSpeech] = useState('');
    const [prediction, setPrediction] = useState('');



    const handleInput = (event) => {
        setSpeech(event.target.value);
    }

    
    const handleKeyPress = (event) => {
        if (event.key === "Enter") {
            onClickInput();
        }
    }

    const onClickInput = async () => {
        try {
            console.log('Input : ', speech)
            const response = await axios.post(`http://127.0.0.1:8000/character/${speech}`)
            if(response.status === 200) {
                console.log(response.data.contents)
                setPrediction(response.data.contents)
                document.location.href = `/contents/${prediction}`
            }
        } catch (error) {
            console.dir(error)
        }
        
    }




    return(
        <div className="hackathon">
            <h1 className='title'>Hello</h1>
            <h3 className='subtitle'>Speech to Text :D</h3>
            <div>
                <textarea className="box" type = "text" name = "input" value = {speech} onChange = {handleInput} onKeyPress = {handleKeyPress} />
            </div>
            <div>
                <button className="button" type="button" onClick={onClickInput}>input</button>
            </div>
        </div>
    )
}


export default Record;