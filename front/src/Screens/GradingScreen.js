import React, {useState, useEffect} from 'react';
import 'Styles/main.css';
import 'Styles/demo.css';
import {TextField, Button} from '@mui/material';
import {checkGrammer, scoreAnswer} from 'utils/demo';
import { float2color, invertColor} from 'utils/misc';

export default function GradingScreen() {
  const [answer, setAnswer] = useState('He is walking on the road');
  const [candidates, setCandidates] = useState(['He walks on the street',
    'A man is walking on the road', 'He cannot walk well']);


  const [semanticReport, setSemanticReport] = useState();
  const [grammerReport, setGrammerReport] = useState();
  const [mode, setMode] = useState('ready'); // 0 for ready, 1 for report

  const setCandidatesIdx = (idx, val) => {
    setCandidates((cand) => {
      let new_cand = [...cand];
      new_cand[idx] = val;
      return new_cand;
    });
  };

  const checkSubmitValid = () => {
    if (answer.length < 3 || candidates[0].length == 0) {
      return false;
    }
    if (mode != 'ready') {
      return false;
    }
    return true;
  };

  const submitAnswer = async () => {
    try {
      const gramRsp = await checkGrammer(answer);
      setGrammerReport(gramRsp);
      const semRsp = await scoreAnswer(answer, candidates);
      setSemanticReport(semRsp);
      setMode('report');
    } catch (e) {
      console.warn(e);
    }
  };
  const renderAnswerInput = (idx) => {
    return (
      <div className='answer-input' key={idx}>
        <TextField
          fullWidth
          variant='standard'
          value={candidates[idx]}
          onChange={(e) => setCandidatesIdx(idx, e.target.value)}
        />
      </div>
    );
  };
  return (
    <div >
      <h1> Grading Student Answer</h1>
      <div className='input-container'>
        <div className='label'>
          <span>User Submission</span>
        </div>
        <div className='user-input'>
          <TextField
            variant='standard'
            fullWidth
            label='User Answer'
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            disabled={mode != 'ready'}
          />
        </div>
        <div className='label'>
          <span>Answers</span>
        </div>
        {[0, 1, 2].map((idx) => (
          renderAnswerInput(idx)
        ))}
        <div className='submit'>
          <Button
            variant='contained'
            disabled={!checkSubmitValid()}
            onClick={() => submitAnswer()}
          >
            Grade Answer
          </Button>
        </div>
      </div>

      {mode == 'report' && semanticReport &&
        <SemanticReport report={semanticReport}/>
      }
      {mode == 'report' && grammerReport &&
        <GrammerReport report={grammerReport} sentence={answer}/>
      }
      {mode == 'report' &&
        <div className='reset-container'>
          <Button
            variant='contained'
            onClick={() => setMode('ready')}
          >
          reset
          </Button>
        </div>
      }
    </div>
  );
}

function SemanticReport({report}) {
  if (!report) {
    return null;
  }
  const renderHeat = (heat, relation, key) => {
    const bgcolor = float2color(heat);
    const textColor = invertColor(bgcolor);
    return (
      <div className='heat' style={{backgroundColor: bgcolor}} key={key}>
        <span style={{color: textColor}}>
          {heat.toFixed(2)}
          {relation=='contradiction'&&
          <span>*</span>
          }
        </span>
      </div>
    );
  };
  return (
    <div>
      <h1>Semantic Similarity</h1>
      <div className='semantic-container'>
        <div>
        </div>
        {report.map((val, idx) => (
          <div className='label' key={idx}>{val.sentence}</div>
        ))
        }
        <div className='label'>
          {report[0].compare}
        </div>
        {report.map((val, idx) => (
          renderHeat(val.score, val.relation, idx)
        ))
        }
        <div className="note-box">
          <span>* : Semantically Contradict</span>
        </div>
      </div>
      {/* <span>{ JSON.stringify(report)   }</span> */}
    </div>
  );
}

function GrammerReport({sentence, report}) {
  const Highlight = ({ text, substrings }) => {
    const html = substrings.reduce((acc, cur, idx) => {
      return acc.replace(
        new RegExp(
          '(?<=^.{' + (cur.offset + idx * 17) + '})(.{' + cur.length + '})',
        ),
        (str) => `<strong>${str}</strong>`,
      );
    }, text);
    return <span className='highlight' dangerouslySetInnerHTML={{ __html: html }} />;
  };
  if (!report) {
    return null;
  }
  if (report.length == 0) {
    return (
      <div>
        <h1>Grammer Check</h1>
        <p>No grammatical mistake found</p>
      </div>
    );
  }
  const substrings = report.map((item) => ({offset: item.offset, length: item.errorLength}));
  const renderExplain = (item, key) => {
    const wrong = sentence.slice(item.offset, item.offset + item.errorLength);
    let right = null;
    if (item.replacements && item.replacements.length > 0 ) {
      console.log(item.replacements)
      right = item.replacements.slice(0, 3).join('  | ');
    }
    return (
      <div key={key}>
        <div className='check-mark'>&#10004;</div>
        <span className='wrong'>{wrong}</span>
        {right &&
        <span> should be <span className='right'>{right}</span></span>
        }
        <br/>
        <span className='explain'>{item.message}</span>
      </div>
    );
  };
  return (
    <div className='grammer-container'>
      <h1>Grammer Check</h1>
      <div className='highlight-box'>
        <span className='highlight thick'>Correction: </span>
        <Highlight text={sentence} substrings={substrings}/>
      </div>
      <div className='explain-container'>
        {report.map((item, idx) => renderExplain(item, idx))
        }
      </div>
      {/* <span>{JSON.stringify(report)}</span> */}
    </div>
  );
}