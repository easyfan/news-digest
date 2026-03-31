[English](README.md) | [中文](README-CN.md) | [Deutsch](README-de.md) | [Français](README-fr.md) | [Русский](README-ru.md)

# news-digest

Digest d'actualités IA multi-sources pour Claude Code — récupère, résume et apprend des dernières actualités technologiques IA provenant de 11 sources.

```
/news-digest                    # digest complet + couche d'apprentissage
/news-digest --no-learn         # actualités uniquement (mode rapide)
/news-digest llm agent          # filtrer par mot-clé
/news-digest --sources hn,hf    # sources spécifiques uniquement
```

---

## Fonctionnement

**Étape 1 — Notification & récupération** : affiche une bannière avec le temps estimé (20–40 s pour les actualités, +60–80 s avec la couche d'apprentissage) puis récupère depuis 11 sources en un seul appel Bash :

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

**Étape 2 — Filtrage & déduplication** par mot-clé, autorité de source et similarité de titre. Si plus de 3 sources ne retournent pas de données, un avertissement de défaillance partielle `[Diagnostic]` est affiché en haut ; si plus de 50% échouent, une alerte `⚠️ [Avertissement critique]` est affichée avec des étapes de dépannage.

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

> ⚠️ **Non vérifié par des tests automatisés** : `/plugin` est un built-in REPL Claude Code et ne peut pas être invoqué via `claude -p`. À exécuter manuellement dans une session Claude Code ; non couvert par le pipeline skill-test (looper Stage 5).

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
│   └── news-digest.md    # commande slash /news-digest
└── agents/
    └── news-learner.md   # agent couche d'apprentissage (appelé automatiquement)
```

### Structure du paquet

```
news-digest/
├── .claude-plugin/
│   ├── plugin.json         # manifeste plugin CC
│   └── marketplace.json    # entrée place de marché
├── commands/news-digest.md
├── agents/news-learner.md
├── evals/evals.json
├── install.sh
├── install.ps1
└── SKILL.md
```

---

## Prérequis

- **Claude Code** CLI
- **curl** (système)
- **python3** (système) — utilisé pour le parsing JSON/XML dans les scripts inline
- Aucune autre dépendance

---

## Architecture

```
/news-digest (coordinateur de commande)
│
├── Étape 0 : Bash — analyser les args → /tmp/nd_params.json (topics, sources, limit, no_learn)
├── Étape 1 : Sortir bannière de démarrage (temps est.) → Bash : curl toutes sources → /tmp/nd_*.{json,xml,html}
├── Étape 2 : Bash — heredoc Python : parser → filtrer → dédupliquer → tag de pertinence
│           écrit /tmp/nd_deduped.json + /tmp/nd_relevant.json
│           (⚠️ alerte si >50% sources échouent ; [Diagnostic] si >3 échouent)
├── Étape 3 : Afficher le digest CLI formaté
│
└── Étape 4 (si /tmp/nd_relevant.json non vide et --no-learn non défini) :
    └── news-learner (agent) ← reçoit relevant_items_path : /tmp/nd_relevant.json
        ├── [Étape 1/4] Lit les descriptions ~/.claude/ pour inventorier les capacités de la plateforme
        ├── [Étape 2/4] Lit l'historique tech-watch.md (si existant) ; récupère le contenu via curl
        ├── [Étape 3/4] Analyse chaque élément : problème → manque → niveau de recommandation
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
