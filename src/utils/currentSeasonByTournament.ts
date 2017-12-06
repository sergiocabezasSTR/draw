import config from '../config.json'

const { wc, uefa } = config.currentSeason

type Stage = 'gs' | 'ko'

export default (tournament: string, stage: Stage) => {
  return tournament === 'wc' ? wc : uefa[tournament || 'cl'][stage || 'gs']
}
