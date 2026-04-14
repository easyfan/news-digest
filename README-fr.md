[English](README.md) | [中文](README-CN.md) | [Deutsch](README-de.md) | [Français](README-fr.md) | [Русский](README-ru.md)

# news-digest

Digest d'actualités IA multi-sources pour Claude Code — récupère, résume et apprend des dernières actualités technologiques IA provenant de 12 sources.

```
/news-digest                    # digest complet + couche d'apprentissage
/news-digest --no-learn         # actualités uniquement (mode rapide)
/news-digest llm agent          # filtrer par mot-clé
/news-digest --sources hn,hf    # sources spécifiques uniquement
```

---

## Fonctionnement

**Étape 1 — Notification & récupération** : affiche une bannière avec le temps estimé (20–40 s pour les actualités, +60–80 s avec la couche d'apprentissage) puis récupère depuis 12 sources en un seul appel Bash :

| Source | Contenu |
|--------|---------|
| `hn` | Page d'accueil Hacker News |
| `arxiv` | Derniers articles arXiv cs.AI |
| `hf` | HuggingFace Daily Papers (IA curatée) |
| `github` | Dépôts GitHub Trending |
| `anthropic` | Actualités officielles Anthropic |
| `openai` | Actualités OpenAI (via Jina Reader, contourne Cloudflare) |
| `reddit` | r/MachineLearning + r/LocalLLaMA + r/agents |
| `langchain` | RSS du blog LangChain |
| `github_watch` | Releases des dépôts suivis (openclaw, opencode…) |
| `openclaw` | RSS du blog OpenClaw |
| `clawhub` | Dernières mises à jour des skills ClawHub |
| `devto` | Articles IA de DEV Community (tag:ai, plus réactionnés) |

**Étape 0 — Détection du profil projet** : détecte automatiquement le répertoire du projet courant et charge un profil de contenu correspondant. Profils intégrés :

| Projet | Axe | Sources boostées |
|--------|-----|-----------------|
| `cc_manager` | Claude Code harness, orchestration d'agents, MCP, conception d'outils | anthropic, hn, github, langchain, clawhub |
| `thinking_of_memory` | Articles académiques, méthodes d'analyse de données, modélisation statistique | arxiv, hf, reddit |

Des profils personnalisés peuvent être ajoutés dans `~/.claude/news-digest-profiles.json` :
```json
{
  "my_project": {
    "display": "my-project",
    "focus": "description du domaine d'intérêt",
    "extra_keywords": ["keyword1", "keyword2"],
    "preferred_sources": ["arxiv", "hn"],
    "learner_instruction": "Comment news-learner doit orienter son analyse pour ce projet..."
  }
}
```

Si aucun profil ne correspond, le mode par défaut est utilisé sans biais de filtrage.

**Étape 2 — Filtrage & déduplication** par mot-clé, autorité de source et similarité de titre. Les mots-clés et pondérations de sources du profil sont appliqués ici. Si plus de 3 sources ne retournent pas de données, un avertissement de défaillance partielle `[Diagnostic]` est affiché en haut ; si plus de 50% échouent, une alerte `⚠️ [Avertissement critique]` est affichée avec des étapes de dépannage.

**Étape 3 — Affichage** d'un digest CLI structuré :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI News Digest  |  2026-03-22  |  23 éléments
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Hacker News
1. [Titre]
   Résumé · lien

### HuggingFace Daily Papers
1. [Titre de l'article]
   Extrait du résumé · lien
...

Sources : hn arxiv hf github anthropic  |  Échecs : openai  |  Filtrés par : agent mcp
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Étape 4 — Couche d'apprentissage** (optionnel, ~60–80 s) : l'agent `news-learner` analyse les éléments pertinents pour votre workflow IA, les compare à vos skills/agents/patterns Claude Code existants et produit des recommandations priorisées :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Opportunités d'apprentissage  |  2 éléments analysés
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Adopt] Outil X — vrai manque dans notre couche d'orchestration
  → Étape 1 : créer un nouveau skill basé sur cette conception
  → lien : https://...

[Learn] Framework Y — recouvre le pattern existant Z
  → archivé dans ~/.claude/projects/<project>/memory/tech-watch.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Niveaux de recommandation : `[Priority Adopt]` → `[Adopt]` → `[Learn]` → `[Skip]`

- **`[Adopt]` / `[Priority Adopt]`** : une invite de décision interactive apparaît ; entrer un numéro pour agir, `s N` pour ignorer, `w N` pour dégrader vers `[Learn]`
- **`[Learn]`** : dédupliqué par URL et archivé dans `tech-watch.md` dans le répertoire mémoire du projet courant
- **`[Skip]`** : noté en session, aucun fichier écrit

---

## Installation

### Option A — Plugin Claude Code (recommandé)

```
/plugin marketplace update news-digest
/plugin install news-digest@news-digest
```

> Première utilisation ? Ajoutez d'abord la place de marché :
> ```
> /plugin marketplace add easyfan/news-digest
> /plugin install news-digest@news-digest
> ```

> ⚠️ **Partiellement couvert par des tests automatisés** : Le chemin CLI sous-jacent `claude plugin install` est vérifié par looper T2b (Plan B). Le point d'entrée REPL `/plugin` (interface interactive) ne peut pas être testé via `claude -p` et doit être vérifié manuellement dans une session Claude Code.

> **En cas d'erreur `ENAMETOOLONG`**, le cache du plugin est corrompu par un bug du runtime CC. Réparer avec :
> ```bash
> git clone https://github.com/easyfan/news-digest && cd news-digest && bash install.sh
> ```
> L'installeur détecte et répare automatiquement le cache corrompu.


### Option B — Script d'installation

```bash
# macOS / Linux
git clone https://github.com/easyfan/news-digest
cd news-digest
./install.sh

# Windows
.\install.ps1
```

```bash
# Options
./install.sh --dry-run      # prévisualiser les changements sans écrire
./install.sh --uninstall    # supprimer les fichiers installés
CLAUDE_DIR=/custom ./install.sh   # chemin de configuration Claude personnalisé
```

> ✅ **Vérifié** : couvert par le pipeline skill-test (looper Stage 5).

### Option C — Manuel

```bash
cp commands/news-digest.md ~/.claude/commands/
cp agents/news-learner.md  ~/.claude/agents/
```

> ✅ **Vérifié** : couvert par le pipeline skill-test (looper Stage 5).

---

## Utilisation

```
/news-digest [topics...] [--sources LISTE] [--limit N] [--no-learn]
```

| Argument | Description | Défaut |
|----------|-------------|--------|
| `topics` | Filtre par mot-clé — séparé par espaces, logique OU | tous les éléments |
| `--sources` | IDs de sources séparés par virgules (voir tableau ci-dessus) | les 11 sources |
| `--limit N` | Nombre max d'éléments par source | 5 |
| `--no-learn` | Ignorer la couche d'apprentissage, afficher uniquement les actualités (~60–80 s économisées) | désactivé |
| `--mode=cron` | Mode batch non-interactif : récupérer, résumer, écrire dans le log puis quitter sans invite | désactivé |
| `--channel` | Canal de sortie (`cli` disponible ; `slack`/`email`/`file` prévu) | `cli` |

**Exemples :**

```bash
/news-digest                             # exécution complète, toutes les sources
/news-digest --no-learn                  # rapide — actualités uniquement, pas d'agent
/news-digest llm agent mcp               # filtre par mot-clé
/news-digest --sources hn,arxiv,hf       # trois sources seulement
/news-digest --sources github --limit 10 # GitHub Trending top 10
/news-digest mcp --sources anthropic,openai  # deux sources officielles, filtre MCP
```

---

## Fichiers installés

```
~/.claude/
├── commands/
│   ├── news-digest.md          # commande slash /news-digest
│   ├── DESIGN.md               # configuration des sources et notes de conception
│   └── scripts/
│       ├── detect_project_profile.py
│       ├── parse_arguments.py
│       ├── fetch_sources.sh
│       ├── parse_items.py
│       ├── filter_items.py
│       ├── archive_learn.py
│       ├── scan_platform.sh
│       ├── fetch_full_content.sh
│       └── write_tech_watch.py
├── agents/
│   └── news-learner.md         # agent couche d'apprentissage (appelé automatiquement)
└── skills/
    └── news-digest/
        └── SKILL.md            # définition du skill (utilisée par looper T3)
```

### Structure du paquet

```
news-digest/
├── .claude-plugin/
│   ├── plugin.json         # manifeste plugin CC
│   └── marketplace.json    # entrée place de marché
├── commands/news-digest.md
├── agents/news-learner.md
├── skills/news-digest/
│   └── SKILL.md
├── evals/evals.json
├── install.sh
├── install.ps1
└── package.json
```

---

## Prérequis

- **Claude Code** CLI
- **curl** (système)
- **python3** (système) — utilisé pour le parsing JSON/XML dans les scripts inline
- Aucune autre dépendance

---

## Architecture

Chaque invocation génère un token `ND_SESSION` unique ; tous les fichiers IPC `/tmp` sont isolés sous `/tmp/nd_{session}_*` — les exécutions simultanées de `/news-digest` ne peuvent pas interférer.

```
/news-digest (coordinateur de commande)
│
├── Étape 0 : générer ND_SESSION → Bash — détecter le profil projet → /tmp/nd_{session}_profile.json
│           analyser les args → /tmp/nd_{session}_params.json (topics, sources, limit, no_learn)
├── Étape 1 : Sortir bannière de démarrage (temps est.) → Bash : curl toutes sources → /tmp/nd_{session}_*.{json,xml,html}
├── Étape 2 : Bash — heredoc Python : parser → filtrer → dédupliquer → tag de pertinence
│           extra_keywords du profil fusionnés dans RELEVANT_KW
│           preferred_sources du profil reçoivent +2 de poids SOURCE_RANK
│           écrit /tmp/nd_{session}_deduped.json + /tmp/nd_{session}_relevant.json
│           (⚠️ alerte si >50% sources échouent ; [Diagnostic] si >3 échouent)
├── Étape 3 : Afficher le digest CLI formaté
│
└── Étape 4 (si des éléments pertinents existent et --no-learn non défini) :
    └── news-learner (agent) ← reçoit relevant_items_path, project_profile, learner_instruction
        ├── [Étape 1/4] Lit les descriptions ~/.claude/ pour inventorier les capacités de la plateforme
        ├── [Étape 2/4] Lit l'historique tech-watch.md (si existant) ; récupère le contenu via curl
        ├── [Étape 3/4] Analyse chaque élément selon le prisme du profil : problème → manque → niveau de recommandation
        ├── [Étape 4/4] Écrit les éléments [Learn] → tech-watch.md (dédupliqué par URL)
        └── Retourne l'invite de décision interactive pour les éléments [Adopt]+
```

---

## Exemple concret : De la veille à une nouvelle capacité

Un vrai cycle d'adoption du 2026-03-24, illustrant le workflow complet `/news-digest` → `news-learner` → décision immédiate.

### Ce qui l'a déclenché

En exécutant `/news-digest` sans filtres, la couche d'apprentissage a détecté un élément de niveau `[Adopt]` :

> **"How we monitor internal coding agents for misalignment"** — OpenAI Engineering Blog
> *Un framework de surveillance comportementale à l'exécution pour les agents de code : détection d'évasion, contrôles de débordement de portée, détection d'anomalies de permissions, mesure de dérive d'intention.*

`news-learner` l'a comparé aux capacités existantes de la plateforme et a trouvé un **vrai manque** :

```
Capacité principale : surveillance comportementale d'agent à l'exécution — détecter dérive d'intention et évasion
État actuel :   skill-review ne fait qu'une analyse statique des définitions ; pas de surveillance à l'exécution
Recommandation : [Adopt]
Plan d'adoption :
  1. Créer l'agent agent-monitor : lire la trace de tâche, vérifier contre la checklist à quatre signaux
  2. Créer le pattern agent-monitoring : guide les coordinateurs pour déclencher la surveillance après des tâches à risque élevé
```

L'invite de décision est apparue à la fin du digest :

```
⚡ Action requise (1 élément) :

  1. [Adopt] How we monitor internal coding agents for misalignment
     Plan : créer l'agent agent-monitor, lire la trace de tâche, détecter dérive d'intention et évasion

Entrer 1 pour agir maintenant, s 1 pour ignorer, w 1 pour dégrader vers [Learn]
```

### Ce qui a été construit (l'utilisateur a tapé `1`)

Trois fichiers créés dans la même session :

**`~/.claude/agents/agent-monitor.md`** — lit le fichier de trace d'une tâche terminée et vérifie quatre catégories de signaux (évasion, débordement de portée, anomalie de permissions, dérive d'intention), écrit des alertes graduées dans `memory/agent-alerts.md` :

