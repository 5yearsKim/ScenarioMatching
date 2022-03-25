from .db_handler import DBHandler
from .vectorizer import Vectorizer
from .utils import read_scenario, batching_list, np_to_blob
from .type_models import ScriptIn, ScriptOut, ScriptInfo
class Scripter:
    def __init__(self, script_map, db_path='vector.db'):
        self.script_map = script_map
        self.dh = DBHandler(db_path)
        self.vectorizer = Vectorizer()

    
    def setup_script(self):
        ''' add answer sentence to db '''
        holder = []
        for file in self.script_map.values():
            script = read_scenario(file)
            for item in script.script:
                answers = item.answer if hasattr(item, 'answer') else []
                holder.extend(list(answers))
        for sent in holder:
            self.dh.insert_utterance(sent.trim())
        
        '''vectorize unvectorized sentence '''
        unvectorized = self.dh.get_unvectorized()
        print(len(unvectorized))
        batched_unvectorized = batching_list(unvectorized, n=4)
        for items in batched_unvectorized:
            sents = list(map(lambda x: x.sentence, items))
            vectors = self.vectorizer(sents)
            for item, vector in zip(items, vectors):
                item.vector = vector.numpy()
        print(unvectorized)
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
        candidates = item.answer
        is_true, picked = self.check_answer(answer, candidates)
        print(is_true, picked)

    def check_answer(self, answer, candidates, threshold=0.8):
        print(answer, candidates)
        picked_ans = 'sample'
        return True, picked_ans
