from flask import Flask, request, jsonify
import json
from sentence_transformers import SentenceTransformer, util
import torch
import re

app = Flask(__name__)
 
# Load website content
with open('website_content.json') as f:
    content = json.load(f)

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings
pages = [item['text'] for item in content]
page_embeddings = model.encode(pages, convert_to_tensor=True)

def split_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    query_emb = model.encode(question, convert_to_tensor=True)
    page_scores = util.pytorch_cos_sim(query_emb, page_embeddings)[0]
    top_page_indices = torch.topk(page_scores, k=3).indices.tolist()

    all_candidates = []
    for idx in top_page_indices:
        sentences = split_sentences(content[idx]['text'])
        if not sentences:
            continue
        sent_emb = model.encode(sentences, convert_to_tensor=True)
        sent_scores = util.pytorch_cos_sim(query_emb, sent_emb)[0]
        top_scores, top_idx = torch.topk(sent_scores, k=min(3, len(sentences)))
        for s_i, s_score in zip(top_idx.tolist(), top_scores.tolist()):
            all_candidates.append({
                "sentence": sentences[s_i],
                "score": float(s_score),
                "source": content[idx]['url']
            })

    # sort globally
    all_candidates.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({"answers": all_candidates[:3]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
