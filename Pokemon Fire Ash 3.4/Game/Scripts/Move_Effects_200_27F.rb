#===============================================================================
# Increased crit rate with chance to inflict Poison, Paralysis or Sleep.
# (Dire Claw)
#===============================================================================
class PokeBattle_Move_200 < PokeBattle_Move
  def pbAdditionalEffect(user,target)
    return if target.damageState.substitute
    case @battle.pbRandom(3)
    when 0 then target.pbPoison(user) if target.pbCanPoison?(user, false, self)
    when 1 then target.pbParalyze if target.pbCanParalyze?(user, false, self)
    when 2 then target.pbSleep(user) if target.pbCanSleep?(user, false, self)
    end
  end
end


#===============================================================================
# Sets up Stealth Rock after dealing damage. (Stone Axe)
#===============================================================================
class PokeBattle_Move_201 < PokeBattle_Move
  def pbEffectGeneral(user)
    return if user.pbOpposingSide.effects[PBEffects::StealthRock]
    user.pbOpposingSide.effects[PBEffects::StealthRock] = true
    @battle.pbDisplay(_INTL("Pointed stones float in the air around {1}!",
       user.pbOpposingTeam(true)))
  end
end



#===============================================================================
# Increases the user's Attack, Defense and Speed by 1 stage each.
# (Victory Dance)
#===============================================================================
class PokeBattle_Move_202 < PokeBattle_MultiStatUpMove
  def initialize(battle,move)
    super
    @statUp = [:ATTACK,1,:DEFENSE,1,:SPEED,1]
  end
end



#===============================================================================
# Has a chance to poison the target and doubles in power if the target is 
# poisoned. (Barb Barrage)
#===============================================================================
class PokeBattle_Move_203 < PokeBattle_PoisonMove
  def pbBaseDamage(baseDmg,user,target)
    if target.poisoned? &&
       (target.effects[PBEffects::Substitute]==0 || ignoresSubstitute?(user))
      baseDmg *= 2
    end
    return baseDmg
  end
end



#===============================================================================
# Increased crit rate with 50% chance to lower defense and 30% chance to flinch
# (Triple Arrows)
#===============================================================================
class PokeBattle_Move_204 < PokeBattle_TargetStatDownMove
  def initialize(battle,move)
    super
    @statDown = [:DEFENSE, 1]
  end
  
  def flinchingMove?; return true; end

  def pbAdditionalEffect(user, target)
    super
    return if target.damageState.substitute
    target.pbFlinch(user) if @battle.pbRandom(100) < 30
  end
end  



#===============================================================================
# Has a chance to burn the target and doubles in power if the target is has any
# status condition (Infernal Parade)
#===============================================================================
class PokeBattle_Move_205 < PokeBattle_BurnMove
  def pbBaseDamage(baseDmg,user,target)
    if target.pbHasAnyStatus? &&
       (target.effects[PBEffects::Substitute]==0 || ignoresSubstitute?(user))
      baseDmg *= 2
    end
    return baseDmg
  end
end



#===============================================================================
# Increased hit rate and sets up Spikes (Ceaseless Edge)
#===============================================================================
class PokeBattle_Move_206 < PokeBattle_Move
  def pbEffectGeneral(user)
    if user.pbOpposingSide.effects[PBEffects::Spikes] < 3
      user.pbOpposingSide.effects[PBEffects::Spikes] += 1
      @battle.pbDisplay(_INTL("Spikes were scattered all around {1}'s feet!",
        user.pbOpposingTeam(true)))
    end
  end
end



#===============================================================================
# Cures the user's burn, poison or paralysis and raises its Sp. Atk and Sp. Def
# stats by 1 stage each. (Take Heart)
#===============================================================================
class PokeBattle_Move_207 < PokeBattle_MultiStatUpMove
  def initialize(battle,move)
    super
    @statUp = [:SPECIAL_ATTACK, 1, :SPECIAL_DEFENSE, 1]
  end
  
  def pbMoveFailed?(user,targets)
    return false if user.pbHasAnyStatus?
    return super 
  end 
  
  def pbEffectGeneral(user)
    user.pbCureStatus if user.pbHasAnyStatus?
    super 
  end 
end
