# A Arquitetura de Automação de Redes

Referência de bolso do **Capítulo 5** do curso *Nornir: da Execução à
Arquitetura*. Este capítulo é conceitual — os diagramas abaixo são o "código"
dele. Guarde-os: eles são o mapa da Parte II inteira.

O recorte em camadas é um consenso da comunidade de automação de redes
(Network Automation Forum / AutoCon; livro *Network Automation Architecture*,
O'Reilly). Cada camada é definida por **responsabilidade**, não por produto —
por isso as ferramentas são substituíveis.

## As cinco camadas (arquitetura de referência)

- **User Interactions** — como se PEDE e se CONSOME automação.
- **Source of Truth (SoT)** — o estado DESEJADO da rede, modelado e versionado.
- **Automation Engine** — a execução: conecta e aplica. É onde o Nornir mora.
- **Orchestration** — QUANDO e em que ORDEM tudo roda.
- **Telemetry & Observability** — o estado REAL; vs. SoT = detecção de drift.

```text
   ┌───────────────────────────────────────────────────────────┐
   │  USER INTERACTIONS  —  como se PEDE e se CONSOME automação│
   │  formulários · dashboards · ChatOps · Merge Requests      │
   └─────────────────────────────┬─────────────────────────────┘
                                 │  "quero a VLAN 20 no site POA"
   ┌─────────────────────────────▼─────────────────────────────┐
   │  ORCHESTRATION  —  QUANDO e em que ORDEM tudo roda        │
   │  agenda · dispara · encadeia · retries · estado · eventos │
   └─────────────────────────────┬─────────────────────────────┘
                                 │  "rode este workflow agora"
   ┌────────────────┐   ┌────────▼───────┐   ┌─────────────────┐
   │ SOURCE OF TRUTH│──▶│  AUTOMATION    │   │  TELEMETRY &    │
   │ estado         │   │  ENGINE        │   │  OBSERVABILITY  │
   │ DESEJADO:      │   │  (execução)    │   │  estado REAL:   │
   │ devices, VLANs,│◀──│  conecta,      │   │  métricas,      │
   │ serviços —     │   │  renderiza,    │   │  logs, alertas  │
   │ versionado     │   │  aplica config │   │                 │
   │                │   │  >> NORNIR <<  │   │                 │
   └───────┬────────┘   └───────┬────────┘   └────────▲────────┘
           │                    │ aplica              │ lê o real
           │  compara           ▼                     │
           │  (desejado     ┌───────────────────────────────────┐
           └── × real) ────▶│          A REDE REAL              │
                = DRIFT     │  r1..r4 · eos1..eos2 · f5 · ...   │
                            └────────────────────┬──────────────┘
                                                 └── alimenta a telemetria

```

## O stack deste curso (camada -> ferramenta -> capítulo)

```text
  CAMADA (arquitetura)      FERRAMENTA no curso         ONDE você aprende
  ─────────────────────────────────────────────────────────────────────────
  User Interactions    →    GitLab (Merge Requests)  →  Cap. 7  (GitOps)
                            Infrahub UI (formulários)    Cap. 6
  Orchestration        →    Prefect                  →  Cap. 8
  Source of Truth      →    Infrahub                 →  Cap. 6
  Automation Engine    →    Nornir  (toda a Parte I) →  Cap. 1–4   ✓ feito
  Telemetry & Observ.  →    (fora do escopo v1)      →  —  (ponteiro)
  ─────────────────────────────────────────────────────────────────────────
  A REDE               →    r1..r4 · eos1..eos2 · f5 →  o lab, desde o Cap. 1

```

## O mapa do curso (o fluxo que o capstone percorre)

```text
  Você abre um Merge Request  ───────────────────────────────  [Cap. 7]
        │
        ▼
  Infrahub   define o estado desejado (branch + proposed change) [Cap. 6]
        │
        ▼
  GitLab CI  lint · pytest · dry-run/diff · portão de aprovação  [Cap. 7]
        │
        ▼
  Prefect    agenda, dispara, retry, observabilidade da execução [Cap. 8]
        │
        ▼
  Nornir     conecta e aplica config nos devices (execução)      [Parte I ✓]
        │
        ▼
  A REDE     r1..r4 · eos1..eos2 · f5                            [o lab]
        │
        └──▶ post-checks / conformidade ──▶ drift de volta ao SoT [Cap. 9]

```

## O que este curso NÃO cobre

- Três famílias de plataforma no núcleo (IOS-XE, EOS, F5; VyOS numa aula do Cap. 9).
- Sem observabilidade profunda (nada de streaming telemetry / Prometheus / Grafana).
- Sem multi-region / HA dos serviços (Infrahub, GitLab, Prefect single-node no lab).
- Segurança no básico: credenciais em env vars, segredos fora do Git.
