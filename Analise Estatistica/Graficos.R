library('tm')
library('wordcloud')

comentarios_ds <- read.delim("D:/code/R/RPI/comentarios.csv", encoding="UTF-8")
c = comentarios_ds$TIPOLOGIA, comentarios_ds$INTEGRANTE)

barplot(c, 
        col = brewer.pal(8, 'Dark2'), 
        legend.text = T, 
        args.legend = list(x = "topleft", cex = 0.4),
        xpd = T,
        las=2)