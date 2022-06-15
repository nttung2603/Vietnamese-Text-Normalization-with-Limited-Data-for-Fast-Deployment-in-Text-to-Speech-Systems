import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class BiLSTM(nn.Module):
    def __init__(self, vocab_size, tagset_size, embedding_dim, hidden_dim, device, num_rnn_layers=1, rnn="lstm", embedding_weights = None, loss_weights = None):
        super(BiLSTM, self).__init__()
        #self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size
        self.tagset_size = tagset_size
        self.device = device
        #self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.embedding = nn.Embedding.from_pretrained(embedding_weights, freeze = True)
        RNN = nn.LSTM if rnn == "lstm" else nn.GRU
        self.rnn = RNN(embedding_dim, 
                       hidden_dim // 2, 
                       num_rnn_layers,
                       bidirectional=True, 
                       batch_first=True)
        self.fc = nn.Linear(hidden_dim, tagset_size)
        self.loss_fn = nn.CrossEntropyLoss(weight = torch.tensor(loss_weights).float(), ignore_index=0)
    def __build_features(self, sentences):
        masks = sentences != 0
        embeds = self.embedding(sentences.long())
        seq_length = masks.sum(1).to(self.device)
        sorted_seq_length, perm_idx = seq_length.sort(descending=True)
        embeds = embeds[perm_idx, :]

        pack_sequence = pack_padded_sequence(embeds, lengths=sorted_seq_length.to("cpu"), batch_first=True)
        packed_output, _ = self.rnn(pack_sequence)
        lstm_out, _ = pad_packed_sequence(packed_output, batch_first=True)
        _, unperm_idx = perm_idx.sort()
        lstm_out = lstm_out[unperm_idx, :]
        return lstm_out, masks

    def loss(self, xs, tags):
        features, masks = self.__build_features(xs)
        #features = features.view(-1, features.shape[2])
        features = self.fc(features)
        #features = F.log_softmax(features, dim=1)
        L = features.size(1)
        features = torch.transpose(features, 1, 2)
        tags = tags[:,:L]
        loss = self.loss_fn(features, tags)
        return loss

    def forward(self, xs):
        # Get the emission scores from the BiLSTM
        features, masks = self.__build_features(xs)
        features = self.fc(features)
        return features
    def predict(probs, accept_class):
        preds = probs.argmax(dim=2)
        return preds