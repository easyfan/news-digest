[English](README.md) | [中文](README-CN.md) | [Deutsch](README-de.md) | [Français](README-fr.md) | [Русский](README-ru.md)

# news-digest

Mehrquelliger KI-Nachrichten-Digest für Claude Code — ruft die neuesten KI-Technologienachrichten aus 12 Quellen ab, fasst sie zusammen und lernt daraus.

```
/news-digest                    # Vollständiger Digest + Lernebene
/news-digest --no-learn         # Nur Nachrichten (Schnellmodus)
/news-digest llm agent          # Nach Stichwort filtern
/news-digest --sources hn,hf    # Nur bestimmte Quellen
```

---

## Funktionsweise

**Schritt 1 — Benachrichtigung & Abruf**: Gibt ein Banner mit geschätzter Dauer aus (20–40 s für Nachrichten, +60–80 s mit Lernebene) und ruft dann in einem einzigen Bash-Aufruf aus 12 Quellen ab:

| Quelle | Inhalt |
|--------|--------|
| `hn` | Hacker News Startseite |
| `arxiv` | arXiv cs.AI neueste Paper |
| `hf` | HuggingFace Daily Papers (kuratierte KI) |
| `github` | GitHub Trending Repositories |
| `anthropic` | Anthropic offizielle Neuigkeiten |
| `openai` | OpenAI Neuigkeiten (via Jina Reader, umgeht Cloudflare) |
| `reddit` | r/MachineLearning + r/LocalLLaMA + r/agents |
| `langchain` | LangChain Blog RSS |
| `github_watch` | Verfolgte Repo-Releases (openclaw, opencode …) |
| `openclaw` | OpenClaw Blog RSS |
| `clawhub` | ClawHub neueste Skill-Updates |
| `devto` | DEV Community KI-Artikel (tag:ai, meistgereagiert) |

**Schritt 0 — Projektprofilerkennung**: Erkennt automatisch das aktuelle Projektverzeichnis und lädt das passende Inhaltsprofil. Integrierte Profile:

| Projekt | Schwerpunkt | Höher gewichtete Quellen |
|---------|------------|--------------------------|
| `cc_manager` | Claude Code Harness, Agent-Orchestrierung, MCP, Tool-Design | anthropic, hn, github, langchain, clawhub |
| `thinking_of_memory` | Wissenschaftliche Paper, Datenanalyse, statistische Modellierung | arxiv, hf, reddit |

Eigene Profile in `~/.claude/news-digest-profiles.json` ergänzbar. Ohne passendes Profil läuft der Standardmodus ohne Filterbias.

**Schritt 2 — Filtern & Deduplizieren** nach Stichwort, Quellengewichtung und Titelähnlichkeit. Profil-Keywords und Quellengewichtungen werden hier angewendet. Wenn mehr als 3 Quellen keine Daten liefern, erscheint oben eine `[Diagnose]`-Teilausfallwarnung; wenn mehr als 50% ausfallen, ein `⚠️ [Kritische Warnung]`-Alert mit Fehlerbehebungsschritten.

**Schritt 3 — Ausgabe** eines strukturierten CLI-Digests:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI News Digest  |  2026-03-22  |  23 Einträge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Hacker News
1. [Titel]
   Zusammenfassung · Link

### HuggingFace Daily Papers
1. [Paper-Titel]
   Kurzauszug · Link
...

Quellen: hn arxiv hf github anthropic  |  Fehlgeschlagen: openai  |  Filter: agent mcp
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Schritt 4 — Lernebene** (optional, ca. 60–80 s): Der `news-learner`-Agent analysiert für Ihren KI-Workflow relevante Einträge, vergleicht sie mit den vorhandenen Claude Code Skills/Agents/Patterns und gibt priorisierte Empfehlungen aus:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Lernmöglichkeiten  |  2 Einträge analysiert
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Adopt] Tool X — echte Lücke in unserer Orchestrierungsebene
  → Schritt 1: neuen Skill basierend auf diesem Design erstellen
  → Link: https://...

