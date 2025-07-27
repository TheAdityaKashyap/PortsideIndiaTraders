from flask import Flask, request, jsonify
import json
from sentence_transformers import SentenceTransformer, util
import torch
import re

app = Flask(__name__)

# Load website content
with open('website_content.json') as f:
    content = json.load(f)

# Initialize model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute page embeddings
pages = [item['text'] for item in content]
page_embeddings = model.encode(pages, convert_to_tensor=True)

def split_sentences(text):
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    query_embedding = model.encode(question, convert_to_tensor=True)

    # ---- Step 1: Find top 3 most relevant pages ----
    page_scores = util.pytorch_cos_sim(query_embedding, page_embeddings)[0]
    top_page_indices = torch.topk(page_scores, k=3).indices.tolist()

    all_candidate_sentences = []
    all_sentence_sources = []

    # ---- Step 2: For each top page, get its best sentences ----
    for idx in top_page_indices:
        page_text = content[idx]['text']
        page_url = content[idx]['url']
        sentences = split_sentences(page_text)
        if not sentences:
            continue
        sent_embeddings = model.encode(sentences, convert_to_tensor=True)
        sent_scores = util.pytorch_cos_sim(query_embedding, sent_embeddings)[0]
        top_sent_scores, top_sent_indices = torch.topk(sent_scores, k=min(3, len(sentences)))

        for s_idx, s_score in zip(top_sent_indices.tolist(), top_sent_scores.tolist()):
            all_candidate_sentences.append((sentences[s_idx], s_score))
            all_sentence_sources.append(page_url)

    # ---- Step 3: Rank all candidate sentences globally ----
    all_candidate_sentences_with_source = list(zip(all_candidate_sentences, all_sentence_sources))
    all_candidate_sentences_with_source.sort(key=lambda x: x[0][1], reverse=True)

    # ---- Step 4: Take top 3 best sentences overall ----
    top_answers = []
    for (sentence, score), source in all_candidate_sentences_with_source[:3]:
        top_answers.append({
            "sentence": sentence,
            "score": float(score),
            "source": source
        })

    return jsonify({"answers": top_answers})

if __name__ == "__main__":
    app.run(port=5000)
