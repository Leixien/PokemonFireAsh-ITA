def createNew(maxtrainers)
  trainers = []
  for i in 1...maxtrainers + 1
    trainers.push(i)
  end
  $game_variables[79] = trainers
end

def trainerCheck(trainers,max)
  for i in 0...max
    if $game_variables[100] == trainers[i]
      return true
    end
  end
  return false
end

def randomTrainer(number,increment)
  trainers = $game_variables[79]
  max = trainers.length
  $game_variables[100] = rand(number) + 1 + increment
  check = trainerCheck(trainers,max)
  while check == false
    $game_variables[100] = rand(number) + 1 + increment
    check = trainerCheck(trainers,max)
  end
  trainers.delete($game_variables[100])
  $game_variables[79] = trainers
end

