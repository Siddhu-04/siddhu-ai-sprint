# - [ ]  Embed 20 sentences using OpenAI. Find the 3 most-similar pairs.
# - [ ]  Visualize embeddings in 2D using `umap` or `t-SNE`

from sentence_transformers import SentenceTransformer
import numpy as np

import umap, matplotlib.pyplot as plt

sentences = [
    "The cat is on the table.",
    "The table is under the cat.",
    "The table is of red color.",
    "The fish is swimming in the pond.",
    "The sun is shining brightly.",
    "The moon is glowing at night.",
    "My love is just like moon.",
    "The Moon is so beautiful tonight.",
    "The flower is blooming in the spring.",
    "The river is flowing through the valley.",
    "The mountain is covered in snow.",
    "The car is parked in the driveway.",
    "The house is located in the city.",
    "The book is on the shelf.",
    "The phone is ringing on the desk.",
    "The computer is running a program.",
    "The music is playing in the background.",
    "The food is cooking in the kitchen.",
    "The water is boiling in the pot.",
    "The air is fresh in the morning."
]

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(sentences)

# for i in range(len(sentences)):
#     for j in range(i + 1, len(sentences)):
#         sim = np.dot(embeddings[i], embeddings[j]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]))
#         # print(f"Similarity between '{sentences[i]}' and '{sentences[j]}': {sim:.4f}")
#         most_similar_pairs = sorted([(sentences[i], sentences[j], sim) for i in range(len(sentences)) for j in range(i + 1, len(sentences))], key=lambda x: x[2], reverse=True)[:3]
# print("\nMost similar pairs:")
# for pair in most_similar_pairs:
#     print(f"'{pair[0]}' and '{pair[1]}' with similarity {pair[2]:.4f}")

# Visualize embeddings in 2D using UMAP
reducer = umap.UMAP(n_components=2, random_state=42)
embedding_2d = reducer.fit_transform(embeddings)
plt.figure(figsize=(10, 6))
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], color='blue')
for i, sentence in enumerate(sentences):
    plt.text(embedding_2d[i, 0], embedding_2d[i, 1], sentence, fontsize=9)
plt.title('UMAP Projection of Sentence Embeddings')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.grid()
plt.show()