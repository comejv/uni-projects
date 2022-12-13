{1M {G} {A 3M {} {DA} ?} ? C !} C !

#si rien devant
#   avance
#   si rien à gauche
#       gauche
#       avance
#   sinon
#       pass
#sinon
#   droite
#
# => suivre le mur avec la main gauche

# Marche bien quand pas d'ilot
# donc tourne en boucle dans terrain_6.txt
# mais sort dans terrain_5.txt

# 20 25 25 .4 1234 82%
# 20 25 25 .7 1234 100%