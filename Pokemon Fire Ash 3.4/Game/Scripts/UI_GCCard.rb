#===============================================================================
#
#===============================================================================
class GCCard_Scene
  def pbUpdate
    pbUpdateSpriteHash(@sprites)
  end

  def pbStartScene
    @viewport = Viewport.new(0,0,Graphics.width,Graphics.height)
    @viewport.z = 99999
    @sprites = {}
    background = pbResolveBitmap(sprintf("Graphics/Pictures/Trainer Card/bg_f"))
    if $Trainer.female? && background
      addBackgroundPlane(@sprites,"bg","Trainer Card/bg_f",@viewport)
    else
      addBackgroundPlane(@sprites,"bg","Trainer Card/bg",@viewport)
    end
    cardexists = pbResolveBitmap(sprintf("Graphics/Pictures/Trainer Card/GCcard"))
    @sprites["card"] = IconSprite.new(0,0,@viewport)
    @sprites["card"].setBitmap("Graphics/Pictures/Trainer Card/GCcard")
    @sprites["overlay"] = BitmapSprite.new(Graphics.width,Graphics.height,@viewport)
    pbSetSystemFont(@sprites["overlay"].bitmap)
    @sprites["trainer"] = IconSprite.new(336,112,@viewport)
    @sprites["trainer"].setBitmap(GameData::TrainerType.player_front_sprite_filename($Trainer.trainer_type))
    @sprites["trainer"].x -= (@sprites["trainer"].bitmap.width-128)/2
    @sprites["trainer"].y -= (@sprites["trainer"].bitmap.height-128)
    @sprites["trainer"].z = 2
    pbDrawGCCard
    pbFadeInAndShow(@sprites) { pbUpdate }
  end

  def pbDrawGCCard
    overlay = @sprites["overlay"].bitmap
    overlay.clear
    baseColor   = Color.new(72,72,72)
    shadowColor = Color.new(160,160,160)
    totalsec = Graphics.frame_count / Graphics.frame_rate
    hour = totalsec / 60 / 60
    min = totalsec / 60 % 60
    time = (hour>0) ? _INTL("{1}h {2}m",hour,min) : _INTL("{1}m",min)
    $PokemonGlobal.startTime = pbGetTimeNow if !$PokemonGlobal.startTime
    starttime = _INTL("{1} {2}, {3}",
       pbGetAbbrevMonthName($PokemonGlobal.startTime.mon),
       $PokemonGlobal.startTime.day,
       $PokemonGlobal.startTime.year)
    textPositions = [
       [_INTL("Practice"),32,71,0,baseColor,shadowColor],
       [_INTL("Club"),135,71,0,baseColor,shadowColor],
       [_INTL("Gauntlet"),232,71,0,baseColor,shadowColor],
       [_INTL("ID No."),332,58,0,baseColor,shadowColor],
       [sprintf("%05d",$Trainer.public_ID),468,58,1,baseColor,shadowColor],
       [_INTL("Mayhem"),36,217,0,baseColor,shadowColor],
       [_INTL("Sygna"),135,217,0,baseColor,shadowColor],
       [_INTL("Titan"),236,217,0,baseColor,shadowColor],
       [_INTL("Credits"),323,322,0,baseColor,shadowColor],
       [_INTL("#{$game_variables[80]}"),450,322,0,baseColor,shadowColor]
    ]
    pbDrawTextPositions(overlay,textPositions)
    imagePositions = []
    if $game_variables[91] > 3
      nd = 3
    else
      nd = $game_variables[91]
    end
    imagePositions.push(["Graphics/Pictures/Trainer Card/Practice_medals",33,117,(nd-1)*84,0,84,84])
    if $game_variables[92] > 3
      nd = 3
    else
      nd = $game_variables[92]
    end
    if $game_variables[92] > 0
      imagePositions.push(["Graphics/Pictures/Trainer Card/Club_ribbons",157,117,(nd-1)*36,0,36,84])
    end
    if $game_variables[93] > 3
      nd = 3
    else
      nd = $game_variables[93]
    end
    imagePositions.push(["Graphics/Pictures/Trainer Card/Gauntlet_embelems",233,117,(nd-1)*84,0,84,84])
    if $game_variables[94] > 3
      nd = 3
    else
      nd = $game_variables[94]
    end
    imagePositions.push(["Graphics/Pictures/Trainer Card/Mayhem_plaques",33,264,(nd-1)*84,0,84,84])
    if $game_variables[95] <= 0
      nd = 0
    elsif $game_variables[95] >= $game_variables[97]
      nd = 3
    elsif $game_variables[95] >= $game_variables[97]/2
      nd = 2
    else
      nd = 1
    end
    if nd > 0
      imagePositions.push(["Graphics/Pictures/Trainer Card/Sygna_medallions",148,266,(nd-1)*53,0,53,84])
    end
    if $game_variables[96] <= 0
      nd = 0
    elsif $game_variables[96] >= $game_variables[97]
      nd = 3
    elsif $game_variables[96] >= $game_variables[97]/2
      nd = 2
    else
      nd = 1
    end
    if nd > 0
      imagePositions.push(["Graphics/Pictures/Trainer Card/Titan_crowns",233,264,(nd-1)*84,0,84,84])
    end
    pbDrawImagePositions(overlay,imagePositions)
  end

  def pbGCCard
    pbSEPlay("GUI trainer card open")
    loop do
      Graphics.update
      Input.update
      pbUpdate
      if Input.trigger?(Input::BACK)
        pbPlayCloseMenuSE
        break
      end
    end
  end

  def pbEndScene
    pbFadeOutAndHide(@sprites) { pbUpdate }
    pbDisposeSpriteHash(@sprites)
    @viewport.dispose
  end
end

#===============================================================================
#
#===============================================================================
class GCCardScreen
  def initialize(scene)
    @scene = scene
  end

  def pbStartScreen
    @scene.pbStartScene
    @scene.pbGCCard
    @scene.pbEndScene
  end
end
