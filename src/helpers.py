class helpers:
    def __init__(self,labels,data):
        
        self.labels = labels
        self.data = data
        self.id2label = dict(enumerate(labels)) # integer label to BIO format label mapping
        self.label2id = {v:k for k,v in self.id2label.items()} # BIO format label to integer label mapping
        self.tokenized_data = []
        
    def labels_to_ids(self):
        _data = []
        for _dictionary in self.data:
            _dictionary['labels_id'] = [self.label2id[i] for i in _dictionary['labels']]
            _data.append(_dictionary)
        self.data = _data
        return self.data
        
    def tokenize_and_align_labels(self,examples,tokenizer):
        _tokenized_inputs = tokenizer(examples["tokens"], is_split_into_words=True)
        _tokenized_inputs["document"] = examples["document"]

        _labels = []
        _label=examples[f"labels_id"]
        _word_ids = _tokenized_inputs.word_ids()  # Map tokens to their respective word.
        _previous_word_idx = None
        _label_ids = []
        for _word_idx in _word_ids:  # Set the special tokens to -100.
            if _word_idx is None:
                _label_ids.append(-100)
            elif _word_idx != _previous_word_idx:  # Only label the first token of a given word.
                _label_ids.append(_label[_word_idx])
            else:
                _label_ids.append(-100)
            _previous_word_idx = _word_idx

        _tokenized_inputs["labels_ids"] = _label_ids
        return _tokenized_inputs
    
    def token_data(self,tokenizer):
        _tokenized_data = []
        for _example in self.data:
            _tokenized_data.append(self.tokenize_and_align_labels(_example,tokenizer))
        self.tokenized_data = _tokenized_data
        return self.tokenized_data
            
            
            
    