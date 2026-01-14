# Guia de Gravacao dos Videos de Backup

## Ferramentas Recomendadas

| Ferramenta | Instalacao | Uso |
|------------|------------|-----|
| **OBS Studio** | `sudo apt install obs-studio` | Interface grafica, mais completo |
| **SimpleScreenRecorder** | `sudo apt install simplescreenrecorder` | Simples e leve |
| **asciinema** | `sudo apt install asciinema` | Apenas terminal (pode converter para video) |

## Configuracao Recomendada

- **Resolucao:** 1920x1080 (Full HD)
- **FPS:** 30
- **Formato:** MP4 (H.264)
- **Audio:** Opcional (pode narrar ou deixar mudo)

## Estrutura dos Videos

```
videos/backup/
├── 01-ci-pipeline.mp4      # ~3-5 min
├── 02-deploy-dev.mp4       # ~2-3 min
├── 03-promotion-stg.mp4    # ~2-3 min
├── 04-promotion-prod.mp4   # ~2-3 min
└── 05-rollback.mp4         # ~3-5 min
```

---

## Video 01: CI Pipeline (3-5 min)

### Objetivo
Mostrar o fluxo completo de CI: PR → GitHub Actions → merge → push de imagem.

### Pre-requisitos
- Branch `feature/change-role` disponivel
- GitHub Actions configurado

### Roteiro

1. **Mostrar codigo atual (30s)**
   ```bash
   cd ~/repos/personal/image-promotion-gitops
   git log --oneline -5
   git status
   ```

2. **Criar PR (30s)**
   ```bash
   gh pr create --base main --head feature/change-role \
     --title "feat: add role change support" \
     --body "Permite alterar a role do usuario na edicao"
   ```

3. **Mostrar GitHub Actions (2-3 min)**
   - Abrir browser: https://github.com/marcellmartini/image-promotion-gitops/actions
   - Mostrar jobs executando: pyright, pylint, black, tests, build
   - Aguardar conclusao (ou usar video acelerado)

4. **Aprovar e Mergear (30s)**
   ```bash
   gh pr merge --merge
   ```

5. **Mostrar imagem no Docker Hub (30s)**
   - Abrir: https://hub.docker.com/r/marcellmartini/image-promotion-backend/tags
   - Mostrar nova tag com hash do commit

---

## Video 02: Deploy em DEV (2-3 min)

### Objetivo
Mostrar Kargo detectando nova imagem e promovendo automaticamente para dev.

### Pre-requisitos
- Nova imagem disponivel no Docker Hub
- Kargo e Argo CD rodando

### Roteiro

1. **Verificar Warehouse (30s)**
   ```bash
   kubectl get warehouse -n image-promotion
   ```

2. **Verificar Freight criado (30s)**
   ```bash
   kubectl get freight -n image-promotion
   # Mostrar alias e imagens
   kubectl get freight -n image-promotion -o yaml | grep -A 10 "images:"
   ```

3. **Verificar promocao automatica (30s)**
   ```bash
   kubectl get promotions -n image-promotion
   kubectl get stages -n image-promotion
   ```

4. **Mostrar Argo CD (30s)**
   - Abrir UI: https://localhost:8080
   - Mostrar dev-app sincronizado e Healthy

5. **Verificar pods (30s)**
   ```bash
   kubectl get pods -n dev
   kubectl get pods -n dev -o wide
   ```

---

## Video 03: Promocao para STG (2-3 min)

### Objetivo
Mostrar aprovacao manual no Kargo UI e deploy em STG.

### Pre-requisitos
- Freight disponivel e verificado em dev
- Kargo UI acessivel

### Roteiro

1. **Mostrar stage aguardando (30s)**
   ```bash
   kubectl get stages -n image-promotion
   # stg deve mostrar "Stage has no current Freight"
   ```

2. **Aprovar no Kargo UI (1 min)**
   - Abrir: https://localhost:3000
   - Login: admin / admin
   - Navegar: Projects → image-promotion
   - Clicar no stage "stg"
   - Clicar em "Promote"
   - Selecionar o freight disponivel
   - Confirmar

3. **Verificar promocao (30s)**
   ```bash
   kubectl get promotions -n image-promotion | grep stg
   kubectl get stages -n image-promotion
   ```

