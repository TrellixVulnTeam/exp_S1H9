''' Data Loader class for training iteration '''
import random
import numpy as np
import torch
from torch.autograd import Variable

def cover_text2int(sentence):
    tokens = sentence.strip().split(",")
    return [int(token) for token in tokens]

class DataLoader(object):
    ''' For data iteration '''

    def __init__(
            self, data,
            cuda=True, batch_size=64, test=False):

        self.cuda = cuda
        self.test = test

        #f = open(data)
        count = 39780811
        #for count, _ in enumerate(f):
        #    pass
        #count += 1
        #f.close()

        self.length = count
        
        self._n_batch = int(np.ceil(self.length / batch_size))
        self._batch_size = batch_size

        self._iter_count = 0

        self.data_file = data
        self.data = open(data)

    @property
    def n_insts(self):
        ''' Property for dataset size '''
        return self.length

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __len__(self):
        return self._n_batch

    def next(self):
        ''' Get the next batch '''

        def pad_to_longest(insts, max_len):
            ''' Pad the instance to the max seq length in batch '''
            inst_data = np.array([
                inst[:max_len] + [0] * (max_len - len(inst[:max_len]))
                for inst in insts])
            mask = np.zeros((inst_data.shape[0], inst_data.shape[1]))
            for b in range(len(inst_data)):
                for i in range(len(inst_data[b])):
                    if inst_data[b, i] > 0:
                        mask[b, i] = 1
            mask_tensor = Variable(
                    torch.FloatTensor(mask), requires_grad = False)
            inst_data_tensor = Variable(
                    torch.LongTensor(inst_data), volatile=self.test)
            if self.cuda:
                mask_tensor = mask_tensor.cuda()
                inst_data_tensor = inst_data_tensor.cuda()
            return inst_data_tensor, mask_tensor

        if self._iter_count < self._n_batch:
            batch_idx = self._iter_count

            q_list = []
            pos_list = []
            neg_list = []
            pos_axm_list = []
            neg_axm_list = []
            pos_adj_list = []
            neg_adj_list = []

            while True:
                self._iter_count += 1
                for i in range(self._batch_size):
                    line = self.data.readline().strip().split('\t')

                    if len(line) < 7:
                        continue

                    query = line[0]
                    pos = line[1]
                    neg = line[2]
                    axm_pos = line[3]
                    adj_pos = line[4]
                    axm_neg = line[5]
                    adj_neg = line[6]
                   
                    query = cover_text2int(query)
                    pos = cover_text2int(pos)
                    neg = cover_text2int(neg)
                    pos_axm = cover_text2int(axm_pos)
                    neg_axm = cover_text2int(axm_neg)
                    pos_adj = cover_text2int(adj_pos)
                    neg_adj = cover_text2int(adj_neg)
                    # print(len(query), len(pos), len(neg))
                    if sum(query) == 0 or sum(pos) == 0 or sum(neg) == 0 or sum(pos_axm) == 0 or sum(neg_axm) == 0 or sum(pos_adj) == 0 or sum(neg_adj) == 0:
                        continue

                    q_list.append(query)
                    pos_list.append(pos)
                    neg_list.append(neg)
                    pos_axm_list.append(pos_axm)
                    neg_axm_list.append(neg_axm)
                    pos_adj_list.append(pos_adj)
                    neg_adj_list.append(neg_adj)

                if len(q_list) != 0:
                    break

            inst_q, mask_q = pad_to_longest(q_list, 20)
            inst_d_pos, mask_d_pos = pad_to_longest(pos_list, 200)
            inst_d_neg, mask_d_neg = pad_to_longest(neg_list, 200)

            inst_d_pos_axm, mask_d_pos_axm = pad_to_longest(pos_axm_list, 200)
            inst_d_neg_axm, mask_d_neg_axm = pad_to_longest(neg_axm_list, 200)

            inst_d_pos_adj, mask_d_pos_adj = pad_to_longest(pos_adj_list, 200)
            inst_d_neg_adj, mask_d_neg_adj = pad_to_longest(neg_adj_list, 200)


            return inst_q, inst_d_pos, inst_d_neg, inst_d_pos_axm, inst_d_neg_axm, inst_d_pos_adj, inst_d_neg_adj, mask_q, mask_d_pos, mask_d_neg, mask_d_pos_axm, mask_d_neg_axm, mask_d_pos_adj, mask_d_neg_adj

        else:

            self._iter_count = 0
            self.data = open(self.data_file)
            raise StopIteration()
