set xdata time
set timefmt "%d-%m-%Y %H:%M"
set format x "%d., %H:%M"
set ylabel "Freie Plätze"
set title "Letzte Woche" 
#set style fill solid
set style fill pattern border

#set color "green"
set terminal png size 350,200 enhanced font "Helvetica,10"
set output "kitbib_7.png" 
plot 'kitbib_7.txt' using 1:4 title "KIT-Bib"
set output "rest_7.png" 
plot 'bibn_7.txt' using 1:4 with boxes title "Bib - Campus Nord" lt-1, \
 'fbp_7.txt' using 1:4 with boxes title "Physiker-Bib" lt-1, \
 'laf_7.txt' using 1:4 with boxes title "Lernzentrum" lt-1
 
set title "Letzte 24h" 
set format x "%H:%M"
set output "kitbib_24.png" 
plot 'kitbib_24.txt' using 1:4 title "KIT-Bib"
set output "rest_24.png" 
plot 'bibn_24.txt' using 1:4 with boxes title "Bib - Campus Nord", \
 'fbp_24.txt' using 1:4 with boxes title "Physiker-Bib", \
 'laf_24.txt' using 1:4 with boxes title "Lernzentrum"

set title "Letzte 3h" 
set output "kitbib_3.png" 
plot 'kitbib_3.txt' using 1:4 with boxes title "KIT-Bib"
set output "rest_3.png" 
plot 'bibn_3.txt' using 1:4 with boxes title "Bib - Campus Nord", \
 'fbp_3.txt' using 1:4 with boxes title "Physiker-Bib", \
 'laf_3.txt' using 1:4 with boxes title "Lernzentrum"