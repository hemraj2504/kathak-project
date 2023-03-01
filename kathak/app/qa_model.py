import torch
import numpy as np
from transformers import AutoTokenizer, pipeline, AutoModelForQuestionAnswering

model = AutoModelForQuestionAnswering.from_pretrained("./app/mobilebert-squad")
tokenizer = AutoTokenizer.from_pretrained("./app/mobilebert-squad")
qa_pipeline = pipeline(
    "question-answering",
    model=model,
    tokenizer=tokenizer
)

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def get_answers(context,question):
    input_ids = tokenizer.encode(question, context)
    # Search for `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    num_seg_a = sep_index + 1
    num_seg_b = len(input_ids) - num_seg_a

    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    outputs = model(
                torch.tensor([input_ids]),
                token_type_ids=torch.tensor([segment_ids]),
                return_dict=True
            ) 

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    all_scores = softmax((start_scores+end_scores).detach().numpy())

    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    answer = tokens[answer_start]
    for i in range(answer_start + 1, answer_end + 1):
        
        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        else:
            answer += ' ' + tokens[i]
    prediction = {
        'score': all_scores.max(),
        'answer':answer
    }
    return prediction

def get_answer(content, question):
    # content = _text.content
    print (question)
    predictions = qa_pipeline({
        'context': content,
        'question': question
    })
    return predictions