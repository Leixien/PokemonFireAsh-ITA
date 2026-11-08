#==============================================================================
# * Scene_Credits
#------------------------------------------------------------------------------
# Scrolls the credits you make below. Original Author unknown.
#
## Edited by MiDas Mike so it doesn't play over the Title, but runs by calling
# the following:
#    $scene = Scene_Credits.new
#
## New Edit 3/6/2007 11:14 PM by AvatarMonkeyKirby.
# Ok, what I've done is changed the part of the script that was supposed to make
# the credits automatically end so that way they actually end! Yes, they will
# actually end when the credits are finished! So, that will make the people you
# should give credit to now is: Unknown, MiDas Mike, and AvatarMonkeyKirby.
#                                             -sincerly yours,
#                                               Your Beloved
# Oh yea, and I also added a line of code that fades out the BGM so it fades
# sooner and smoother.
#
## New Edit 24/1/2012 by Maruno.
# Added the ability to split a line into two halves with <s>, with each half
# aligned towards the centre. Please also credit me if used.
#
## New Edit 22/2/2012 by Maruno.
# Credits now scroll properly when played with a zoom factor of 0.5. Music can
# now be defined. Credits can't be skipped during their first play.
#
## New Edit 25/3/2020 by Maruno.
# Scroll speed is now independent of frame rate. Now supports non-integer values
# for SCROLL_SPEED.
#
## New Edit 21/8/2020 by Marin.
# Now automatically inserts the credits from the plugins that have been
# registered through the PluginManager module.
#==============================================================================
class Scene_Credits
  # Backgrounds to show in credits. Found in Graphics/Titles/ folder
  BACKGROUNDS_LIST       = ["credits1", "credits2", "credits3", "credits4", "credits5"]
  BGM                    = "ThemeSong"
  SCROLL_SPEED           = 40   # Pixels per second
  SECONDS_PER_BACKGROUND = 80
  TEXT_OUTLINE_COLOR     = Color.new(0, 0, 128, 255)
  TEXT_BASE_COLOR        = Color.new(255, 255, 255, 255)
  TEXT_SHADOW_COLOR      = Color.new(0, 0, 0, 100)

  # This next piece of code is the credits.
  # Start Editing
  CREDIT = <<_END_

Pokémon Fire Ash was created by:
Hunter Hoesch



Extra images supplied by:
akuma tsubasa<s>Alan Flygon
alejox51<s>Amethyst
Andrews Sprites<s>aniki0001
Arclart<s>aveontrainer
backburner26<s>beliot419
Bioseth<s>blckwh
BrendanBass<s>Brumirage
capylus<s>chasemortier
ChriSX698<s>CynthiaCelestic
darkgaara736<s>DarkusShadow
drawnamu<s>DSIKJHEZDIURH8EU09UR
[Espada]<s>fridave
Furs the Fox<s>geno2925
Giervlion<s>gnomowladny
Grimmjow<s>gregarlink10
hamsterSKULL<s>HeXeR
izzyvicious<s>Johnny05
kaleriodion<s>kcbabaz
leparagon<s>Mademoiselle
mattmc95<s>Maxewen
MrDollSteak<s>Muzyun
MyMarshlands<s>Nataniel-Sama
NicoMts<s>Pinta77
piphybuilder88<s>pklucario
PKMNTrainerSpriterC<s>Pokecharms
pokemonrater<s>pokemon subrosia
PowerCristal<s>PrettySoldierPetite
princess phoenix<s>Psilo
PurpleZaffre<s>Quanyails
rayd12smitty<s>Remus Lupin
Rogor<s>SageDeoxys
segesi<s>ShiningStars5022
Silver Death<s>Silentninja
<s>SilverTheRiolu123<s>shinyaeon
starsparkless<s>superangel1502
supersilver27<s>swdfm
tebited15<s>thedarkdragon11
thegoku7729<s>TheHero2
TSR<s>ue_wal16
Versekr Dark<s>wally217
wolfang62<s>YellowTemperance
zender1752

