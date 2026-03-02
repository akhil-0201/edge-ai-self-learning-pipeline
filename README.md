# Edge AI Continuous Self-Learning Pipeline

> **Platform:** Rockchip RK3588 (4 GB RAM · 10 GB Storage)  
> **Model:** PyTorch YOLOv8n + RKNN Runtime  
> **Goal:** False-positive rate 8 % → < 3 %, zero-downtime model updates

---

## Architecture Overview

A five-stage **closed-loop** pipeline that runs entirely on-device:

```
[Live Inference] ──► [1. Data Collection] ──► [2. First Screening (base.pt)]
                                                          │
                                                          ▼
                                             [3. Reference Validation]
                                                          │
                                                          ▼
                                             [4. LoRA Retraining + O-LoRA + EWC]
                                                          │
                                                          ▼
                                       [5. Evaluate → RKNN Convert → Atomic Swap]
                                                          │
                                                          ▼
                                              [Production Inference]
```

| Stage | Input | Output | Duration | RAM Budget |
|-------|-------|--------|----------|------------|
| 1. Data Collection | Live stream | Low-conf image buffer | Continuous | ~200 MB |
| 2. First Screening | Buffer + base.pt | Filtered candidates | ~30 s/batch | ~800 MB peak |
| 3. Second Screening | Candidates + ref dataset | Curated training set | ~30 s/batch | ~600 MB |
| 4. LoRA Retraining | Curated set + current model | Updated LoRA weights | ≤3 min | ~2.5 GB peak |
| 5. Eval & Deploy | Updated model + test set | Deployed RKNN model | ~90 s | ~1.5 GB peak |

---

## Repository Structure

```
edge_learner/
├── config/                  # YAML configuration
├── collector/               # Stage 1 – data collection
├── screener/                # Stages 2–3 – validation pipeline
├── trainer/                 # Stage 4 – LoRA + O-LoRA + EWC + replay
├── evaluator/               # Stage 5a – metrics & gate check
├── deployer/                # Stage 5b – RKNN conversion & atomic swap
├── orchestrator/            # Pipeline runner, mode manager, scheduler
├── inference/               # RKNN inference engine
└── utils/                   # Storage, provenance, logging, cloud sync
systemd/                     # systemd service files
.github/workflows/           # CI/CD for model versioning
```

---

## Quick Start

```bash
# 1. Install dependencies (ARM64 / x86 dev machine)
pip install -e .[dev]

# 2. Edit configuration
nano config/pipeline.yaml

# 3. Run inference engine (normal mode)
python -m edge_learner.inference.frame_pipeline

# 4. Trigger a manual maintenance cycle
python -m edge_learner.orchestrator.pipeline_runner --mode maintenance

# 5. Install systemd services on RK3588
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now edge-learner-inference.service
sudo systemctl enable --now edge-learner-pipeline.service
```

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| False Positive Rate | 8 % | < 3 % |
| Defect Escape Rate | 34 % missed | < 10 % missed |
| Inference Latency | < 100 ms | < 100 ms (200 ms max) |
| Throughput | 30 img/s | 30 img/s maintained |
| Model Update Downtime | Manual | Zero (atomic swap) |
| Retraining Duration | N/A | ≤ 3 minutes |

---

## Implementation Roadmap

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| 1. Foundation | 1–3 | Inference + passive data collection |
| 2. Validation Pipeline | 4–6 | Two-stage screening + curated datasets |
| 3. LoRA Training Engine | 7–9 | On-device retraining within constraints |
| 4. Eval & Deployment | 10–12 | Full autonomous pipeline |
| 5. Hardening | 13–14 | Monitoring, systemd, GitHub Actions |

---

## License

MIT
