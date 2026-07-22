# 🔐 Shared Secrets Vault

Të gjitha kredencialet e infrastrukturës ruhen këtu.

## Skedarët

- `infrastructure.env` — API keys për shërbime cloud (Brave, Stability AI, DeepSeek)
- `manage.sh` — script për menaxhimin e sekreteve

## Rregullat

1. **ASNJËHERË** commit në git
2. Çdo API key ruhet në `.env` file në këtë folder
3. Projekte individuale (EdaS, TotoTrading, etj) kanë `secrets/secrets.env` të tyren
4. Ky folder është i aksesueshëm vetëm nga Halim dhe Kllosha

## Si të shtosh një secret

```bash
echo "API_KEY=sk-xxx" >> secrets/infrastructure.env
```

## Si t'i përdorësh në Gateway config

Gateway config referencon çelësat nga ky folder përmes `tools.web.search.apiKey`.
