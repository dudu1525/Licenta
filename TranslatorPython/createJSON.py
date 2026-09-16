import json

core_data = []


pronouns = [
    ("I", "eu", ["<prn>","<p1>","<sg>","<nom>"], ["<prn>","<p1>","<sg>","<nom>","<tn>"]),
    ("me", "mă", ["<prn>","<p1>","<sg>","<acc>"], ["<prn>","<p1>","<sg>","<acc>","<cl>"]),
    ("my", "meu", ["<prn>","<p1>","<sg>","<gen>"], ["<prn>","<p1>","<sg>","<gen>"]),
    ("mine", "al meu", ["<prn>","<p1>","<sg>","<gen>"], ["<prn>","<p1>","<sg>","<gen>","<tn>"]),
    ("you", "tu", ["<prn>","<p2>","<sg>","<nom>"], ["<prn>","<p2>","<sg>","<nom>","<tn>"]),
    ("your", "tău", ["<prn>","<p2>","<sg>","<gen>"], ["<prn>","<p2>","<sg>","<gen>"]),
    ("he", "el", ["<prn>","<p3>","<sg>","<m>","<nom>"], ["<prn>","<p3>","<sg>","<m>","<nom>","<tn>"]),
    ("him", "îl", ["<prn>","<p3>","<sg>","<m>","<acc>"], ["<prn>","<p3>","<sg>","<m>","<acc>","<cl>"]),
    ("his", "lui", ["<prn>","<p3>","<sg>","<m>","<gen>"], ["<prn>","<p3>","<sg>","<m>","<gen>"]),
    ("she", "ea", ["<prn>","<p3>","<sg>","<f>","<nom>"], ["<prn>","<p3>","<sg>","<f>","<nom>","<tn>"]),
    ("her", "o", ["<prn>","<p3>","<sg>","<f>","<acc>"], ["<prn>","<p3>","<sg>","<f>","<acc>","<cl>"]),
    ("we", "noi", ["<prn>","<p1>","<pl>","<nom>"], ["<prn>","<p1>","<pl>","<nom>","<tn>"]),
    ("us", "ne", ["<prn>","<p1>","<pl>","<acc>"], ["<prn>","<p1>","<pl>","<acc>","<cl>"]),      
    ("they", "ei", ["<prn>","<p3>","<pl>","<nom>"], ["<prn>","<p3>","<pl>","<m>","<nom>","<tn>"]),
    ("them", "îi", ["<prn>","<p3>","<pl>","<acc>"], ["<prn>","<p3>","<pl>","<m>","<acc>","<cl>"]),
]
core_data.extend(pronouns)


humans = [
    ("man","bărbat","<m>"), ("woman","femeie","<f>"), ("child","copil","<m>"),
    ("boy","băiat","<m>"), ("girl","fată","<f>"), ("baby","bebeluș","<m>"),
    ("father","tată","<m>"), ("mother","mamă","<f>"), ("son","fiu","<m>"),
    ("daughter","fiică","<f>"), ("brother","frate","<m>"), ("sister","soră","<f>"),
    ("grandfather","bunic","<m>"), ("grandmother","bunică","<f>"), ("uncle","unchi","<m>"),
    ("aunt","mătușă","<f>"), ("cousin","văr","<m>"), ("husband","soț","<m>"),
    ("wife","soție","<f>"), ("friend","prieten","<m>"), ("teacher","profesor","<m>"),
    ("student","student","<m>"), ("doctor","doctor","<m>"), ("king","rege","<m>"),
    ("queen","regină","<f>")
]
for en, ro, g in humans:
    core_data.append((en, ro, ["<n>","<sg>","<count>"], ["<n>",g,"<sg>","<anim>","<human>"]))

animals = [
    ("dog","câine","<m>"), ("cat","pisică","<f>"), ("horse","cal","<m>"),
    ("cow","vacă","<f>"), ("pig","porc","<m>"), ("sheep","oaie","<f>"),
    ("goat","capră","<f>"), ("chicken","pui","<m>"), ("duck","rață","<f>"),
    ("fish","pește","<m>"), ("bird","pasăre","<f>"), ("bear","urs","<m>"),
    ("wolf","lup","<m>"), ("fox","vulpe","<f>"), ("rabbit","iepure","<m>"),
    ("mouse","șoarece","<m>"), ("lion","leu","<m>"), ("tiger","tigru","<m>"),
    ("elephant","elefant","<m>"), ("monkey","maimuță","<f>"), ("snake","șarpe","<m>"),
    ("frog","broască","<f>"), ("bee","albină","<f>"), ("ant","furnică","<f>"),
    ("butterfly","fluture","<m>")
]
for en, ro, g in animals:
    core_data.append((en, ro, ["<n>","<sg>","<count>"], ["<n>",g,"<sg>","<anim>"]))

