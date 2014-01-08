# sestre 3
set N;                          # skup medicinskih sestara (MS)
set NE, within N;               # podskup iskusnih MS

param names{N}, symbolic;       # imena MS
param dpm;                      # broj dana u mesecu

# termini
set D := 1..dpm;                # skup dana u mesecu
set SH;                         # skup smena u danu
set SSH, within SH;             # smene jakog intenziteta
set WSH, within SH;             # smene slabog intenziteta
set T := {D, SH};               # skup mesecnih termina
param tsh{SH};                  # trajanje smene

# paterni
set PAT;                        # skup paterna
param patlen := card(SH);       # duzina paterna, tj. broj smena u danu
param patern{p in PAT, 1..patlen};       # paterni

# PRAVILA:
# pravila sekvenci
set RS;                         # skup pravila nedozvoljenih sekvenci
param ts{RS};                   # interval sekvence
param prs{r in RS, 1..ts[r]};   # patern za svaki dan sekvence

# pravila grupisanja
set RG;                         # skup pravila grupisanja
set NR{RG}, within N;           # skup MS koje rade po pravilu r
param prg{RG};                  # pravilo za patern
param tg{RG}, default dpm;      # interval za pravilo
param nug{RG};                  # max broj pojavljivanja u intervalu

# termini / sestre
set VD{n in N}, within D, default {};               # podskup dana u kojima je sestra n na god. odmoru, tj.
set WD{n in N} := D diff VD[n];                     # podskup dana u kojima sestra n nije na odmoru (tj. raspoloziva je za posao)
set NA{d in D} := setof{n in N : d not in VD[n]} n; # podskup MS raspolozivih za dan d (nisu na god. odmoru)

set TF{n in N}, within T, default {{},{}};          # podskup termina u kojima sestra n ne sme da radi
set TW{n in N}, within T, default {{},{}};          # podskup termina u kojima sestra n mora da radi
set TP{n in N}, within T, default {{},{}};          # podskup termina u kojima sestra n preferira odsutnost

param ne, integer, >=0;         # min broj iskusnih MS koji mora biti prisutan u svakoj smeni
param ns, integer, >=0;         # min broj MS koji mora biti prisutan u terminima jakog intenziteta
param nsi, integer, >=0;        # idealan broj MS u terminima jakog intenziteta
param nw, integer, >=0;         # min broj MS koji mora biti prisutan u terminima slabog inteziteta
param nwi, integer, >=0;        # idealan broj MS u terminima slabog inteziteta
param nis{D,s in SH}, default if s in SSH then nsi else nwi;   # idealan broj MS u danima/smenama sa posebnim potrebama
param wdpm, integer, >0;        # broj radnih dana u mesecu
param wtwd, integer, >0;        # obracunsko radno vreme

param M1, integer, >=0;         # tezina odstupanja od kriterijuma 1. prioriteta
param M2, integer, >=0;         # tezina odstupanja od kriterijuma 2. prioriteta
param M3, integer, >=0;         # tezina odstupanja od kriterijuma 3. prioriteta
param M4, integer, >=0;         # tezina odstupanja od kriterijuma 4. prioriteta
param t{n in N} := wdpm * wtwd * card(WD[n]) / dpm;   # norma u h

var x{N,D,PAT}, binary;         # da li sestra n dana d radi po paternu p
var dsL{D,SSH}, >=0;            # podbacaj broja MS u smenama jakog intenziteta
var dsT{D,SSH}, >=0;            # prebacaj broja MS u smenama jakog intenziteta
var dwL{D,WSH}, >=0;            # podbacaj broja MS u smenama slabog intenziteta
var dwT{D,WSH}, >=0;            # prebacaj broja MS u smenama slabog intenziteta
var daT{N}, >=0;                # prebacaj za preferirane izostanke
var tnL{N}, >=0;                # podbacaj norme u h
var tnT{N}, >=0;                # prebacaj norme u h
var tn, >=0;                    # maksimum svih odstupanja od radne norme

minimize f: M1 * sum{d in D, s in SSH} (dsL[d,s] + dsT[d,s]) +      # idealan broj MS u smenama jakog intenziteta
            M2 * sum{d in D, s in WSH} (dwL[d,s] + dwT[d,s]) +      # idealan broj MS u smenama slabog intenziteta
            M3 * sum{n in N} daT[n] +                               # zadovoljenje trazenih slobodnih dana/smena
            M4 * tn;                                                # odstupanje od mesecne norme radnog vremena
