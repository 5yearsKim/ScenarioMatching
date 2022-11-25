import React, {useState, useEffect} from 'react';
import 'Styles/main.css';
import 'Styles/demo.css';
import {scriptInfo} from 'utils/demo';
// import Typing from 'react-typing-animation';
import TypeWriter from 'Components/TypeWriter';
import {TextField, Button} from '@mui/material';
import { scriptRespond } from 'utils/demo';

const SCRIPT_LIST = ['sample'];

export default function ScriptScreen() {
  const [scriptId, setScriptId] = useState(SCRIPT_LIST[0]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [npcName, setNpcName] = useState('');
  const [npcSay, setNpcSay] = useState('');
  const [answer, setAnswer] = useState('');
  const [hint, setHint] = useState('');
  const [turnIdx, setTurnIdx] = useState(0);
  const [trial, setTrial] = useState(0);
  const [infoText, SetInfoText] = useState({});

  useEffect(() => {
    const m_scriptInfo = async () => {
      const info = await scriptInfo(scriptId);
      setTitle(info.title);
      setDescription(info.description);
      setNpcName(info.npc_name);
      setNpcSay(info.npc);
      setAnswer('');
      setHint('');
      setTurnIdx(0);
      SetInfoText({});
    };
    m_scriptInfo();
  }, [scriptId]);

  const onSubmit = async () => {
    const rsp = await scriptRespond(scriptId, turnIdx, answer, trial );
    setNpcSay(rsp.npc);
    setTurnIdx(rsp.turn_idx);
    setHint(rsp.hint);
    if (rsp.isSuccess) {
      setTrial(0);
    } else {
      setTrial(val => val + 1);
    }

    const infoText = {
      your_answer: answer,
      is_success: rsp.is_success,
      answer: rsp.last_answer,
      trial: trial,
    };
    SetInfoText(infoText);
  };
  return (
    <div >
      <h1> {title} </h1>
      <div>
        <span className='description'>{description}</span>
      </div>
      <div className='script-container'>
        <div className='empty-box'/>
        <div className='chat-box'>
          <div className='npc-box'>
            <span>{npcName}: </span>
            <TypeWriter text={npcSay}/>
          </div>
          <div className='hint-box'>
            { hint && hint.length > 0 &&
              <span>Hint: </span>
            }
            <span>{hint}</span>
          </div>
          <div className='input-box'>
            <TextField
              value={answer}
              fullWidth
              variant="standard"
              onChange={(e) => setAnswer(e.target.value)}
            />
            <Button
              variant='contained'
              onClick={async () => await onSubmit() }
            >
          submit
            </Button>
          </div>
        </div>
        <div className='noti-box'>
          { infoText && Object.keys(infoText).length > 0 &&
            <pre>{JSON.stringify(infoText, null, 2)}</pre>
          }
        </div>
      </div>

    </div>
  );
}