body = [
    ("head","cap","<nt>"), ("face","față","<f>"), ("eye","ochi","<m>"),
    ("ear","ureche","<f>"), ("nose","nas","<nt>"), ("mouth","gură","<f>"),
    ("tooth","dinte","<m>"), ("tongue","limbă","<f>"), ("lip","buza","<f>"),
    ("neck","gât","<nt>"), ("shoulder","umăr","<nt>"), ("arm","braț","<nt>"),
    ("hand","mână","<f>"), ("finger","deget","<nt>"), ("leg","picior","<nt>"),
    ("foot","picior","<nt>"), ("knee","genunchi","<nt>"), ("back","spate","<nt>"),
    ("chest","piept","<nt>"), ("heart","inimă","<f>"), ("blood","sânge","<nt>"),
    ("bone","os","<nt>"), ("skin","piele","<f>"), ("hair","păr","<nt>"),
    ("brain","creier","<nt>")
]
for en, ro, g in body:
    core_data.append((en, ro, ["<n>","<sg>","<count>"], ["<n>",g,"<sg>"]))

house = [
    ("house","casă","<f>"), ("room","cameră","<f>"), ("door","ușă","<f>"),
    ("window","fereastră","<f>"), ("wall","perete","<m>"), ("floor","podea","<f>"),
    ("roof","acoperiș","<nt>"), ("table","masă","<f>"), ("chair","scaun","<nt>"),
    ("bed","pat","<nt>"), ("desk","birou","<nt>"), ("shelf","raft","<nt>"),
    ("mirror","oglindă","<f>"), ("lamp","lampă","<f>"), ("clock","ceas","<nt>"),
    ("key","cheie","<f>"), ("lock","lacăt","<nt>"), ("book","carte","<f>"),
    ("pen","stilou","<nt>"), ("paper","hârtie","<f>"), ("phone","telefon","<nt>"),
    ("computer","calculator","<nt>"), ("car","mașină","<f>"), ("bicycle","bicicletă","<f>"),
    ("road","drum","<nt>"), ("street","stradă","<f>"), ("bridge","pod","<nt>"),
    ("shirt","cămașă","<f>"), ("pants","pantaloni","<m>"), ("shoe","pantof","<m>"),
    ("hat","pălărie","<f>"), ("coat","palton","<nt>"), ("bag","geantă","<f>"),
    ("money","bani","<m>"), ("coin","monedă","<f>"), ("tool","unealtă","<f>"),
    ("knife","cuțit","<nt>"), ("cup","cană","<f>"), ("plate","farfurie","<f>"),
    ("bottle","sticlă","<f>")
]
for en, ro, g in house:
    core_data.append((en, ro, ["<n>","<sg>","<count>"], ["<n>",g,"<sg>"]))

nature = [
    ("sun","soare","<m>"), ("moon","lună","<f>"), ("star","stea","<f>"),
    ("sky","cer","<nt>"), ("cloud","nor","<m>"), ("rain","ploaie","<f>"),
    ("snow","zăpadă","<f>"), ("wind","vânt","<nt>"), ("storm","furtună","<f>"),
    ("sea","mare","<f>"), ("river","râu","<nt>"), ("lake","lac","<nt>"),
    ("mountain","munte","<m>"), ("hill","deal","<nt>"), ("valley","vale","<f>"),
    ("forest","pădure","<f>"), ("tree","copac","<m>"), ("flower","floare","<f>"),
    ("grass","iarbă","<f>"), ("leaf","frunză","<f>"), ("stone","piatră","<f>"),
    ("sand","nisip","<nt>"), ("earth","pământ","<nt>"), ("fire","foc","<nt>"),
    ("ice","gheață","<f>")
]
for en, ro, g in nature:
    core_data.append((en, ro, ["<n>","<sg>","<count>"], ["<n>",g,"<sg>"]))