s.t.
    patern_dan{n in N, d in D}: sum{p in PAT} x[n,d,p] = 1;
    sequence_r{r in RS, n in N, d in 1..dpm-ts[r]+1}: sum{k in 1..ts[r]} x[n,d+k-1,prs[r,k]] <= ts[r] - 1;
    grouping_r{r in RG, n in NR[r], d in 1..dpm-tg[r]+1}: sum{k in d..d+tg[r]-1} x[n,k,prg[r]] <= nug[r];
    shift_exp{d in D, s in SH}:  sum{n in (NE inter NA[d]), p in PAT : patern[p,s]} x[n,d,p] >= ne;
    strong_min{d in D, s in SSH}: sum{n in NA[d],  p in PAT : patern[p,s]} x[n,d,p] >= ns;
    strong_idl{d in D, s in SSH}: sum{n in NA[d],  p in PAT : patern[p,s]} x[n,d,p] - dsT[d,s] + dsL[d,s] = nis[d,s];
    weaksh_min{d in D, s in WSH}: sum{n in NA[d],  p in PAT : patern[p,s]} x[n,d,p] >= nw;
    weaksh_idl{d in D, s in WSH}: sum{n in NA[d],  p in PAT : patern[p,s]} x[n,d,p] - dwT[d,s] + dwL[d,s] = nis[d,s];
    nowork{n in N : card(TF[n]) > 0}: sum{(d,s) in TF[n], p in PAT : patern[p,s]} x[n,d,p] = 0;
    yeswork{n in N : card(TW[n]) > 0}: sum{(d,s) in TW[n], p in PAT : patern[p,s]} x[n,d,p] = 1;
    pref_aps{n in N : card(TP[n]) > 0}: sum {(d,s) in TP[n], p in PAT : patern[p,s]} x[n,d,p] - daT[n] = 0;
    time_norm{n in N}: sum{d in WD[n], s in SH, p in PAT : patern[p,s]} tsh[s] * x[n,d,p] - tnT[n] + tnL[n] = t[n];
    time_devL{n in N}: tn >= tnL[n];
    time_devT{n in N}: tn >= tnT[n];

solve;

param col{d in 1..31}, symbolic := (if d <= 24 then "" else "A") & substr("CDEFGHIJKLMNOPQRSTUVWXYZABCDEFG", d, 1);
param del, symbolic := ",";     # <-- pod navodnike staviti podrazumevani delimiter u spredsit programu, tipicno: "," ili ";"
printf "Name\tTime\t";
printf{d in D} "%d\t", d;
printf{p in PAT} "Sum %s\t", p;
printf "\n";
for{n in N}{
    printf "%s\t%d\t", names[n], sum{d in WD[n], s in SH, p in PAT : patern[p,s]} tsh[s] * x[n,d,p];
    printf{d in D, p in PAT : x[n,d,p] = 1} "%s\t", if d in VD[n] then "v.d." else p;
    printf{p in PAT} "=COUNTIF(C%d:AG%d%s%d)\t", n + 1, n + 1, del, p;
    printf "\n";
}
printf "Tot.\tM:\t";
printf{d in D} "=COUNTIF(%s2:%s%d%s1)+COUNTIF(%s2:%s%d%s12)\t", col[d], col[d], card(N)+1, del, col[d], col[d], card(N)+1, del;
printf "\n\tA:\t";
printf{d in D} "=COUNTIF(%s2:%s%d%s2)+COUNTIF(%s2:%s%d%s12)\t", col[d], col[d], card(N)+1, del, col[d], col[d], card(N)+1, del;
printf "\n\tN:\t";
printf{d in D} "=COUNTIF(%s2:%s%d%s3)\t", col[d], col[d], card(N)+1, del;
printf "\nExp.\tM:\t";
printf{d in D} "=COUNTIF(%s2:%s%d%s1)+COUNTIF(%s2:%s%d%s12)\t", col[d], col[d], card(NE)+1, del, col[d], col[d], card(NE)+1, del;
printf "\n\tA:\t";
printf{d in D} "=COUNTIF(%s2:%s%d%s2)+COUNTIF(%s2:%s%d%s12)\t", col[d], col[d], card(NE)+1, del, col[d], col[d], card(NE)+1, del;
printf "\n\tN:\t";
printf{d in D} "=COUNTIF(%s2:%s%d%s3)\t", col[d], col[d], card(NE)+1, del;
printf "\n";

end;
