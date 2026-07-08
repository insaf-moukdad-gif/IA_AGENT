# HelpDeskBot – Agent IA de Support Informatique

HelpDeskBot est un agent conversationnel intelligent développé avec **LangGraph**, **LangChain** et **RAG (Retrieval-Augmented Generation)**. Il assiste les utilisateurs dans la résolution des problèmes informatiques courants en s'appuyant sur une base documentaire interne, une recherche Web et plusieurs outils spécialisés.

---

## Fonctionnalités

- Recherche dans une base documentaire (RAG)
- Recherche Web via Tavily
- Diagnostic de problèmes informatiques
- Création de tickets de support
- Mémoire de conversation avec LangGraph
- Visualisation du graphe de l'agent
- Évaluation automatique de l'agent

---

## Structure du projet

```
HelpDeskBot/
│
├── test.py
├── graph.py
├── etat.py
├── prompt.py
├── tool.py
├── rag.py
├── report.py
├── graph.png
├── README.md
│
├── data/
│  
│
└── .env
```

---

## Technologies utilisées

- Python 3.12+
- LangChain
- LangGraph
- Ollama
- Llama 3.2:3B
- HuggingFace Embeddings
- InMemoryVectorStore
- Tavily Search API
- PyPDF
- OpenPyXL

---

## Lancer l'agent
```bash
python test.py
```
