import axios from 'axios';

// const server = axios.create({baseURL: 'https://server-lim-demo.onioncontent.com', timeout: 4000});
const server = axios.create({baseURL: 'http://localhost:8001', timeout: 4000});

export async function scoreAnswer(answer, candidates) {
  const data = {
    answer: answer,
    candidates: candidates,
  };
  const rsp = await server.post('/score_answer', data );
  return rsp.data;
}

export async function checkGrammer(sentence) {
  const params = {sentence: sentence};
  const rsp = await server.get('/check_grammer', {params: params});
  return rsp.data;
}

export async function scriptInfo(scriptId) {
  const rsp = await server.get('/script_info/' + scriptId);
  return rsp.data;
}

export async function scriptRespond(scriptId, turnIdx, answer, trial) {
  const data = {
    turn_idx: turnIdx,
    answer: answer,
    trial: trial,
  };
  const rsp = await server.post('/script_respond/' + scriptId, data);
  return rsp.data;
}