food = [
    ("bread","pâine","<f>","<mass>"), ("meat","carne","<f>","<mass>"),
    ("fish_food","pește","<m>","<count>"), ("egg","ou","<nt>","<count>"),
    ("cheese","brânză","<f>","<mass>"), ("butter","unt","<nt>","<mass>"),
    ("milk","lapte","<nt>","<mass>"), ("water","apă","<f>","<mass>"),
    ("wine","vin","<nt>","<mass>"), ("beer","bere","<f>","<mass>"),
    ("coffee","cafea","<f>","<count>"), ("tea","ceai","<nt>","<count>"),
    ("juice","suc","<nt>","<count>"), ("soup","supă","<f>","<count>"),
    ("apple","măr","<nt>","<count>"), ("pear","pară","<f>","<count>"),
    ("grape","strugure","<m>","<count>"), ("orange","portocală","<f>","<count>"),
    ("banana","banană","<f>","<count>"), ("tomato","roșie","<f>","<count>"),
    ("potato","cartof","<m>","<count>"), ("onion","ceapă","<f>","<count>"),
    ("carrot","morcov","<m>","<count>"), ("salt","sare","<f>","<mass>"),
    ("sugar","zahăr","<nt>","<mass>"), ("oil","ulei","<nt>","<mass>"),
    ("rice","orez","<nt>","<mass>"), ("cake","tort","<nt>","<count>"),
    ("chocolate","ciocolată","<f>","<mass>"), ("ice_cream","înghețată","<f>","<count>")
]
for en, ro, g, c in food:
    core_data.append((en, ro, ["<n>","<sg>",c], ["<n>",g,"<sg>"]))


time_words = [
    ("time","timp","<m>"), ("year","an","<m>"), ("month_l","lună","<f>"),
    ("week","săptămână","<f>"), ("day","zi","<f>"), ("hour","oră","<f>"),
    ("minute","minut","<nt>"), ("second","secundă","<f>"), ("morning","dimineață","<f>"),
    ("afternoon","după-amiază","<f>"), ("evening","seară","<f>"), ("night","noapte","<f>"),
    ("today","azi","<adv>"), ("tomorrow","mâine","<adv>"), ("yesterday","ieri","<adv>"),
    ("Monday","luni","<f>"), ("Tuesday","marți","<f>"), ("Wednesday","miercuri","<f>"),
    ("Thursday","joi","<f>"), ("Friday","vineri","<f>"), ("Saturday","sâmbătă","<f>"),
    ("Sunday","duminică","<f>"), ("January","ianuarie","<f>"), ("February","februarie","<f>"),
    ("March","martie","<f>"), ("April","aprilie","<f>"), ("May_m","mai","<m>"),
    ("June","iunie","<f>"), ("July","iulie","<f>"), ("August","august","<m>"),
    ("September","septembrie","<f>"), ("October","octombrie","<f>"), ("November","noiembrie","<f>"),
    ("December","decembrie","<f>"), ("spring","primăvară","<f>"), ("summer","vară","<f>"),
    ("autumn","toamnă","<f>"), ("winter","iarnă","<f>")
]
for en, ro, g in time_words:
    if "<adv>" in g:
        core_data.append((en, ro, ["<adv>"], ["<adv>"]))
    else:
        core_data.append((en, ro, ["<n>","<sg>","<count>"], ["<n>",g,"<sg>"]))

numbers = [
    ("zero","zero"), ("one","unu"), ("two","doi"), ("three","trei"),
    ("four","patru"), ("five","cinci"), ("six","șase"), ("seven","șapte"),
    ("eight","opt"), ("nine","nouă"), ("ten","zece"), ("eleven","unsprezece"),
    ("twelve","doisprezece"), ("thirteen","treisprezece"), ("fourteen","paisprezece"),
    ("fifteen","cincisprezece"), ("sixteen","șaisprezece"), ("seventeen","șaptesprezece"),
    ("eighteen","optsprezece"), ("nineteen","nouăsprezece"), ("twenty","douăzeci"),
    ("thirty","treizeci"), ("forty","patruzeci"), ("fifty","cincizeci"),
    ("hundred","sută")
]
for en, ro in numbers:
    core_data.append((en, ro, ["<n>","<sg>","<count>"], ["<n>","<m>","<sg>"]))