[Learn] Framework Y — überschneidet sich mit bestehendem Muster Z
  → archiviert in ~/.claude/projects/<project>/memory/tech-watch.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Empfehlungsstufen: `[Priority Adopt]` → `[Adopt]` → `[Learn]` → `[Skip]`

- **`[Adopt]` / `[Priority Adopt]`**: interaktive Entscheidungsaufforderung erscheint; Nummer eingeben zum Ausführen, `s N` zum Überspringen, `w N` zum Herabstufen auf `[Learn]`
- **`[Learn]`**: URL-dedupliziert und in `tech-watch.md` im Memory-Verzeichnis des aktuellen Projekts archiviert
- **`[Skip]`**: in der Sitzung vermerkt, keine Datei geschrieben

---

## Installation

### Option A — Claude Code Plugin (empfohlen)

```
/plugin marketplace update news-digest
/plugin install news-digest@news-digest
```

> Erstmalige Nutzung? Marketplace zuerst hinzufügen:
> ```
> /plugin marketplace add easyfan/news-digest
> /plugin install news-digest@news-digest
> ```

> ⚠️ **Teilweise durch automatisierte Tests abgedeckt**: Der zugrunde liegende `claude plugin install` CLI-Pfad wird durch looper T2b (Plan B) verifiziert. Der `/plugin` REPL-Einstiegspunkt (interaktive UI) kann nicht via `claude -p` getestet werden und muss manuell in einer Claude Code-Sitzung überprüft werden.

> **Bei `ENAMETOOLONG`-Fehlern** ist der Plugin-Cache durch einen CC-Runtime-Bug beschädigt. Reparatur:
> ```bash
> git clone https://github.com/easyfan/news-digest && cd news-digest && bash install.sh
> ```
> Der Installer erkennt und repariert den beschädigten Cache automatisch.


### Option B — Installationsskript

```bash
# macOS / Linux
git clone https://github.com/easyfan/news-digest
cd news-digest
./install.sh

# Windows
.\install.ps1
```

```bash
# Optionen
./install.sh --dry-run      # Vorschau der Änderungen ohne Schreiben
./install.sh --uninstall    # installierte Dateien entfernen
CLAUDE_DIR=/custom ./install.sh   # benutzerdefinierter Claude-Konfigurationspfad
```

> ✅ **Verifiziert**: durch die skill-test-Pipeline (looper Stage 5) abgedeckt.

### Option C — Manuell

```bash
cp commands/news-digest.md ~/.claude/commands/
cp agents/news-learner.md  ~/.claude/agents/
```

> ✅ **Verifiziert**: durch die skill-test-Pipeline (looper Stage 5) abgedeckt.

---

## Verwendung

```
/news-digest [topics...] [--sources LISTE] [--limit N] [--no-learn]
```

| Argument | Beschreibung | Standard |
|----------|-------------|---------|
| `topics` | Stichwortfilter — leerzeichen-getrennt, ODER-Logik | alle Einträge |
| `--sources` | Komma-getrennte Quell-IDs (siehe Tabelle oben) | alle 11 Quellen |
| `--limit N` | Max. Einträge pro Quelle | 5 |
| `--no-learn` | Lernebene überspringen, nur Nachrichten ausgeben (ca. 60–80 s gespart) | aus |
| `--mode=cron` | Nicht-interaktiver Batch-Modus: abrufen, zusammenfassen, in Log schreiben und ohne Eingabeaufforderungen beenden | aus |
| `--channel` | Ausgabekanal (`cli` derzeit verfügbar; `slack`/`email`/`file` geplant) | `cli` |

**Beispiele:**

```bash
/news-digest                             # vollständiger Lauf, alle Quellen
/news-digest --no-learn                  # schnell — nur Nachrichten, kein Agent
/news-digest llm agent mcp               # Stichwortfilter
/news-digest --sources hn,arxiv,hf       # drei Quellen
/news-digest --sources github --limit 10 # GitHub Trending Top 10
/news-digest mcp --sources anthropic,openai  # zwei offizielle Quellen, MCP-Filter
```

---

## Installierte Dateien