Extra sounds supplied by:
G-Master
Phasma
Morningdew

Additional code by:
Badhaas<s>(Box unlocking script)
Crystal Noel<s>(Evolution Moves script)
Zerokid<s>(Evolution Moves fix)
FL<s>(Pokémon Selection script)
Marin<s>(Better Fast-forward script)
Mashirosakura<s>(Wild Hidden Ability script)
Hunter Hoesch
Lucas Hoesch
Maq47

Additional help by:
Abs Samantha
Hitsukid
Intweener
LaDestitute
Lucas Hoesch
Maq47
Marek14
Meru Otonashi
Takeshi55
The Matrix Net
WittleBuddy
and everyone who helped out on the Discord

Tested by:
Hunter Hoesch
Lucas Hoesch
Maq47
Luc-ker
SytherSK

Walk-through created by:
Marek14, Ebrethil, and Abs Samantha


{INSERTS_PLUGIN_CREDITS_DO_NOT_REMOVE}

"Pokémon Essentials" was created by:
Flameguru
Poccil (Peter O.)
Maruno

With contributions from:
AvatarMonkeyKirby<s>Marin
Boushy<s>MiDas Mike
Brother1440<s>Near Fantastica
FL.<s>PinkMan
Genzai Kawakami<s>Popper
Golisopod User<s>Rataime
help-14<s>Savordez
IceGod64<s>SoundSpawn
Jacob O. Wobbrock<s>the__end
KitsuneKouta<s>Venom12
Lisa Anthony<s>Wachunga
Luka S.J.<s> 
and everyone else who helped out

"mkxp-z" by:
Roza
Based on MKXP by Ancurio et al.

"RPG Maker XP" by:
Enterbrain

Pokémon is owned by:
The Pokémon Company
Nintendo
Affiliated with Game Freak



This is a non-profit fan-made game.
No copyright infringements intended.
Please support the official games!