verbs = [
    ("be","a_fi",["<intr>"]), ("have","a_avea",["<tran>"]),
    ("do","a_face",["<tran>"]), ("go","a_merge",["<intr>"]),
    ("come","a_veni",["<intr>"]), ("see","a_vedea",["<tran>"]),
    ("hear","a_auzi",["<tran>"]), ("say","a_spune",["<tran>","<ditrans>"]),
    ("give","a_da",["<tran>","<ditrans>"]), ("take","a_lua",["<tran>"]),
    ("know","a_ști",["<tran>"]), ("think","a_gândi",["<tran>"]),
    ("want","a_vrea",["<tran>","<gov_conj>"]), ("can","a_putea",["<tran>","<gov_conj>"]),
    ("must","a_trebui",["<tran>","<gov_conj>"]), ("love","a_iubi",["<tran>"]),
    ("hate","a_urî",["<tran>"]), ("like","a_plăcea",["<tran>"]),
    ("eat","a_mânca",["<tran>"]), ("drink","a_be",["<tran>"]),
    ("sleep","a_dormi",["<intr>"]), ("wake","a_trezii",["<intr>"]),
    ("walk","a_merge",["<intr>"]), ("run","a_alerga",["<intr>"]),
    ("sit","a_se_aseza",["<intr>","<ref>"]), ("stand","a_sta",["<intr>"]),
    ("write","a_scrie",["<tran>"]), ("read","a_citi",["<tran>"]),
    ("speak","a_vorbi",["<intr>"]), ("listen","a_asculta",["<tran>"]),
    ("look","a_privii",["<intr>"]), ("watch","a_privii",["<tran>"]),
    ("find","a_găsi",["<tran>"]), ("lose","a_pierde",["<tran>"]),
    ("buy","a_cumpăra",["<tran>"]), ("sell","a_vinde",["<tran>"]),
    ("pay","a_plăti",["<tran>"]), ("work","a_lucra",["<intr>"]),
    ("play","a_se_juca",["<intr>","<ref>"]), ("learn","a_învăța",["<tran>"]),
    ("teach","a_predua",["<tran>","<ditrans>"]), ("help","a_ajuta",["<tran>"]),
    ("ask","a_întreba",["<tran>","<ditrans>"]), ("answer","a_răspunde",["<intr>"]),
    ("call","a_suna",["<tran>"]), ("wait","a_aștepta",["<tran>"]),
    ("open","a_deschide",["<tran>"]), ("close","a_închide",["<tran>"]),
    ("start","a_începe",["<tran>"]), ("finish","a_termina",["<tran>"]),
    ("stop","a_opri",["<tran>"]), ("continue","a_continua",["<tran>"]),
    ("try","a_încerca",["<tran>"]), ("need","a_avea_nevoie",["<tran>"]),
    ("use","a_folosi",["<tran>"]), ("make","a_face",["<tran>"]),
    ("create","a_crea",["<tran>"]), ("build","a_construi",["<tran>"]),
    ("break","a_sparge",["<tran>"]), ("fix","a_repara",["<tran>"]),
    ("clean","a_curăța",["<tran>"]), ("wash","a_spăla",["<tran>","<ref>"]),
    ("cook","a_găti",["<tran>"]), ("cut","a_tăia",["<tran>"]),
    ("pull","a_trage",["<tran>"]), ("push","a_impinge",["<tran>"]),
    ("throw","a_arunca",["<tran>"]), ("catch","a_prinde",["<tran>"]),
    ("fall","a_cădea",["<intr>"]), ("rise","a_se_ridica",["<intr>","<ref>"]),
    ("fly","a_zbura",["<intr>"]), ("swim","a_înota",["<intr>"]),
    ("drive","a_conduce",["<tran>"]), ("ride","a_călări",["<intr>"]),
    ("travel","a_călători",["<intr>"]), ("arrive","a_sosi",["<intr>"]),
    ("leave","a_pleca",["<intr>"]), ("return","a_se_întoarce",["<intr>","<ref>"]),
    ("enter","a_intra",["<intr>"]), ("exit","a_ieși",["<intr>"]),
    ("live","a_trăi",["<intr>"]), ("die","a_muri",["<intr>"]),
    ("kill","a_omorî",["<tran>"]), ("born","a_se_naște",["<intr>","<ref>"]),
    ("grow","a_crește",["<intr>"]), ("change","a_schimba",["<tran>"]),
    ("become","a_deveni",["<intr>"]), ("stay","a_rămâne",["<intr>"]),
    ("feel","a_simți",["<tran>"]), ("seem","a_părea",["<intr>"]),
    ("appear","a_apărea",["<intr>"]), ("disappear","a_dispărea",["<intr>"]),
    ("happen","a_se_întâmpla",["<intr>","<ref>"]), ("exist","a_exista",["<intr>"]),
    ("belong","a_apartine",["<intr>"]), ("contain","a_conține",["<tran>"]),
    ("include","a_include",["<tran>"]), ("mean","a_însemna",["<tran>"]),
    ("remember","a_și_aminti",["<tran>","<ref>"]), ("forget","a_uita",["<tran>"]),
    ("believe","a_crede",["<tran>"]), ("hope","a_spera",["<tran>","<gov_conj>"]),
    ("fear","a_se_tem",["<tran>","<ref>"]), ("wish","a_dori",["<tran>","<gov_conj>"]),
    ("choose","a_alege",["<tran>"]), ("decide","a_decide",["<tran>"]),
    ("agree","a_fi_de_acord",["<intr>"]), ("disagree","a_nu_fi_de_acord",["<intr>"]),
    ("promise","a_promite",["<tran>","<ditrans>"]), ("offer","a_oferi",["<tran>","<ditrans>"]),
    ("receive","a_primi",["<tran>"]), ("send","a_trimite",["<tran>","<ditrans>"]),
    ("bring","a_aduce",["<tran>"]), ("carry","a_cara",["<tran>"]),
    ("hold","aține",["<tran>"]), ("put","a_pune",["<tran>"]),
    ("move","a_mișca",["<tran>"]), ("turn","a_intoarce",["<tran>"]),
    ("follow","a_urmări",["<tran>"]), ("lead","a_conduce",["<tran>"]),
    ("meet","a_întâlni",["<tran>"]), ("visit","a_vizita",["<tran>"]),
    ("invite","a_invita",["<tran>","<ditrans>"]), ("thank","a_mulțumi",["<tran>"]),
    ("apologize","a_și_cere_scuze",["<intr>","<ref>"]), ("celebrate","a_celebra",["<tran>"])
]
for en, ro, extra_tags in verbs:
    core_data.append((en, ro, ["<vb>"] + extra_tags, ["<vb>"] + extra_tags))


