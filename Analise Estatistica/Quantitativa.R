com_ds <- read.delim("ComentariosRp.csv", encoding="UTF-8")

relevantes <- com_ds[com_ds$TIPOLOGIA !="IRRELEVANTE" && com_ds$TIPOLOGIA !="",]

defensores <- relevantes[grepl("DEFENSOR", relevantes$TIPOLOGIA), c("TIPOLOGIA")]
opositores <- relevantes[grepl("OPOSITOR", relevantes$TIPOLOGIA), c("TIPOLOGIA")]

#passivos <- relevantes[!grepl("AGRESSIVO", relevantes$TIPOLOGIA), c("TIPOLOGIA")]
#agressivos <- relevantes[grepl("AGRESSIVO", relevantes$TIPOLOGIA), c("TIPOLOGIA")]
#old.par <- par(mfrow=c(1, 2))

#Criando tabelas de frequencia
t_defensores <- table(droplevels(defensores)) / length(defensores)
t_opositores <- table(droplevels(opositores)) / length(opositores)

#Graf. Barras ativos vs passivos
barplot(c(t_defensores, t_opositores),
        main = "Comentários Passivos vs Ativos",
        las=T,
        #legend.text = T, 
        #args.legend = list(x = "topright", cex = 0.6),
        col = c("lightblue", "red","lightblue", "red"),
        xpd = F
        #axisnames = F,
        #names.arg = seq(0,1,0.2)
)
#A proporção de comentários agressivos está relacionada ao caso?
t_casos <- table(relevantes$CASO, relevantes$TIPOLOGIA)
