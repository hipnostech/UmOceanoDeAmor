import re, html, json, sys, unicodedata, urllib.request
FONTES = {
 "kb": ["anavitoria/ai-amor","anavitoria/porque-eu-te-amo","anavitoria/me-conta-da-tua-janela","anavitoria/singular",
        "anavitoria/quero-contar-pra-sao-paulo","anavitoria/cor-de-marte","anavitoria/calendario","marisa-monte/amor-i-love-you","marisa-monte/ainda-bem",
        "marisa-monte/beija-eu","marisa-monte/infinito-particular","marisa-monte/vilarejo","djavan/oceano","djavan/se",
        "djavan/petala","djavan/eu-te-devoro","caetano-veloso/sozinho","tim-maia/azul-da-cor-do-mar","lulu-santos/como-uma-onda"],
}
def baixar(url):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Macintosh)"}), timeout=15).read()
    try: return raw.decode("utf-8")
    except UnicodeDecodeError: return raw.decode("latin-1")
def limpar(t):
    t = re.sub(r'<br\s*/?>', '\n', t); t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', '\n', t))
def norm(t):
    t = unicodedata.normalize("NFKC", t).lower()
    t = re.sub(r'[“”"«»().,?!:;…\-—–]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()
corpus = []
for p in FONTES["kb"]:
    s = baixar(f"https://www.kboing.com.br/{p}/"); m = re.search(r'class="lyric[^"]*"[^>]*>(.*?)</(?:div|section)>', s, re.S)
    corpus.append((p, norm(limpar(m.group(1)) if m else "")))
for nome, url in [("trevo","https://www.letras.com.br/anavitoria/trevo"),("o-mar","https://www.vagalume.com.br/dorival-caymmi/o-mar.html")]:
    corpus.append((nome, norm(limpar(baixar(url)))))
s = open("index.html", encoding="utf-8").read()
def lista(nome):
    a = s.index(f"const {nome} = ["); b = s.index("];", a)
    return re.findall(r'"([^"]+)"', s[a:b])
NOSSAS = {"TRÊS LUAS CHEIAS","TRÊS MESES DE NÓS"}
TITULOS = {"BABYDOLL","STAY","PRETTY BABY","PORQUE EU TE AMO","PRA VOCÊ GUARDEI O AMOR","PERTO DE VOCÊ","CHAMEGO MEU","EU TE DEVORO",
  "TE AMAR É MASSA DEMAIS","COR DE MARTE","A GENTE JUNTO","UM DIA APÓS O OUTRO","AI, AMOR","LUZ DOS OLHOS","JURA JURADINHO","SIDERAL",
  "VEM MEU AMOR","DENGO","NÓS","TUA","FICA","QUERO CONTAR PRA SÃO PAULO","ME CONTA DA TUA JANELA","AZUL DA COR DO MAR"}
citas = re.findall(r'musica: "♪ “([^”]+)” — ([^"]+)"', s)
erros = 0
def checar(frase, rotulo):
    global erros
    n = norm(frase); ach = [p for p, c in corpus if n in c]
    if not ach: erros += 1
    print(("OK  " if ach else "ERRO"), rotulo, "|", frase, "→", ",".join(ach) or "não está em nenhuma letra")
for f in lista("FRASES"):
    if f in NOSSAS: print("NOSSA", "chão |", f); continue
    if f in TITULOS: print("TÍTULO", "chão |", f); continue
    checar(f, "chão")
for f in lista("ESTRELAS"): checar(f, "estrela")
for f, onde in citas: checar(f, "carta (" + onde + ")")
print("\nERROS:", erros)
