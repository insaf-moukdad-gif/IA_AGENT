"""
-------------
Evaluation du systeme sur 10 questions simples et 10 questions complexes.
Mesure : temps de reponse, nombre d'appels LLM/outils, sources recuperees.
"""

import time
from langchain.messages import HumanMessage
from graph import build_graph, save_graph_image
from report import add_result, save_excel

SIMPLE_QUESTIONS = [

    "Que faire si j'ai oublié mon mot de passe ?",

    "Comment débloquer un compte utilisateur ?",

    "Pourquoi je ne reçois plus mes e-mails ?",

    "Comment résoudre un problème de connexion à Outlook ?",

    "Que faire si je n'arrive pas à me connecter au Wi-Fi ?",

    "Comment résoudre un problème de connexion VPN ?",

    "Que faire si je n'ai plus accès à Internet ?",

    "Que faire si mon imprimante n'imprime plus ?",

    "Comment débloquer une impression bloquée ?",

    "Quels documents sont nécessaires pour demander l'accès à une nouvelle application ?",

]

COMPLEX_QUESTIONS = [

    "J'ai oublié mon mot de passe et après plusieurs tentatives mon compte est bloqué. Quelle procédure dois-je suivre ?",

    "Je suis connecté au Wi-Fi mais je n'ai toujours pas accès à Internet. Quelles vérifications dois-je effectuer ?",

    "Je travaille à distance et le VPN refuse de se connecter alors que ma connexion Internet fonctionne correctement.",

    "Outlook affiche une erreur de synchronisation et je ne reçois plus de nouveaux e-mails. Comment résoudre ce problème ?",

    "Mon imprimante réseau est allumée mais elle n'apparaît plus sur mon ordinateur. Que dois-je faire ?",

    "Je souhaite obtenir l'accès à une nouvelle application métier. Quelle est la procédure et quels documents dois-je fournir ?",

    "J'ai suivi toutes les étapes de dépannage du Wi-Fi mais le problème persiste. Peux-tu créer un ticket de support ?",

    "Mon imprimante reste bloquée malgré le redémarrage du service d'impression. Crée un ticket avec une priorité normale.",

    "Existe-t-il une nouvelle version de Microsoft Outlook ou des mises à jour importantes concernant le VPN de Microsoft ?",

    "Je ne parviens plus à accéder à ma messagerie, mon VPN ne fonctionne plus et mon compte semble bloqué. Quelle est la meilleure démarche à suivre ?"

]


def test(questions, title):

    # Construire le graphe
    agent = build_graph()

    # Générer une image du workflow
    save_graph_image(agent)

    config = {
        "configurable": {
            "thread_id": "evaluation"
        }
    }

    print(f"\n===== {title} =====")

    for i, question in enumerate(questions, 1):

        start = time.perf_counter()

        response = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            },
            config=config
        )

        temps_reponse = time.perf_counter() - start

        answer = response["messages"][-1].content

        add_result(
            question=question,
            time=round(temps_reponse, 2),
            llm_calls=response.get("llm_calls", 0),
            tool_calls=response.get("tool_calls_count", 0),
            answer=answer
)

        print(f"\nQuestion {i}")
        print(question)
        print("\nRéponse :")
        print(answer)
        print(f"\nTemps : {temps_reponse:.2f} s")


if __name__ == "__main__":

    test(SIMPLE_QUESTIONS, "Questions simples")

    test(COMPLEX_QUESTIONS, "Questions complexes")

    save_excel()

    print("\nRapport enregistré : test.xlsx")