```
~/.claude/
├── commands/
│   ├── news-digest.md          # /news-digest Slash-Befehl
│   ├── DESIGN.md               # Datenquellen-Konfiguration und Designnotizen
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
│   └── news-learner.md         # Lernebene-Agent (wird automatisch aufgerufen)
└── skills/
    └── news-digest/
        └── SKILL.md            # Skill-Definition (für looper T3-Triggertest)
```

### Paketstruktur

```
news-digest/
├── .claude-plugin/
│   ├── plugin.json         # CC-Plugin-Manifest
│   └── marketplace.json    # Marketplace-Eintrag
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

## Voraussetzungen

- **Claude Code** CLI
- **curl** (System)
- **python3** (System) — für JSON/XML-Parsing in Inline-Skripten
- Keine weiteren Abhängigkeiten

---

## Architektur

Jeder Aufruf erzeugt ein eindeutiges `ND_SESSION`-Token; alle `/tmp`-IPC-Dateien werden als `/tmp/nd_{session}_*` isoliert — gleichzeitige `/news-digest`-Aufrufe können sich gegenseitig nicht stören.

```
/news-digest (Befehlskoordinator)
│
├── Schritt 0: ND_SESSION erzeugen → Bash — Projektprofil erkennen → /tmp/nd_{session}_profile.json
│           Parameter parsen → /tmp/nd_{session}_params.json (topics, sources, limit, no_learn)
├── Schritt 1: Startbanner ausgeben (gesch. Zeit) → Bash: curl alle Quellen → /tmp/nd_{session}_*.{json,xml,html}
├── Schritt 2: Bash — Python-Heredoc: parsen → filtern → deduplizieren → Relevanz-Tag
│           schreibt /tmp/nd_{session}_deduped.json + /tmp/nd_{session}_relevant.json
│           (⚠️ Alert wenn >50% Quellen fehlschlugen; [Diagnose] wenn >3 fehlschlugen)
├── Schritt 3: Formatierten CLI-Digest ausgeben
│
└── Schritt 4 (wenn relevante Einträge vorhanden und --no-learn nicht gesetzt):
    └── news-learner (Agent) ← empfängt relevant_items_path, project_profile, learner_instruction
        ├── [Schritt 1/4] ~/.claude/-Beschreibungen lesen, Plattformfähigkeiten inventarisieren
        ├── [Schritt 2/4] tech-watch.md-Verlauf lesen (falls vorhanden); Inhalt via curl abrufen
        ├── [Schritt 3/4] Jeden Eintrag analysieren: Problem → Lücke → Empfehlungsstufe
        ├── [Schritt 4/4] [Learn]-Einträge → tech-watch.md schreiben (URL-dedupliziert)
        └── Interaktive Entscheidungsaufforderung für [Adopt]+-Einträge zurückgeben
```

---

## Praxisbeispiel: Von Nachrichten zu neuer Fähigkeit

Ein realer Adoptionszyklus vom 2026-03-24, der den vollständigen `/news-digest` → `news-learner` → sofortige Entscheidungs-Workflow zeigt.

### Auslöser

Bei einem Lauf von `/news-digest` ohne Filter erkannte die Lernebene einen `[Adopt]`-Eintrag:

> **"How we monitor internal coding agents for misalignment"** — OpenAI Engineering Blog
> *Ein Laufzeit-Verhaltensüberwachungsframework für Coding-Agents: Erkennung von Ausweichverhalten, Scope-Überlauf-Checks, Berechtigungsanomalien-Erkennung, Intent-Drift-Messung.*

`news-learner` verglich es mit den vorhandenen Plattformfähigkeiten und fand eine **echte Lücke**:

```
Kernfähigkeit: Laufzeit-Agent-Verhaltensüberwachung — Intent-Drift und Ausweichen erkennen
Aktueller Stand:   skill-review macht nur statische Definitionsanalyse; keine Laufzeitüberwachung
Empfehlung:  [Adopt]
Adoptionsplan:
  1. agent-monitor-Agent erstellen: Task-Trace lesen, gegen Vier-Signal-Checkliste prüfen
  2. agent-monitoring-Pattern erstellen: leitet Koordinatoren an, Überwachung nach Hochrisiko-Tasks auszulösen
