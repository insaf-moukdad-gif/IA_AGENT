"""
tools.py
---------
Outils de HelpDeskBot.
"""

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

from rag import get_it_vector_store, search_with_relevance

load_dotenv()

tavily_client = TavilyClient()

vector_store = get_it_vector_store()


# Recherche dans la base documentaire
@tool
def search_kb(query: str) -> str:
    """Recherche une information dans la base documentaire."""

    results, sufficient = search_with_relevance(vector_store, query)

    if not results:
        return "Aucun résultat."

    documents = "\n\n".join(
        doc.page_content
        for doc in results
    )

    if sufficient:
        return "[SUFFISANT]\n" + documents

    return "[INSUFFISANT]\n" + documents


# Recherche Web
@tool
def search_web(query: str) -> str:
    """Recherche une information récente sur Internet."""

    results = tavily_client.search(query)
    return str(results)


CHECKLIST = {

    "reseau": [
        "Vérifier le Wi-Fi.",
        "Redémarrer le routeur.",
        "Tester Internet."
    ],

    "imprimante": [
        "Vérifier le papier.",
        "Vérifier l'imprimante.",
        "Redémarrer le service d'impression."
    ],

    "messagerie": [
        "Vérifier Internet.",
        "Redémarrer Outlook.",
        "Reconnecter le compte."
    ],

    "mot_de_passe": [
        "Réinitialiser le mot de passe.",
        "Vérifier si le compte est bloqué."
    ]
}


# Diagnostic
@tool
def diagnose(category: str) -> str:
    """Retourne les étapes de dépannage."""

    category = category.lower()

    if category not in CHECKLIST:
        return "Catégorie inconnue."

    return "\n".join(
        f"{i+1}. {step}"
        for i, step in enumerate(CHECKLIST[category])
    )


ticket = 0


# Création d'un ticket
@tool
def create_ticket(problem: str) -> str:
    """Crée un ticket de support."""

    global ticket

    ticket += 1

    return f"Ticket TCK-{ticket:03d} créé.\nProblème : {problem}"


all_tools = [
    search_kb,
    search_web,
    diagnose,
    create_ticket,
]

tools_by_name = {
    tool.name: tool
    for tool in all_tools
}