_END_
# Stop Editing

  def main
    #-------------------------------
    # Animated Background Setup
    #-------------------------------
    @counter = 0.0   # Counts time elapsed since the background image changed
    @bg_index = 0
    @bitmap_height = Graphics.height   # For a single credits text bitmap
    @trim = Graphics.height / 10
    # Number of game frames per background frame
    @realOY = -(Graphics.height - @trim)
    #-------------------------------
    # Credits text Setup
    #-------------------------------
    plugin_credits = ""
    PluginManager.plugins.each do |plugin|
      pcred = PluginManager.credits(plugin)
      plugin_credits << "\"#{plugin}\" v.#{PluginManager.version(plugin)} by:\n"
      if pcred.size >= 5
        plugin_credits << pcred[0] + "\n"
        i = 1
        until i >= pcred.size
          plugin_credits << pcred[i] + "<s>" + (pcred[i + 1] || "") + "\n"
          i += 2
        end
      else
        pcred.each { |name| plugin_credits << name + "\n" }
      end
      plugin_credits << "\n"
    end
    CREDIT.gsub!(/\{INSERTS_PLUGIN_CREDITS_DO_NOT_REMOVE\}/, plugin_credits)
    credit_lines = CREDIT.split(/\n/)
    #-------------------------------
    # Make background and text sprites
    #-------------------------------
    text_viewport = Viewport.new(0, @trim, Graphics.width, Graphics.height - (@trim * 2))
    text_viewport.z = 99999
    @background_sprite = IconSprite.new(0, 0)
    @background_sprite.setBitmap("Graphics/Titles/" + BACKGROUNDS_LIST[0])
    @credit_sprites = []
    @total_height = credit_lines.size * 32
    lines_per_bitmap = @bitmap_height / 32
    num_bitmaps = (credit_lines.size.to_f / lines_per_bitmap).ceil
    for i in 0...num_bitmaps
      credit_bitmap = Bitmap.new(Graphics.width, @bitmap_height)
      pbSetSystemFont(credit_bitmap)
      for j in 0...lines_per_bitmap
        line = credit_lines[i * lines_per_bitmap + j]
        next if !line
        line = line.split("<s>")
        xpos = 0
        align = 1   # Centre align
        linewidth = Graphics.width
        for k in 0...line.length
          if line.length > 1
            xpos = (k == 0) ? 0 : 20 + Graphics.width / 2
            align = (k == 0) ? 2 : 0   # Right align : left align
            linewidth = Graphics.width / 2 - 20
          end
          credit_bitmap.font.color = TEXT_SHADOW_COLOR
          credit_bitmap.draw_text(xpos,     j * 32 + 8, linewidth, 32, line[k], align)
          credit_bitmap.font.color = TEXT_OUTLINE_COLOR
          credit_bitmap.draw_text(xpos + 2, j * 32 - 2, linewidth, 32, line[k], align)
          credit_bitmap.draw_text(xpos,     j * 32 - 2, linewidth, 32, line[k], align)
          credit_bitmap.draw_text(xpos - 2, j * 32 - 2, linewidth, 32, line[k], align)
          credit_bitmap.draw_text(xpos + 2, j * 32,     linewidth, 32, line[k], align)
          credit_bitmap.draw_text(xpos - 2, j * 32,     linewidth, 32, line[k], align)
          credit_bitmap.draw_text(xpos + 2, j * 32 + 2, linewidth, 32, line[k], align)
          credit_bitmap.draw_text(xpos,     j * 32 + 2, linewidth, 32, line[k], align)
          credit_bitmap.draw_text(xpos - 2, j * 32 + 2, linewidth, 32, line[k], align)
          credit_bitmap.font.color = TEXT_BASE_COLOR
          credit_bitmap.draw_text(xpos,     j * 32,     linewidth, 32, line[k], align)
        end
      end
      credit_sprite = Sprite.new(text_viewport)
      credit_sprite.bitmap = credit_bitmap
      credit_sprite.z      = 9998
      credit_sprite.oy     = @realOY - @bitmap_height * i
      @credit_sprites[i] = credit_sprite
    end
    #-------------------------------
    # Setup
    #-------------------------------
    # Stops all audio but background music
    previousBGM = $game_system.getPlayingBGM
    pbMEStop
    pbBGSStop
    pbSEStop
    pbBGMFade(2.0)
    pbBGMPlay(BGM)
    Graphics.transition(20)
    loop do
      Graphics.update
      Input.update
      update
      break if $scene != self
    end
    pbBGMFade(2.0)
    Graphics.freeze
    Graphics.transition(20, "fadetoblack")
    @background_sprite.dispose
    @credit_sprites.each { |s| s.dispose if s }
    text_viewport.dispose
    $PokemonGlobal.creditsPlayed = true
    pbBGMPlay(previousBGM)
  end

  # Check if the credits should be cancelled
  def cancel?
    if Input.trigger?(Input::USE) && $PokemonGlobal.creditsPlayed
      $scene = Scene_Map.new
      pbBGMFade(1.0)
      return true
    end
    return false
  end

  # Checks if credits bitmap has reached its ending point
  def last?
    if @realOY > @total_height + @trim
      $scene = ($game_map) ? Scene_Map.new : nil
      pbBGMFade(2.0)
      return true
    end
    return false
  end

  def update
    delta = Graphics.delta_s
    @counter += delta
    # Go to next slide
    if @counter >= SECONDS_PER_BACKGROUND
      @counter -= SECONDS_PER_BACKGROUND
      @bg_index += 1
      @bg_index = 0 if @bg_index >= BACKGROUNDS_LIST.length
      @background_sprite.setBitmap("Graphics/Titles/" + BACKGROUNDS_LIST[@bg_index])
    end
    return if cancel?
    return if last?
    @realOY += SCROLL_SPEED * delta
    @credit_sprites.each_with_index { |s, i| s.oy = @realOY - @bitmap_height * i }
  end
end