adjectives = [
    ("good","bun"), ("bad","rău"), ("big","mare"), ("small","mic"),
    ("long","lung"), ("short","scurt"), ("high","înalt"), ("low","scund"),
    ("wide","larg"), ("narrow","îngust"), ("thick","gros"), ("thin","subțire"),
    ("heavy","greu"), ("light","ușor"), ("fast","rapid"), ("slow","lent"),
    ("hot","cald"), ("cold","rece"), ("warm","cald"), ("cool","rece"),
    ("new","nou"), ("old","vechi"), ("young","tânăr"), ("beautiful","frumos"),
    ("ugly","urât"), ("clean","curat"), ("dirty","murdar"), ("rich","bogat"),
    ("poor","sărac"), ("happy","fericit"), ("sad","trist"), ("angry","supărat"),
    ("tired","obosit"), ("hungry","flămând"), ("thirsty","însetat"), ("sick","bolnav"),
    ("healthy","sănătos"), ("strong","puternic"), ("weak","slab"), ("smart","deștept"),
    ("stupid","prost"), ("easy","ușor"), ("hard","greu"), ("simple","simplu"),
    ("difficult","dificil"), ("important","important"), ("necessary","necesar"),
    ("possible","posibil"), ("impossible","imposibil"), ("true","adevărat"),
    ("false","fals"), ("red","roșu"), ("blue","albastru"), ("green","verde"),
    ("yellow","galben"), ("black","negru"), ("white","alb"), ("brown","maro"),
    ("gray","gri"), ("full","plin"), ("empty","gol"), ("open","deschis"),
    ("closed","închis"), ("right","drept"), ("left","stâng")
]
for en, ro in adjectives:
    core_data.append((en, ro, ["<adj>"], ["<adj>"]))