| Grade | Signification | Action du coordinateur |
|-------|--------------|----------------------|
| ✅ CLEAN | Normal | Continuer |
| ⚠️ WATCH | Signal mineur, possible faux positif | Journaliser, suivre la tendance |
| 🚨 ALERT | Signal à haut risque | Mettre en pause, notifier l'utilisateur |
| 🛑 BLOCK | Indicateurs malveillants confirmés | Arrêter + rollback |

**`~/.claude/patterns/agent-monitoring.md`** — guide du coordinateur : quelles tâches nécessitent une surveillance post-exécution et comment invoquer `agent-monitor`.

**`~/.claude/hooks/post_bash_error.sh`** — écouteur passif qui se déclenche à chaque échec d'appel Bash, écrit des entrées d'erreur structurées dans `memory/errors.md` et signale les patterns à haut risque (curl hors liste blanche, `rm -rf`, force-push, lectures de fichiers sensibles) dans `memory/agent-alerts.md`.

### Pourquoi c'est important

La boucle complète — découverte → analyse du manque → décision → construction — s'est terminée en une seule session. `news-learner` a identifié une capacité que la plateforme n'avait vraiment pas (surveillance à l'exécution vs. analyse statique), et le nouvel agent était opérationnel dès que l'utilisateur a tapé `1`.

C'est le workflow prévu : `/news-digest` fait remonter ce qui mérite d'être connu ; `news-learner` le mappe à vos manques réels ; l'invite de décision rend l'adoption sans friction.

---

## Exemple réel : mise à niveau de version de modèle découverte lors des tests de pipeline

Un second cas réel du 2026-04-05, survenu lors de `/skill-test packer/news-digest` à l'étape 3 d'évaluation comportementale — montrant comment `news-learner` détecte une publication pertinente pour la plateforme et émet une recommandation de mise à niveau concrète.

### Ce qui l'a déclenché

Durant l'exécution de l'évaluation de l'étape 3, `/news-digest` a récupéré la source d'actualités officielle d'Anthropic et obtenu :

> **« claude-sonnet-4.6 désormais disponible »** — Actualités officielles Anthropic
> *Anthropic a publié claude-sonnet-4.6 (ID de modèle : `claude-sonnet-4-6`), la dernière génération Sonnet avec un meilleur raisonnement et une meilleure utilisation des outils. La génération précédente claude-sonnet-4.5 reste disponible, mais n'est plus la version par défaut recommandée pour les nouveaux déploiements.*

`news-learner` a analysé les agents et skills installés sur la plateforme et a trouvé des références `sonnet` codées en dur pointant vers la génération précédente :

```
Capacité principale : actualité de la version du modèle — agents/skills sur le dernier Sonnet recommandé
État actuel :  news-learner.md utilise `model: sonnet` (alias nu, résolu par le runtime CC ;
               non épinglé, sans documentation sur le caractère intentionnel)
Recommandation : [Adopt]
Plan d'adoption :
  1. Décision : épingler à un ID de version explicite ou conserver l'alias nu avec l'intention documentée
  2. Si épinglage : mettre à jour le champ model vers `claude-sonnet-4-6` dans les fichiers d'agents concernés
  3. Si conservation de l'alias : ajouter un commentaire confirmant le comportement flottant intentionnel
```

L'invite de décision est apparue à la fin du digest :

```
⚡ Action requise (1 élément) :

  1. [Adopt] claude-sonnet-4.6 publié — news-learner utilise encore l'alias nu `sonnet`
     Plan : épingler à claude-sonnet-4-6 ou documenter l'alias comme intentionnel

Entrer 1 pour agir maintenant, s 1 pour ignorer, w 1 pour déclasser
```

### Ce qui s'est passé (l'utilisateur a tapé `1`)

L'alias nu `model: sonnet` était un choix délibéré — CC le résout vers le dernier Sonnet à l'installation, permettant un « auto-upgrade » sans modifier les fichiers. La session a clarifié cette intention et l'a documentée en ligne :

```yaml
# agents/news-learner.md (frontmatter)
model: sonnet   # alias nu intentionnel — résolu vers le dernier Sonnet lors de l'installation CC
```

Aucun contenu de fichier n'a été modifié substantiellement ; la décision a été enregistrée comme un no-op délibéré avec justification.

### Pourquoi c'est important

Ce cas illustre une autre classe d'éléments `[Adopt]` : non pas un manque de capacité, mais une **décision de posture de maintenance**. `news-learner` a fait remonter la publication le jour même de sa sortie ; le propriétaire de la plateforme devait décider — épingler ou flotter — plutôt que de découvrir la dérive des semaines plus tard.

Le contexte du pipeline (étape 3 eval) a rendu ce signal plus pertinent qu'un simple digest ordinaire : le champ modèle de l'agent testé était directement impliqué, transformant une note de publication ambiante en un point de revue actionnable.

---

## Développement

### Evals

`evals/evals.json` contient 6 cas de test couvrant l'analyse des arguments, la récupération de données et la couche d'apprentissage :

| ID | Scénario | Ce qui est vérifié |
|----|----------|-------------------|
| 1 | `/news-digest` (exécution complète, pas d'args) | Récupère les 11 sources, affiche le digest, couche d'apprentissage s'exécute |
| 2 | `/news-digest --no-learn` | Ignore l'agent news-learner ; affiche uniquement le résumé des actualités |
| 3 | `/news-digest llm agent` (filtre par mot-clé) | Seuls les éléments avec `llm` ou `agent` dans titre/résumé sont affichés |
| 4 | `/news-digest --sources hn,hf --limit 3` | Récupère uniquement les sources spécifiées, max 3 éléments chacune |
| 5 | Chemin MCP/Jina (var. d'env. `JINA_API_KEY` présente) | L'outil Jina MCP est utilisé préférentiellement pour la récupération de contenu |
| 6 | ID de source invalide | Affiche un message d'erreur listant les IDs valides ; aucune récupération tentée |

Tests manuels (dans une session Claude Code) :
```bash
/news-digest --no-learn     # vérification rapide, eval 2
/news-digest llm            # filtre par mot-clé, eval 3
```

Exécuter tous les evals avec le eval loop de skill-creator (si installé) :
```bash
python ~/.claude/skills/skill-creator/scripts/run_loop.py \
  --skill-path ~/.claude/commands/news-digest.md \
  --evals-path evals/evals.json
```

---

## Licence

MIT