```

Am Ende des Digests erschien die Entscheidungsaufforderung:

```
⚡ Aktion erforderlich (1 Eintrag):

  1. [Adopt] How we monitor internal coding agents for misalignment
     Plan: agent-monitor-Agent erstellen, Task-Trace lesen, Intent-Drift und Ausweichen erkennen

1 eingeben zum sofortigen Handeln, s 1 zum Überspringen, w 1 zum Herabstufen auf [Learn]
```

### Was gebaut wurde (Benutzer tippte `1`)

Drei Dateien in derselben Sitzung erstellt:

**`~/.claude/agents/agent-monitor.md`** — liest die Trace-Datei einer abgeschlossenen Aufgabe und prüft vier Signalkategorien (Ausweichen, Scope-Überlauf, Berechtigungsanomalie, Intent-Drift), schreibt nach Schweregrad gestufte Alerts in `memory/agent-alerts.md`:

| Stufe | Bedeutung | Koordinatoraktion |
|-------|-----------|-------------------|
| ✅ CLEAN | Normal | Weiter |
| ⚠️ WATCH | Kleineres Signal, mögliches Falsch-Positiv | Protokollieren, Trend verfolgen |
| 🚨 ALERT | Hochrisiko-Signal | Pausieren, Benutzer benachrichtigen |
| 🛑 BLOCK | Bestätigte bösartige Indikatoren | Stoppen + Rollback |

**`~/.claude/patterns/agent-monitoring.md`** — Koordinatorleitfaden: welche Aufgaben eine Überwachung nach dem Lauf erfordern und wie `agent-monitor` aufgerufen wird.

**`~/.claude/hooks/post_bash_error.sh`** — passiver Listener, der bei jedem fehlgeschlagenen Bash-Aufruf ausgelöst wird, strukturierte Fehlereinträge in `memory/errors.md` schreibt und Hochrisiko-Muster (nicht-Whitelist-curl, `rm -rf`, Force-Push, sensible Datei-Lesezugriffe) in `memory/agent-alerts.md` markiert.

### Warum das wichtig ist

Die vollständige Schleife — Entdecken → Lücke analysieren → Entscheiden → Bauen — wurde in einer Sitzung abgeschlossen. `news-learner` identifizierte eine Fähigkeit, die der Plattform wirklich fehlte (Laufzeitüberwachung vs. statische Analyse), und der neue Agent war einsatzbereit, sobald der Benutzer `1` eingab.

Das ist der beabsichtigte Workflow: `/news-digest` bringt hervor, was wissenswert ist; `news-learner` ordnet es Ihren tatsächlichen Lücken zu; die Entscheidungsaufforderung macht Adoption reibungslos.

---

## Praxisbeispiel: Modellversions-Upgrade während Pipeline-Test entdeckt

Ein zweiter Realfall vom 2026-04-05, der während `/skill-test packer/news-digest` Stage 3 Verhaltensevaluation auftrat — zeigt, wie `news-learner` eine plattformrelevante Veröffentlichung im Digest aufgreift und eine konkrete Upgrade-Empfehlung ausspricht.

### Was es auslöste

Während des Stage-3-Eval-Durchlaufs rief `/news-digest` die offizielle Anthropic-Nachrichtenquelle ab und erhielt:

> **„claude-sonnet-4.6 jetzt verfügbar"** — Anthropic offizielle Neuigkeiten
> *Anthropic veröffentlichte claude-sonnet-4.6 (Model-ID: `claude-sonnet-4-6`), die neueste Sonnet-Generation mit verbessertem Reasoning und Tool-Use. Die vorherige Generation claude-sonnet-4.5 bleibt verfügbar, ist aber nicht mehr die empfohlene Standardversion für neue Deployments.*

`news-learner` scannte die installierten Agents und Skills der Plattform und fand hartcodierte `sonnet`-Referenzen auf die vorherige Generation:

```
Kernfähigkeit: Modellversions-Aktualität — ob Agents/Skills das neueste empfohlene Sonnet nutzen
Aktueller Stand: news-learner.md verwendet `model: sonnet` (blankes Alias, vom CC-Runtime aufgelöst;
                 keine Versionsverankerung, keine Dokumentation ob bewusst gewählt)
