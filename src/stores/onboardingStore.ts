import { create } from 'zustand'

export type UserType = 'student' | 'professional' | 'switcher' | null

export interface OnboardingAnswers {
  // Screen 2
  userType: UserType
  // Screen 3
  currentRole: string
  currentField: string
  yearsExperience: number
  education: string
  // Screen 4
  currentSkills: string[]
  skillLevels: Record<string, number> // skill -> 1-3 confidence
  customSkills: string[]
  // Screen 5
  targetRole: string
  targetField: string
  seniorityTarget: string
  motivation: string[]
  // Screen 6
  timeBudgetMinutes: number
  preferredLearningStyle: string[]
  preferredStudyTime: string
  blockers: string[]
}

interface OnboardingState {
  currentScreen: number
  answers: Partial<OnboardingAnswers>
  setScreen: (n: number) => void
  setAnswer: <K extends keyof OnboardingAnswers>(key: K, value: OnboardingAnswers[K]) => void
  setAnswers: (partial: Partial<OnboardingAnswers>) => void
  reset: () => void
  // Computed
  totalScreens: number
  progress: number
}

const INITIAL: Partial<OnboardingAnswers> = {
  userType: null,
  currentSkills: [],
  skillLevels: {},
  customSkills: [],
  motivation: [],
  preferredLearningStyle: [],
  blockers: [],
  timeBudgetMinutes: 60,
  yearsExperience: 0,
}

export const useOnboardingStore = create<OnboardingState>((set, get) => ({
  currentScreen: 1,
  answers: { ...INITIAL },
  totalScreens: 7,

  get progress() {
    return Math.round((get().currentScreen / 7) * 100)
  },

  setScreen: (n) => set({ currentScreen: n }),

  setAnswer: (key, value) =>
    set((state) => ({
      answers: { ...state.answers, [key]: value },
    })),

  setAnswers: (partial) =>
    set((state) => ({
      answers: { ...state.answers, ...partial },
    })),

  reset: () => set({ currentScreen: 1, answers: { ...INITIAL } }),
}))
