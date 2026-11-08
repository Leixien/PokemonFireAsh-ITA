# lead and ace are the species of the trainer's lead and ace Pokemon, respectively
# possibilities is an array with all the possible choices. Defaults to empty
# number is the total number of Pokemon on the team. Defaults to six.
# - this value does include the lead and the ace, so add 2.
# - the code has error handlers that prevent the creation of teams larger than six, or of teams larger than the array above will allow.
# name is the trainer's name. Defaults to Bobby
# class is the type of trainer they are (Ace Trainer, Gym Leader, etc.). Defaults to Youngster.

# This version of the code is for making the Pokemon have "default" moves.
# Easier to use, but less precise
def defaultRandomTeam(lead,ace,possibilities=[],number=6,name="Bobby",trainerid=:YOUNGSTER)
# Allow for multiple types of inputting species types
# numbers, strings of the Pokemon's name, or the internal name
if lead.is_a?(String) || lead.is_a?(Symbol)
lead=getConst(PBSpecies,lead)
end
if ace.is_a?(String) || ace.is_a?(Symbol)
lead=getConst(PBSpecies,ace)
end
for i in 0...possibilities.length
if possibilities[i].is_a?(String) || possibilities[i].is_a?(Symbol)
possibilities[i]=getConst(PBSpecies,possibilities[i])
end
end
# Allow for multiple methods of inputting trainer type names
if trainerid.is_a?(String) || trainerid.is_a?(Symbol)
trainerid=getConst(PBTrainers,trainerid)
end
# create the "lead" pokemon
poke1=createPokemon(lead,64) # change the 64 to be the level you want the Pokemon to be
team=[poke1]
# create the "grunt" pokemon
grunts=[possibilities.length,number-2,4].min
if grunts>0
for i in 0...grunts
# choosing a random Pokemon from the list of possibilities
poke=rand(possibilities.length)
poke2=createPokemon(possibilities[poke],64) # again, change 64 to the proper level
team.push(poke2)
# removing the chosen Pokemon from the list of possibilities so it doesn't get picked again.
possibilities[poke]=nil
possibilities.compact!
end
end
# create the "ace" pokemon
poke3=createPokemon(ace,64) # change the 64 to be the level you want the Pokemon to be
team.push(poke3)
# create the trainer
return createTrainer(trainerid,name,team)
end

# this version of the code allows you to define Pokemon complete with moves, specific abilities, etc.
# more custom and precise, but requires more initialization
def definedRandomTeam(lead,ace,possibilities=[],number=6,name="Bobby",trainerid=:YOUNGSTER)
# Allow for multiple methods of inputting trainer type names
if trainerid.is_a?(String) || trainerid.is_a?(Symbol)
trainerid=getConst(PBTrainers,trainerid)
end
# add the lead
team=[lead]
# add the grunts
grunts=[possibilities.length,number-2,4].min
if grunts>0
for i in 0...grunts
# choosing a random Pokemon from the list of possibilities
poke=rand(possibilities.length)
team.push(possibilities[poke])
# removing the chosen Pokemon from the list of possibilities so it doesn't get picked again.
possibilities[poke]=nil
possibilities.compact!
end
end
# add the ace
team.push(ace)
# create the trainer
return createTrainer(trainerid,name,team)
end



def waterLeaderRematch
  lead=createPokemon(:POLITOED,64)
  lead.setAbility(2) # give Hidden Ability (Water Absorb)
  ace=createPokemon(:LANTURN,64)
  ace.item=getConst(:CHARCOAL) # give it the item Assault Vest
  grunt1=createPokemon(:LUDICOLO,64)
  grunt1.makeMale # make it male
  grunt1.name="Miror B" # nickname it Miror B
  grunt2=createPokemon(:GASTRODON,64)
  grunt2.form=0 # give it the first form, for East Sea
  grunt3=createPokemon(:MILOTIC,64)
  grunt3.makeFemale # make it female
  grunt3.makeShiny # make it shiny
  grunt4=createPokemon(:JELLICENT,64)
  # Note that in Essentials, the stats go in this order:
  # HP, Attack, Defense, Speed, SpAtk, SpDef
  # Most Pokemon things list Speed at the end, so don't make the mistake of directly copying
  grunt4=ev=[248,0,216,44,0,0] # set the EVs
  grunt5=createPokemon(:SWANNA,64)
  grunt5.iv=[31,31,31,31,30,30] # give it Hidden Power Ground
  grunt5.pbLearnMove(:HIDDENPOWER) # teach it Hidden Power
  grunt6=createPokemon(:BARBARACLE,64)
  grunt6.setNature(:ADAMANT)  # give it an Adamant nature
  grunt7=createPokemon(:GYARADOS,64)
  # Allow the Gyarados to Mega Evolve
  grunt7.item=getConst(:GYARADOSITE) if hasConst?(:GYARADOSITE)
  grunt8=createPokemon(:LAPRAS,64)
  grunts=[grunt1,grunt2,grunt3,grunt4,grunt5,grunt6,grunt7,grunt8]
  return definedRandomTeam(lead,ace,grunts,6,"Bob",:SECRET_Brock)
end