Empfehlung:  [Adopt]
Umsetzungsplan:
  1. Entscheidung: auf explizite Versions-ID pinnen oder blankes Alias mit dokumentierter Absicht behalten
  2. Bei Pinning: model-Feld in betroffenen Agent-Dateien auf `claude-sonnet-4-6` aktualisieren
  3. Bei Beibehaltung des Alias: Kommentar hinzufügen, der das bewusste Floating-Verhalten bestätigt
```

Am Ende des Digests erschien die Entscheidungsaufforderung:

```
⚡ Sofortige Entscheidung erforderlich (1 Eintrag):

  1. [Adopt] claude-sonnet-4.6 veröffentlicht — news-learner verwendet noch blankes `sonnet`-Alias
     Plan: auf claude-sonnet-4-6 pinnen oder Alias als bewusst dokumentieren

1 eingeben zum sofortigen Handeln, s 1 zum Überspringen, w 1 zum Herabstufen
```

### Was passierte (Benutzer tippte `1`)

Das blanke Alias `model: sonnet` war eine bewusste Entscheidung — CC löst es bei der Installation auf das neueste Sonnet auf, sodass ein „Auto-Upgrade" ohne Dateiänderungen erfolgt. Die Sitzung klärte diese Absicht und dokumentierte sie inline:

```yaml
# agents/news-learner.md (Frontmatter)
model: sonnet   # bewusstes blankes Alias — wird bei CC-Installation auf neuestes Sonnet aufgelöst
```

Kein Dateiinhalt wurde wesentlich geändert; die Entscheidung wurde als bewusstes No-op mit Begründung festgehalten.

### Warum das wichtig ist

Dieser Fall zeigt eine andere Klasse von `[Adopt]`-Einträgen: keine Fähigkeitslücke, sondern eine **Wartungspositionsentscheidung**. `news-learner` hat die Veröffentlichung am Tag ihres Erscheinens aufgegriffen; der Plattformbetreiber musste sich entscheiden — pinnen oder floating — anstatt den Drift Wochen später passiv zu entdecken.

Der Pipeline-Kontext (Stage 3 Eval) erhöhte den Signalwert über einen gewöhnlichen Digest-Lauf hinaus: Das Modellfeld des getesteten Agents war direkt betroffen und verwandelte eine beiläufige Release-Meldung in einen handlungsrelevanten Review-Punkt.

---

## Entwicklung

### Evals

`evals/evals.json` enthält 6 Testfälle zu Argument-Parsing, Datenabruf und Lernebene:

| ID | Szenario | Was verifiziert wird |
|----|----------|---------------------|
| 1 | `/news-digest` (vollständiger Lauf, keine Args) | Ruft alle 11 Quellen ab, gibt Digest aus, Lernebene wird ausgeführt |
| 2 | `/news-digest --no-learn` | Überspringt den news-learner-Agent; gibt nur die Nachrichtenzusammenfassung aus |
| 3 | `/news-digest llm agent` (Stichwortfilter) | Nur Einträge, bei denen `llm` oder `agent` in Titel/Zusammenfassung vorkommt |
| 4 | `/news-digest --sources hn,hf --limit 3` | Ruft nur angegebene Quellen ab, max. 3 Einträge je |
| 5 | MCP/Jina-Pfad (`JINA_API_KEY` Env-Var vorhanden) | Jina-MCP-Tool wird bevorzugt für Content-Abruf verwendet |
| 6 | Ungültige Quell-ID | Gibt Fehlermeldung mit gültigen Quell-IDs aus; kein Abruf |

Manuelles Testen (in einer Claude Code-Sitzung):
```bash
/news-digest --no-learn     # schnelle Verifikation, Eval 2
/news-digest llm            # Stichwortfilter, Eval 3
```

Alle Evals mit dem Eval-Loop von skill-creator ausführen (falls installiert):
```bash
python ~/.claude/skills/skill-creator/scripts/run_loop.py \
  --skill-path ~/.claude/commands/news-digest.md \
  --evals-path evals/evals.json
```

---

## Lizenz

MIT