function_words = [
    ("in","în",["<pr>"],["<pr>"]),
    ("on","pe",["<pr>"],["<pr>"]),
    ("at","la",["<pr>"],["<pr>"]),
    ("with","cu",["<pr>"],["<pr>"]),
    ("without","fără",["<pr>"],["<pr>"]),
    ("for","pentru",["<pr>"],["<pr>"]),
    ("from","de_la",["<pr>"],["<pr>"]),
    ("to","la",["<pr>"],["<pr>"]),
    ("by","de",["<pr>"],["<pr>"]),
    ("about","despre",["<pr>"],["<pr>"]),
    ("and","și",["<cnj>"],["<cnj>"]),
    ("but","dar",["<cnj>"],["<cnj>"]),
    ("or","sau",["<cnj>"],["<cnj>"]),
    ("because","pentru_că",["<cnj>"],["<cnj>"]),
    ("if","dacă",["<cnj>"],["<cnj>"]),
    ("when","când",["<cnj>"],["<cnj>"]),
    ("of", "de",  ["<pr>","<gen_marker>"], ["<pr>"]),
    ("where","unde",["<adv>"],["<adv>"]),
    ("how","cum",["<adv>"],["<adv>"]),
    ("why","de_ce",["<adv>"],["<adv>"]),
    ("very","foarte",["<adv>"],["<adv>"]),
    ("also","de_asemenea",["<adv>"],["<adv>"]),
    ("always","întotdeauna",["<adv>"],["<adv>"]),
    ("never","niciodată",["<adv>","<neg>"],["<adv>","<neg>"]),
    ("yes","da",["<adv>"],["<adv>"]),
    ("no","nu",["<adv>","<neg>"],["<adv>","<neg>"]),
    ("not","nu",["<adv>","<neg>"],["<adv>","<neg>"]),
    ("here","aici",["<adv>"],["<adv>"]),
    ("there","acolo",["<adv>"],["<adv>"]),
    ("now","acum",["<adv>"],["<adv>"]),
    ("then","atunci",["<adv>"],["<adv>"])
]
for en, ro, en_t, ro_t in function_words:
    core_data.append((en, ro, en_t, ro_t))
