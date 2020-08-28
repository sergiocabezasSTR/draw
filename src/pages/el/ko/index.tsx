import React, {
  useState,
  useCallback,
  useMemo,
  useEffect,
  useRef,
  memo,
} from 'react'

import {
  range,
  shuffle,
} from 'lodash'

import Team from 'model/team/KnockoutTeam'
import getPossiblePairings from 'engine/predicates/uefa/getPossiblePairings'
import getPredicate from 'engine/predicates/uefa/ko'

import useDrawId from 'store/useDrawId'
import useXRay from 'store/useXRay'

import PotsContainer from 'ui/PotsContainer'
// import AirborneContainer from 'ui/AirborneContainer'
import MatchupsContainer from 'ui/MatchupsContainer'
import TablesContainer from 'ui/TablesContainer'
import BowlsContainer from 'ui/BowlsContainer'
import TeamBowl from 'ui/bowls/TeamBowl'
import Separator from 'ui/Separator'
import Announcement from 'ui/Announcement'

import Root from 'pages/Root'

interface Props {
  season: number,
  pots: readonly (readonly Team[])[],
}

interface State {
  currentMatchupNum: number,
  currentPotNum: number,
  possiblePairings: readonly number[] | null,
  matchups: readonly [Team, Team][],
}

function getState(): State {
  const currentPotNum = 1
  const currentMatchupNum = 0
  return {
    currentMatchupNum,
    currentPotNum,
    possiblePairings: null,
    matchups: range(16).map(() => [] as any),
  }
}

const ELKO = ({
  season,
  pots: initialPots,
}: Props) => {
  const [drawId, setNewDrawId] = useDrawId()

  const pots = useMemo(
    () => initialPots.map(pot => shuffle(pot)) as readonly Team[][],
    [initialPots, drawId],
  )

  const predicate = useMemo(() => getPredicate(season), [season])

  const [{
    currentMatchupNum,
    currentPotNum,
    possiblePairings,
    matchups,
  }, setState] = useState(getState)

  const [isXRay] = useXRay()

  const groupsContanerRef = useRef<HTMLElement>(null)

  const onBallPick = useCallback((i: number) => {
    const currentPot = pots[currentPotNum]
    const index = possiblePairings ? possiblePairings[i] : i
    const selectedTeam = currentPot.splice(index, 1)[0]

    const newMatchups = matchups.slice()
    // @ts-ignore
    newMatchups[currentMatchupNum] = [
      ...newMatchups[currentMatchupNum],
      selectedTeam,
    ]

    const newPossiblePairings = currentPotNum === 1
      ? getPossiblePairings(pots, newMatchups, predicate)
      : null

    const newCurrentMatchNum = currentMatchupNum - currentPotNum + 1

    setState({
      currentPotNum: 1 - currentPotNum,
      currentMatchupNum: newCurrentMatchNum,
      possiblePairings: newPossiblePairings,
      matchups: newMatchups,
    })
  }, [predicate, pots, matchups, currentPotNum, currentMatchupNum, possiblePairings])

  const autoPickIfOneBall = () => {
    const isOnlyChoice = possiblePairings?.length === 1
      || currentPotNum === 1 && pots[1].length === 1
    if (isOnlyChoice) {
      onBallPick(0)
    }
  }

  useEffect(() => {
    setTimeout(autoPickIfOneBall, 250)
  }, [currentPotNum])

  const teamBowlPot = useMemo(
    () => possiblePairings && pots[0].filter((team, i) => possiblePairings.includes(i)),
    [possiblePairings],
  )

  const completed = currentMatchupNum >= initialPots[0].length
  const selectedTeams = possiblePairings ? possiblePairings.map(i => pots[0][i]) : []

  return (
    <Root>
      <TablesContainer>
        <PotsContainer
          selectedTeams={selectedTeams}
          initialPots={initialPots}
          pots={pots}
          currentPotNum={currentPotNum}
          split
        />
        <MatchupsContainer
          ref={groupsContanerRef}
          matchups={matchups}
        />
      </TablesContainer>
      <BowlsContainer>
        {!completed && (
          <Separator>Runners-up</Separator>
        )}
        <TeamBowl
          forceNoSelect={currentPotNum === 0}
          display={!completed}
          displayTeams={isXRay}
          selectedTeam={null}
          pot={pots[1]}
          onPick={onBallPick}
        />
        {!completed && (
          <Separator>Group Winners</Separator>
        )}
        {completed && (
          <Announcement
            long={false}
            completed={completed}
            selectedTeam={null}
            pickedGroup={null}
            possibleGroups={null}
            numGroups={0}
            groupsElement={groupsContanerRef.current}
            reset={setNewDrawId}
          />
        )}
        {teamBowlPot && (
          <TeamBowl
            forceNoSelect={currentPotNum === 1}
            display={!completed}
            displayTeams={isXRay}
            selectedTeam={null}
            pot={teamBowlPot}
            onPick={onBallPick}
          />
        )}
      </BowlsContainer>
    </Root>
  )
}

export default memo(ELKO)
