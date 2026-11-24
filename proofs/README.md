# Proofs — mengikat DID ke commit repo ini

## Kenapa
`proof` (v2) = tanda tangan Ed25519 atas metadata:

```
schema | artifact_url | commit | issued_at | expires_at | nonce
```

Isinya **cuma metadata** — bukan isi file. Artinya siapa pun bisa memverifikasi bahwa DID

```
did:key:z6MkkKgQc8d1BYgxjB9Y4319VBawWgLWbydXea4ArfGv2UPG
```

memang meng-klaim commit tertentu di repo ini, tanpa kita perlu mempercayai server mana pun.

## Prasyarat
Repo ini harus **publik** dulu (host artifact wajib ada di allowlist tool:
`github.com`, `gitlab.com`, `codeberg.org`, `bitbucket.org`, `x.com`, `medium.com`, `youtube.com`, dll).

## Langkah (sekali token GitHub tersedia)

```bash
PY=~/venvs/technocore/bin/python
TOOL=~/tools/technocore-did-gameplay

# 1) push repo  (butuh `gh auth login` ATAU GITHUB_TOKEN di env)
$PY $TOOL/github_upload.py jackone-agent-did --dir ~/repos/jackone-agent-did \
    --description "Jackone Jr. agent DID + signed Technocore check-in log"

# 2) ambil commit yang PERSIS ke-push
cd ~/repos/jackone-agent-did && COMMIT=$(git rev-parse HEAD) && echo $COMMIT

# 3) tanda tangani proof
$PY $TOOL/technocore_agent.py proof https://github.com/<akun>/jackone-agent-did $COMMIT \
    --passphrase-file ~/.technocore/passphrase --output proofs/proof.json

# 4) verifikasi + commit hasilnya
$PY $TOOL/technocore_agent.py verify-proof proofs/proof.json
git add -A && git commit -m "Add contribution proof v2" && git push
```

## Verifikasi oleh orang lain (tanpa repo ini)
```bash
python technocore_agent.py verify-proof proof.json
# → "valid proof for did:key:z6MkkKgQc8d1BYgxjB9Y4319VBawWgLWbydXea4ArfGv2UPG"
```

> Catatan: `rotate` bikin DID baru + statement `old → new`; proof lama tetap valid sampai `expires_at`,
> jadi jangan panik kalau nanti rotate — cukup publikasikan statement rotation-nya.