#more words:
articles = [ #no translation in romanian
    ("the", "the", ["<art>","<def>"], ["<art>","<def>"]),
    ("a", "a", ["<art>","<indef>"], ["<art>","<indef>"]),
    ("an", "a", ["<art>","<indef>"], ["<art>","<indef>"]),
]
demonstratives = [
    ("this",  "acest",   ["<prn>","<sg>"], ["<prn>","<sg>"]),
    ("that",  "acel",    ["<prn>","<sg>"], ["<prn>","<sg>"]),
    ("these", "acești",  ["<prn>","<pl>"], ["<prn>","<pl>"]),
    ("those", "acei",    ["<prn>","<pl>"], ["<prn>","<pl>"]),
]
modals = [
    ("should", "ar trebui", ["<adv>"],  ["<vb>"]),
    ("could",  "ar putea",  ["<adv>"],   ["<vb>"]),
    ("might",  "ar putea",  ["<adv>"],   ["<vb>"]),
    ("may",    "poate",     ["<adv>"],   ["<vb>"]),
]
subordinators = [
    ("that",     "că",       ["<cnj>"],  ["<cnj>"]),  
    ("although", "deși",     ["<cnj>"],           ["<cnj>"]),
    ("while",    "în timp ce",["<cnj>"],          ["<cnj>"]),
    ("unless",   "dacă nu",  ["<cnj>"],           ["<cnj>"]),
    ("until",    "până când",["<cnj>"],           ["<cnj>"]),
    ("whether",  "dacă",     ["<cnj>"],           ["<cnj>"]),        
    ("so_that",  "ca să",    ["<cnj>"],["<cnj>"]), 
    ("in_order_to","ca să",  ["<cnj>"],["<cnj>"]),
]
quantifiers = [
    ("many",    "mulți",    ["<num>","<pl>"],  ["<num>","<pl>","<m>"]),
    ("much",    "mult",     ["<num>","<mass>"], ["<num>","<mass>"]),
    ("few",     "puțini",   ["<num>","<pl>"],  ["<num>","<pl>"]),
    ("little",  "puțin",    ["<num>","<mass>"], ["<num>","<mass>"]),
    ("some",    "niște",    ["<prn>"],          ["<prn>"]),
    ("any",     "orice",    ["<num>"],          ["<num>"]),
    ("every",   "fiecare",  ["<prn>","<sg>"],  ["<prn>","<sg>"]),
    ("all",     "toți",     ["<prn>","<pl>"],  ["<prn>","<pl>"]),
    ("each",    "fiecare",  ["<num>","<sg>"],  ["<num>","<sg>"]),
    ("both",    "amândoi",  ["<num>"],["<num>"]),
    ("several", "câțiva",   ["<prn>","<pl>"],  ["<prn>","<pl>"]),
    ("enough",  "destul",   ["<num>",],          ["<num>"]),
    ("another", "alt",      ["<prn>","<sg>"],             ["<prn>","<sg>"]),
    ("other",   "alt",      ["<prn>"],                    ["<prn>"]),
    ("too",     "prea",     ["<adv>","<deg>"],            ["<adv>","<deg>"]),
    ("more",    "mai mult", ["<adv>","<deg>"],            ["<adv>","<deg>"]),   
    ("most",    "cel mai",  ["<adv>","<deg>"],            ["<adv>","<deg>"]),   
    ("less",    "mai puțin",["<adv>","<deg>"],            ["<adv>","<deg>"]),
]
degree_adverbs = [
    ("so",      "atât de",  ["<adv>"],  ["<adv>"]),
    ("such",    "atât de",  ["<adv>"],  ["<adv>"]),
    ("quite",   "destul de",["<adv>"],  ["<adv>"]),
    ("rather",  "destul de",["<adv>"],  ["<adv>"]),
    ("almost",  "aproape",  ["<adv>"],           ["<adv>"]),
    ("just",    "tocmai",   ["<adv>"],           ["<adv>"]),
    ("only",    "doar",     ["<adv>"],           ["<adv>"]),
    ("even",    "chiar",    ["<adv>"],           ["<adv>"]),
    ("still",   "încă",     ["<adv>"],           ["<adv>"]),
    ("already", "deja",     ["<adv>"],           ["<adv>"]),
    ("yet",     "încă",     ["<adv>","<neg>"],   ["<adv>","<neg>"]),  
    ("again",   "din nou",  ["<adv>"],           ["<adv>"]),
    ("than",    "decât",    ["<cnj>"],  ["<cnj>"]),  
    ("as",      "la fel de",["<adv>"],   ["<adv>"]),    
]
neg_pronouns = [
    ("nothing",  "nimic",    ["<prn>","<neg>"], ["<prn>","<neg>"]),
    ("nobody",   "nimeni",   ["<prn>","<neg>"], ["<prn>","<neg>"]),
    ("nowhere",  "nicăieri", ["<adv>","<neg>"], ["<adv>","<neg>"]),
    ("neither",  "nici",     ["<cnj>","<neg>"], ["<cnj>","<neg>"]),
    ("nor",      "nici",     ["<cnj>","<neg>"], ["<cnj>","<neg>"]),
]
core_data.extend(articles)
core_data.extend(demonstratives)
core_data.extend(modals)
core_data.extend(subordinators)
core_data.extend(quantifiers)
core_data.extend(degree_adverbs)
core_data.extend(neg_pronouns)


en_lex = {}
ro_lex = {}
bi_map = {}

for idx, (en_lemma, ro_lemma, en_tags, ro_tags) in enumerate(core_data, start=1):
    en_id = f"en_{idx:03d}"
    ro_id = f"ro_{idx:03d}"
    
  
    en_lex[en_id] = {
        "lemma": en_lemma,
        "tags": en_tags
    }
    
    ro_lex[ro_id] = {
        "lemma": ro_lemma,
        "tags": ro_tags
    }
    
    bi_map[en_id] = ro_id


with open('en_lex.json', 'w', encoding='utf-8') as f:
    json.dump(en_lex, f, indent=2, ensure_ascii=False)
with open('ro_lex.json', 'w', encoding='utf-8') as f:
    json.dump(ro_lex, f, indent=2, ensure_ascii=False)
with open('bilingual_map.json', 'w', encoding='utf-8') as f:
    json.dump(bi_map, f, indent=2, ensure_ascii=False)

print("files created successfully")