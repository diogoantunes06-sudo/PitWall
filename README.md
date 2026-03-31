# PitWall 🏎️

Site de classificações do automobilismo mundial com atualização automática via GitHub Actions.

## Categorias

| Categoria | Atualização | Fonte |
|---|---|---|
| Fórmula 1 | Automática (toda segunda) | Ergast API |
| Fórmula E | Manual | JSON |
| Fórmula 2 | Manual | JSON |
| Fórmula 3 | Manual | JSON |
| F4 Brasil | Manual | JSON |

## Como publicar no GitHub Pages

1. Crie um repositório no GitHub (ex: `pitwall`)
2. Suba todos os arquivos deste projeto
3. Vá em **Settings → Pages**
4. Em **Source**, selecione `Deploy from a branch`
5. Escolha `main` e pasta `/ (root)`
6. Clique em **Save**

O site ficará disponível em: `https://seu-usuario.github.io/pitwall`

## Como atualizar os dados manuais (F2, F3, F4, FE)

Após cada corrida, edite o arquivo correspondente em `data/`:

```json
{
  "drivers": [
    {"pos": 1, "name": "Nome do Piloto", "team": "Equipe", "points": 100, "nationality": "BRA"},
    ...
  ],
  "constructors": [...],
  "calendar": [
    {"round": 1, "name": "Nome da Etapa", "circuit": "Circuito", "date": "2026-04-12", "status": "done"},
    ...
  ],
  "last_updated": "2026-04-12"
}
```

**Status possíveis no calendário:**
- `"done"` — corrida já realizada
- `"upcoming"` — corrida futura

## Automação GitHub Actions

O workflow `.github/workflows/update.yml` roda toda segunda-feira às 06:00 UTC e:
- Atualiza F1 automaticamente via Ergast API
- Mantém os JSONs manuais intactos
- Faz commit automático se houver mudanças

Para rodar manualmente: **Actions → Atualizar dados PitWall → Run workflow**

## Estrutura

```
pitwall/
├── index.html              ← site principal
├── data/
│   ├── f1.json             ← atualizado automaticamente
│   ├── fe.json             ← atualização manual
│   ├── f2.json             ← atualização manual
│   ├── f3.json             ← atualização manual
│   └── f4brasil.json       ← atualização manual
├── scripts/
│   └── update_data.py      ← script de atualização automática
└── .github/workflows/
    └── update.yml          ← agendamento GitHub Actions
```
