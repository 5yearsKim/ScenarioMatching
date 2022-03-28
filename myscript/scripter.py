from .db_handler import DBHandler
# from .vectorizer import Vectorizer
from .utils import read_scenario, batching_list, np_to_blob, blob_to_np, cosine_similarity
from .type_models import ScriptOut, ScriptInfo, Sentence, SentenceScore
from .scorer import Scorer

class Scripter:
    def __init__(self, script_map, db_path='vector.db', score_mode='direct'):
        self.script_map = script_map
        self.dh = DBHandler(db_path)
        # self.vectorizer = Vectorizer()
        # self.setup_script()
        self.scorer = Scorer(load_path='ckpts/mtbert.pt')
    
    def setup_script(self):
        ''' add answer sentence to db '''
        holder = []
        for file in self.script_map.values():
            script = read_scenario(file)
            for item in script.script:
                answers = item.answer if hasattr(item, 'answer') else []
                holder.extend(list(answers))
        for sent in holder:
            self.dh.insert_utterance(sent)
        
        '''vectorize unvectorized sentence '''
        unvectorized = self.dh.get_unvectorized()
        print(len(unvectorized), ' unvectorized from answer..')
        batched_unvectorized = batching_list(unvectorized, n=4)
        for items in batched_unvectorized:
            sents = list(map(lambda x: x.sentence, items))
            vectors = self.vectorizer(sents)
            for item, vector in zip(items, vectors):
                item.vector = vector.numpy()
        for item in unvectorized:
            v_blob = np_to_blob(item.vector)
            self.dh.set_vector(item.id, v_blob)
        print('setup vector done')

    def get_info(self, script_id):
        if script_id not in self.script_map:
            print(f'{script_id} not in candidates')
            return None
        script_path = self.script_map[script_id]
        script = read_scenario(script_path)
        npc = script.script[0].npc
        return ScriptInfo(title=script.title, description=script.description, npc_name=script.npc_name, npc=npc)

    def respond(self, script_id, turn_idx, answer, trial=0):
        if script_id not in self.script_map:
            print(f'{script_id} not in candidates')
            return None
        script_path = self.script_map[script_id]
        script = read_scenario(script_path).script
        try:
            item = script[turn_idx]
        except:
            item = script[-1]
        ''' last item is for goodbye'''
        if turn_idx >= len(script) - 1:
            return ScriptOut(is_success=False, turn_idx = len(script) - 1, npc=item.npc, is_end=True)

        ''' answer check ''' 
        candidates = item.answer
        is_success, picked = self.check_answer(answer, candidates, threshold=0.8)
        if is_success:
            new_idx = turn_idx + 1
            is_end =  new_idx >= len(script) - 1
            new_item = script[new_idx]
            hint = new_item.hint[0] if not is_end else None
            return ScriptOut(is_success=True, turn_idx=new_idx, npc=new_item.npc, last_answer=picked, hint=hint, is_end=is_end)
        else:
            hint = item.hint[trial] if trial < len(item.hint) else item.hint[-1]
            return ScriptOut(is_success=False, turn_idx=turn_idx, npc=item.npc_error, hint=hint)


    def check_answer(self, answer, candidates, threshold=0.8):
        scored = self.score_answer_direct(answer, candidates, combine_score=True)
        picked_ans = max(scored, key=lambda x: x.score)
        if picked_ans.score > threshold:
            return True, picked_ans
        else:
            return False, None

    def score_answer_direct(self, answer, candidates, combine_score=False):
        ans_list = [answer for _ in range(len(candidates))]
        sim_scores, relations = self.scorer.score_sentence(ans_list, candidates)
        holder = []
        for cand, score, relation in zip(candidates, sim_scores, relations):
            if combine_score:
                if relation == 'contradiction':
                    score = score / 2
                elif relation == 'entailment':
                    score = score + 0.1
            sent_score = SentenceScore(compare=answer, sentence=cand, score=score, relation=relation)
            holder.append(sent_score)
        return holder

    def score_answer_from_vector(self, answer, candidates):
        candidates = list(map(lambda x: x.strip(), candidates))
        ans_v = self.vectorizer([answer])[0].numpy()
        cached_candidate = self.dh.get_vectorized_by_sentence(candidates)
        rest_candidates = set(candidates) - set(map(lambda x: x.sentence, cached_candidate))

        to_vectorize = [*rest_candidates, answer]
        vectors = self.vectorizer(to_vectorize)
        for i, (sent, vector) in enumerate(zip(to_vectorize, vectors)):
            if i < len(to_vectorize) - 1:
                sent = Sentence(id=-10000+i, sentence=sent, vector=np_to_blob(vector.numpy()))
                cached_candidate.append(sent)
            else:
                ans_v = vector.numpy()
        holder = []
        for cand in cached_candidate:
            cand_v = blob_to_np(cand.vector)
            score = cosine_similarity(ans_v, cand_v) 
            sent_score = SentenceScore(compare=answer, sentence=cand.sentence, score=score)
            holder.append(sent_score)
        return holder
    
    