4. **Verificar pods em STG (30s)**
   ```bash
   kubectl get pods -n stg
   # Deve mostrar 2 replicas de backend e frontend
   ```

---

## Video 04: Promocao para PROD (2-3 min)

### Objetivo
Mostrar aprovacao manual no Kargo UI e deploy em PROD.

### Pre-requisitos
- Freight verificado em stg
- Kargo UI acessivel

### Roteiro

1. **Aprovar no Kargo UI (1 min)**
   - Abrir: https://localhost:3000
   - Navegar: Projects → image-promotion
   - Clicar no stage "prod"
   - Clicar em "Promote"
   - Selecionar o freight disponivel
   - Confirmar

2. **Verificar promocao (30s)**
   ```bash
   kubectl get promotions -n image-promotion | grep prod
   kubectl get stages -n image-promotion
   ```

3. **Verificar pods em PROD (30s)**
   ```bash
   kubectl get pods -n prod
   # Deve mostrar 3 replicas de backend e frontend
   ```

4. **Mostrar todos os ambientes (30s)**
   ```bash
   echo "=== DEV (1 replica) ===" && kubectl get pods -n dev
   echo "=== STG (2 replicas) ===" && kubectl get pods -n stg
   echo "=== PROD (3 replicas) ===" && kubectl get pods -n prod
   ```

---

## Video 05: Rollback Automatico (3-5 min)

### Objetivo
Mostrar deploy com erro, deteccao de falha e recuperacao.

### Pre-requisitos
- Branch `feature/error` disponivel
- Branch `feature/fix` disponivel
- Ambiente dev funcionando

### Roteiro

1. **Mostrar estado atual (30s)**
   ```bash
   kubectl get pods -n dev
   # Pods devem estar Running
   ```

2. **Criar PR com erro (30s)**
   ```bash
   gh pr create --base main --head feature/error \
     --title "feat: update health check" \
     --body "Atualiza endpoint de health check"
   ```

3. **Mergear (30s)**
   ```bash
   gh pr merge --merge
   ```

4. **Aguardar CI e promocao (1-2 min)**
   ```bash
   # Monitorar promocao
   watch kubectl get promotions -n image-promotion
   ```

5. **Mostrar erro nos pods (30s)**
   ```bash
   kubectl get pods -n dev
   # STATUS: CrashLoopBackOff

   kubectl logs -n dev -l app=backend --tail=10
   # Mostrar erro: RuntimeError
   ```

6. **Mostrar Argo CD degradado (30s)**
   - Abrir UI: https://localhost:8080
   - Mostrar dev-app com status "Degraded"

7. **Criar PR com fix (30s)**
   ```bash
   gh pr create --base main --head feature/fix \
     --title "fix: fix health check" \
     --body "Corrige endpoint de health check"
   ```

8. **Mergear e aguardar recuperacao (1 min)**
   ```bash
   gh pr merge --merge

   # Monitorar recuperacao
   watch kubectl get pods -n dev
   # STATUS: Running
   ```

9. **Mostrar Argo CD recuperado (30s)**
   - Mostrar dev-app com status "Healthy"

---

## Dicas de Gravacao

1. **Prepare o ambiente antes** - tenha tudo pronto antes de iniciar a gravacao
2. **Use tmux/splits** - mostre terminal e browser lado a lado quando possivel
3. **Pause entre comandos** - de tempo para o espectador ler
4. **Aumente a fonte** - use fonte grande no terminal (14-16pt)
5. **Limpe o historico** - `history -c` para nao mostrar comandos anteriores
6. **Teste antes** - faca um dry-run antes de gravar

## Comandos Uteis

```bash
# Limpar terminal
clear

# Aumentar fonte no terminal (Kitty)
kitty @ set-font-size 16

# Gravar com asciinema
asciinema rec demo.cast

# Converter asciinema para GIF
asciinema-agg demo.cast demo.gif

# Converter asciinema para video
# (requer docker)
docker run --rm -v $PWD:/data asciinema/asciicast2gif demo.cast demo.gif
```

---

## Pos-Gravacao

1. Revisar cada video
2. Cortar partes desnecessarias (se precisar)
3. Salvar em `videos/backup/`
4. Testar reproducao antes da apresentacao
