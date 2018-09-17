import jieba
import json
from concurrent.futures import ThreadPoolExecutor


class SynonymsReplacer:
    """
    同义句生成
    original text : 吸烟的危害是什么
    result：['吸烟的危害是什么', '吸烟的危害是那些', '吸烟的危害为什么', '吸烟的危害为那些', '吸烟的害处是什么', '吸烟的害处是那些', '吸烟的害处为什么', '吸烟的害处为那些']

    """
    def __init__(self, synonyms_file_path):

        # self.synonyms = self.load_synonyms(synonyms_file_path)
        self.synonyms_file_path = synonyms_file_path
        # self.segmentor = self.segment(cws_model_path)
        self.candidate_synonym_list = {}  # 每个元素为句子中每个词及其同义词构成的列表

    def segment(self, sentence):

        """调用pyltp的分词方法将str类型的句子分词并以list形式返回"""

        return list(jieba.cut(sentence, cut_all=False))

    def load_synonyms(self, file_path):

        """

        加载同义词表

        :param file_path: 同义词表路径

        :return: 同义词列表[[xx,xx],[xx,xx]...]

        """

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in json.load(file):
                sign = yield line
                if sign == 'stop':
                    break

    def permutation(self, data):

        """
        排列函数
        :param data: 需要进行排列的数据，列表形式

        :return:

        """

        assert len(data) >= 1, "Length of data must greater than 0."

        if len(data) == 1:  # 当data中只剩（有）一个词及其同义词的列表时，程序返回

            return data[0]

        else:

            head = data[0]

            tail = data[1:]  # 不断切分到只剩一个词的同义词列表

        tail = self.permutation(tail)
        permt = []
        for h in head:  # 构建两个词列表的同义词组合

            for t in tail:
                if isinstance(t, str):  # 传入的整个data的最后一个元素是一个一维列表，其中每个元素为str
                    permt.extend([[h] + [t]])
                elif isinstance(t, list):
                    permt.extend([[h] + t])
        return permt

    def search_synonyms(self, word, word_synonyms, index):
        """
        根据同义词列表，对每一个word做搜寻匹配
        :param word:
        :param word_synonyms:
        :param index:
        :return:
        """
        synonyms_generation = self.load_synonyms(self.synonyms_file_path)
        for syn in synonyms_generation:  # 遍历同义词表，syn为其中的一条
            try:
                if word in syn:  # 如果句子中的词在同义词表某一条目中，将该条目中它的同义词添加到该词的同义词列表中
                    syn.remove(word)
                    word_synonyms.extend(syn)
                    synonyms_generation.send('stop')
            except StopIteration:
                break
        return {index: word_synonyms}

    def add_synonyms(self, obj):
        """
        # 添加一个词语的同义词列表
        :param obj:
        :return:
        """
        obj = obj.result()
        self.candidate_synonym_list.update(obj)


    def get_syno_sents_list(self, input_sentence):

        """
        产生同义句，并返回同义句列表，返回的同义句列表没有包含该句本身

        :param input_sentence: 需要制造同义句的原始句子

        :return:

        """

        assert len(input_sentence) > 0, "Length of sentence must greater than 0."

        seged_sentence = self.segment(input_sentence)

        pool = ThreadPoolExecutor(len(seged_sentence))
        for index, word in enumerate(seged_sentence):
            word_synonyms = [word]
            pool.submit(self.search_synonyms, word, word_synonyms, index).add_done_callback(self.add_synonyms)
        pool.shutdown()
        d1 = sorted(self.candidate_synonym_list.items(), key=lambda k: k[0])
        candidate_synonym_list = [k[1] for k in d1]
        perm_sent = self.permutation(candidate_synonym_list)  # 将候选同义词列表们排列组合产生同义句

        syno_sent_list = []
        for p in perm_sent:

            syno_sent_list.append("".join(p))
        return syno_sent_list

if __name__ == '__main__':
    s = SynonymsReplacer('new_synomys.json')
    result = s.get_syno_sents_list("吸烟的危害是什么")
    print(result)
